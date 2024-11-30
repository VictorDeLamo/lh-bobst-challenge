import RPi.GPIO as GPIO
import time

# PINS
SERVO_PIN = 16
TRIG_PIN = 17
ECHO_PIN  = 27

# SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Define PWM for ServoMotor
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def measure_distance():
    # 10µs pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Wait for ECHO pulse
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    # Calculate pulse duration
    lapse = pulse_end - pulse_start
    # Calculate distance in cm
    distance = lapse * 34300 / 2  # Sound speed: 343 m/s
    return distance

try:
    print("Servo is running continuously. Press Ctrl+C to stop.")
    while True:
        # Update servo
        pwm.ChangeDutyCycle(10)
        time.sleep(0.001)

        # Measure distance
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping the servo.")
    pwm.ChangeDutyCycle(0)
    time.sleep(1)
finally:
    pwm.stop()
    GPIO.cleanup()
