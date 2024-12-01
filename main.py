import RPi.GPIO as GPIO
from ina219 import INA219, DeviceRangeError
from azure.iot.device import IoTHubDeviceClient, Message
import time, datetime, json

# VARS
boxes = 0
currentPower = 0
speed = 0
dutyCycle = 12
start_time = time.time()
total_seconds = 0
mwatts = 1.0

# CONST
SERVO_PIN = 16
TRIG_PIN = 17
ECHO_PIN  = 27
LINEAL_PIN = 12
SHUNT_OMHS = 0.1
CONNECTION_STRING = 'HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI3;SharedAccessKey=wALbROiWbQnS3jd7/PtmQXEBAUqKu0iStAIoTMC95ps='
MACHINE_ID = 'lauzhack-pi3'
MACHINE_IP = '10.0.4.4:80'

# SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LINEAL_PIN, GPIO.IN)

ina = INA219(shunt_ohms=SHUNT_OMHS, busnum=1)
ina.configure(
    voltage_range=ina.RANGE_16V,
    gain=ina.GAIN_AUTO,
    bus_adc=ina.ADC_128SAMP,
    shunt_adc=ina.ADC_128SAMP
)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def servo_motor():
    global pwm
    pwm.ChangeDutyCycle(dutyCycle)
    time.sleep(0.001)

def power():
    global mwatts
    mwatts += ina.power()
    time.sleep(1)

def update_speed():
    global current_time, start_time, speed, total_seconds
    current_time = time.time()
    if current_time - start_time >= 1:
        total_seconds +=1
        speed = boxes/total_seconds
        start_time = current_time

def update_boxes():
    global sensor_bool, boxes
    sensor_bool = GPIO.input(LINEAL_PIN)
    if sensor_bool == 0:
        boxes = boxes + 1

def send_telemetry():
        global boxes, speed, mwatts
        telemetry_data = {
            "telemetry": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "datasource": MACHINE_IP,
                "machineid": MACHINE_ID,
                "totaloutputunitcount": boxes,
                "machinespeed": speed,
                "totalworkingenergy": mwatts
            }
        }
        telemetry_json = json.dumps(telemetry_data)
        message = Message(telemetry_json)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "Telemetry"

        try:
            client.send_message(message)
            print(f"Telemetry sent: {telemetry_json}")
        except Exception as e:
            print(f"Failed to send telemetry: {e}")

def main(): 
    try:
        print("Servo is running continuously. Press Ctrl+C to stop.")
        servo_motor()
        while True:
            power()
            update_boxes()
            update_speed()
            send_telemetry()

    except KeyboardInterrupt:
        print("\nStopping the servo.")
        pwm.ChangeDutyCycle(0)
        time.sleep(1)

    finally:
        pwm.stop()
        GPIO.cleanup()
        client.shutdown()

if __name__ == "__main__":
        main()
