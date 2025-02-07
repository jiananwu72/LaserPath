import RPi.GPIO as GPIO
import time
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create a PWM instance on the servo pin
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

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

# Clean up
pwm.stop()
GPIO.cleanup()
