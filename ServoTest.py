import RPi.GPIO as GPIO
import time

# Define the GPIO pin (using BCM numbering) where the servo signal is connected.
SERVO_PIN = 10

# Setup GPIO using BCM numbering.
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create a PWM instance on the servo pin at 50Hz (typical for servos)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)  # Start with a duty cycle of 0

def set_angle(angle):
    """
    Move the servo to the specified angle.
    
    For many servos:
      - 0° corresponds to ~2.5% duty cycle,
      - 90° to ~7.5% duty cycle,
      - 180° to ~12.5% duty cycle.
      
    Adjust the conversion below if needed.
    """
    duty_cycle = (angle / 18.0) + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Give the servo time to move
    pwm.ChangeDutyCycle(0)  # Stop sending the signal to prevent jitter

try:
    while True:
        print("Moving to 0°")
        set_angle(0)
        time.sleep(1)
        
        print("Moving to 90°")
        set_angle(90)
        time.sleep(1)
        
        print("Moving to 180°")
        set_angle(180)
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Exiting program...")

# Cleanup the GPIO and stop PWM
pwm.stop()
GPIO.cleanup()
