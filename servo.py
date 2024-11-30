import RPi.GPIO as GPIO
import time

SERVO_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

try:
    print("Servo is running continuously. Press Ctrl+C to stop.")
    while True:
        pwm.ChangeDutyCycle(10)
        time.sleep(0.001)
except KeyboardInterrupt:
    print("\nStopping the servo.")
    pwm.ChangeDutyCycle(0)
    time.sleep(1)
finally:
    pwm.stop()
    GPIO.cleanup()
