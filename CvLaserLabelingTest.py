import cv2
import numpy as np

# Load the image (replace 'input_image.jpg' with your image file)
image = cv2.imread('LaserPath/TestImages/LaserOnFE.jpg')

# Convert the image from BGR to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define lower and upper ranges for the red color in HSV.
# Note: Red spans across the 0 and 180 hue values, so we use two ranges.
lower_red1 = np.array([0, 230, 230])
upper_red1 = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

lower_red2 = np.array([160, 230, 230])
upper_red2 = np.array([179, 255, 255])
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

# Combine the two masks
mask = cv2.bitwise_or(mask1, mask2)

# Optionally, clean up the mask using morphological operations
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Assume the largest contour corresponds to the laser beam
    largest_contour = max(contours, key=cv2.contourArea)

    # Compute the moments of the largest contour to find the center
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        centerX = int(M["m10"] / M["m00"])
        centerY = int(M["m01"] / M["m00"])
    else:
        centerX, centerY = 0, 0

    # Draw a circle at the detected center
    cv2.circle(image, (centerX, centerY), 10, (0, 255, 0), -1)  # Green circle

    # Optionally, draw a bounding rectangle around the contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle

    # Label the detected position with text
    label_text = f"Laser: ({centerX}, {centerY})"
    cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
else:
    print("No red laser beam detected.")

# Save the annotated image to a file
cv2.imwrite("LaserPath/TestImages/lbdLaserOnFE.jpg", image)

# Optionally, display the result in a window (press any key to close)
cv2.imshow("Detected Laser", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
