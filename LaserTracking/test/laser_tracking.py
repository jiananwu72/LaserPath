import cv2
import numpy as np
import time
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

# -----------------------------
# Setup for the PCA9685 and Servos
# -----------------------------
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 100  # Adjust as needed

# Define channels for horizontal and vertical servo control
x_direction = 0
y_direction = 1
steer=14

horizontal_servo = servo.Servo(pca.channels[x_direction])
vertical_servo = servo.Servo(pca.channels[y_direction])
steer_servo =servo.Servo(pca.channels[steer])
# Set initial servo positions to 90° (center)
horizontal_angle = 90
vertical_angle = 90
horizontal_servo.angle = horizontal_angle
vertical_servo.angle = vertical_angle

steer_angle=90
steer_servo.angle=steer_angle
# -----------------------------
# Setup for Video Capture and Laser Detection
# -----------------------------
cap = cv2.VideoCapture(0)

# Define a high lightness threshold (0-255) for the laser
lightness_threshold = 240  # Slightly lowered for better detection

# Proportional gain for servo adjustments (tune as necessary)
kp = 0.01
scan_horizontal_angle=0
scan_vertical_angle=0
scan_h=5
scan_v=5
scan_step=2

# Minimum contour area to consider (laser point is typically small)
min_area = 10

print("Starting laser tracking (headless mode) using only lightness detection. Press Ctrl+C to exit.")

try:
    while True:
        capture, frame = cap.read()
        if not capture:
            print("Failed to capture frame.")
            break

        # Optionally flip the frame if needed (adjust for your camera orientation)
        frame = cv2.flip(frame, 0)

        # Convert the frame to grayscale and apply a lightness threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, light_mask = cv2.threshold(gray, lightness_threshold, 255, cv2.THRESH_BINARY)

        # Use morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        light_mask = cv2.erode(light_mask, kernel, iterations=1)
        light_mask = cv2.dilate(light_mask, kernel, iterations=2)

        # Find contours in the light mask
        contours, _ = cv2.findContours(light_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        laser_detected=False
        if contours:
            # Choose the largest contour (assumed to be the laser point)
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > min_area:
                M = cv2.moments(c)
                
                if M["m00"] == 0:
                    laser_detected=False
                else:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    laser_detected =True
                    # Calculate error between the detected laser point and the frame's center
                    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
                    error_x = frame_center[0] - cX  
                    error_y = frame_center[1] - cY
                    #theta_x=np.arctan(error_x/error_y)
                    #theta_y=np.arctan(error_y/error_x)
                    # Adjust servo angles using proportional control
                    horizontal_angle += error_x * kp
                    vertical_angle   += error_y * kp
                    steer_angle = 180-horizontal_angle 

                    # Constrain angles to valid servo limits (0° to 180°)
                    horizontal_angle = max(0, min(180, horizontal_angle))
                    vertical_angle   = max(0, min(180, vertical_angle))
                    steer_angle      = max(0, min(180, steer_angle))

                    # Update servo positions
                    horizontal_servo.angle = horizontal_angle
                    vertical_servo.angle = vertical_angle
                    steer_servo.angle= steer_angle

                    # images the mask
                    cv2.imwrite("mask.jpg", light_mask)
                    cv2.imwrite("frame.jpg", frame)

                    print(f"Laser detected at ({cX}, {cY}). "
                          f"Servo angles adjusted to: Horizontal={horizontal_angle:.2f}, Vertical={vertical_angle:.2f}, Steer={steer_angle:.2f}")


        if not laser_detected:
            scan_horizontal_angle += scan_h
            if scan_horizontal_angle >= 180:
                scan_horizontal_angle =0
                scan_horizontal_angle = max(0, min(180, scan_horizontal_angle))
                scan_vertical_angle += scan_v
                scan_vertical_angle   = max(0, min(180, scan_vertical_angle))
            if scan_vertical_angle >= 180:
                scan_vertical_angle = 0
                scan_vertical_angle   = max(0, min(180, scan_vertical_angle))
            horizontal_servo.angle = scan_horizontal_angle
            vertical_servo.angle = scan_vertical_angle
            print(f"Scanning: Horizontal Angle={scan_horizontal_angle:.2f}, Vertical Angle={scan_vertical_angle:.2f}")
        # A short delay to reduce CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Laser tracking terminated by user.")

cap.release()
