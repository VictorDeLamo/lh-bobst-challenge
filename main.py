import RPi.GPIO as GPIO
from ina219 import INA219, DeviceRangeError
from azure.iot.device import IoTHubDeviceClient, Message
import time, datetime, json
from flask import Flask, jsonify, request
import threading

# VARS
boxes = 0
currentPower = 0
speed = 0
dutyCycle = 12
start_time = time.time()
total_seconds = 0
watts = 1.0
servo_direction = "forward" 
read_boxes = True

# CONST
SERVO_PIN = 16
TRIG_PIN = 17
ECHO_PIN  = 27
LINEAL_PIN = 12
SHUNT_OMHS = 0.1
CONNECTION_STRING = 'HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI3;SharedAccessKey=wALbROiWbQnS3jd7/PtmQXEBAUqKu0iStAIoTMC95ps='
MACHINE_ID = 'lauzhack-pi3'
MACHINE_IP = '10.0.4.4:80'
FW_TO_RV = {
    12: 2,
    11: 3,
    10: 4,
    9: 5,
    8: 7,
}
RV_TO_FW = {
    2: 12,
    3: 11,
    4: 10,
    5: 9,
    7: 8,
}

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

def update_stats():
    global start_time, speed, total_seconds, watts, boxes
    current_time = time.time()
    if current_time - start_time >= 1:
        total_seconds +=1
        watts += ina.power() / 1000 
        speed = boxes/total_seconds
        start_time = current_time
        send_telemetry()
        

def update_boxes():
    global sensor_bool, boxes, read_boxes
    sensor_bool = GPIO.input(LINEAL_PIN)
    if sensor_bool == 0 and read_boxes == 1:
        boxes += 1
        read_boxes = 0
    elif sensor_bool == 1 and read_boxes == 0:
         read_boxes = 1

def send_telemetry():
        global boxes, speed, watts
        telemetry_data = {
            "telemetry": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "datasource": MACHINE_IP,
                "machineid": MACHINE_ID,
                "totaloutputunitcount": boxes,
                "machinespeed": speed,
                "totalworkingenergy": watts
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

# API   
app = Flask(__name__)

@app.route("/start", methods=["POST"])
def start_servo():
    global dutyCycle
    dutyCycle = 12
    return jsonify({"status": "Servo motor started"}), 200

@app.route("/stop", methods=["POST"])
def stop_servo():
    global dutyCycle
    dutyCycle = 0
    return jsonify({"status": "Servo motor stopped"}), 200

@app.route("/forward", methods=["POST"])
def set_forward():
    global dutyCycle, servo_direction
    if servo_direction == "reverse" and dutyCycle != 0:
        dutyCycle = RV_TO_FW.get(dutyCycle, None)
        servo_direction = "forward"
      
    return jsonify({"status": "Direction set to forward", "speed": dutyCycle}), 200

@app.route("/reverse", methods=["POST"])
def set_reverse():
    global dutyCycle, servo_direction
    if servo_direction == "forward" and dutyCycle != 0:
        dutyCycle = FW_TO_RV.get(dutyCycle, None)
        servo_direction = "reverse"
    return jsonify({"status": "Direction set to reverse", "speed": dutyCycle}), 200

@app.route("/fast", methods=["POST"])
def fast_servo():
    global dutyCycle, servo_direction
    if servo_direction == "forward" and dutyCycle < 12:
        dutyCycle += 1 
    elif servo_direction == "reverse" and dutyCycle > 2:
        dutyCycle -= 1
    else:
        return jsonify({"error": "Cannot increase speed beyond maximum"}), 400

    return jsonify({"status": "Speed increased", "speed": dutyCycle}), 200

@app.route("/slow", methods=["POST"])
def slow_servo():
    global dutyCycle, servo_direction
    if servo_direction == "forward" and dutyCycle > 8:
        dutyCycle -= 1 
    elif servo_direction == "reverse" and dutyCycle < 7:
        dutyCycle += 1
    else:
        return jsonify({"error": "Cannot decrease speed beyond minimum"}), 400

    return jsonify({"status": "Speed decreased", "speed": dutyCycle}), 200

def main(): 
    try:
        print("Servo is running continuously. Press Ctrl+C to stop.")
        while True:
            servo_motor()
            update_boxes()
            update_stats()
            #send_telemetry()

    except KeyboardInterrupt:
        print("\nStopping the servo.")
        pwm.ChangeDutyCycle(0)
        time.sleep(1)

    finally:
        pwm.stop()
        GPIO.cleanup()
        client.shutdown()

def start_api():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    api_thread = threading.Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()

    main()
