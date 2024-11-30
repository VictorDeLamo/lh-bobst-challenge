from azure.iot.device import IoTHubDeviceClient, Message
import datetime
import json
import time

# Configuration
CONNECTION_STRING = 'HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI3;SharedAccessKey=wALbROiWbQnS3jd7/PtmQXEBAUqKu0iStAIoTMC95ps='
MACHINE_ID = 'lauzhack-pi3'


class IoTDevice:
    def __init__(self, connection_string, machine_id):
        self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self.machine_id = machine_id
        
    def send_telemetry(self, speed, output, energy):
        telemetry_data = {
            "telemetry": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "datasource": "10.0.4.4:80",
                "machineid": self.machine_id,
                "totaloutputunitcount": output,
                "machineSpeed": speed,
                "totalworkingenergy": energy
            }
        }
        telemetry_json = json.dumps(telemetry_data)
        message = Message(telemetry_json)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "Telemetry"

        try:
            self.client.send_message(message)
            print(f"Telemetry sent: {telemetry_json}")
        except Exception as e:
            print(f"Failed to send telemetry: {e}")

    def send_event(self, event_data, event_type):
        try:
            event_json = json.dumps(event_data)
            message = Message(event_json)
            message.content_type = "application/json"
            message.content_encoding = "utf-8"
            message.custom_properties["messageType"] = event_type

            self.client.send_message(message)
            print(f"{event_type} sent: {event_json}")
        except Exception as e:
            print(f"Failed to send {event_type}: {e}")

    def start_producing(self, job_id, job_input_unit_count, job_output_unit_count, total_production_time, total_working_energy):
        event_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "startProducing",
            "jobId": job_id,
            "jobInputUnitCount": job_input_unit_count,
            "jobOutputUnitCount": job_output_unit_count,
            "totalProductionTime": total_production_time,
            "totalWorkingEnergy": total_working_energy
        }
        self.send_event(event_data, "startProducing")

    def stop_producing(self, job_id, job_input_unit_count, job_output_unit_count, total_production_time, total_working_energy, fault, category, location, originator):
        event_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "stopProducing",
            "jobId": job_id,
            "jobInputUnitCount": job_input_unit_count,
            "jobOutputUnitCount": job_output_unit_count,
            "totalProductionTime": total_production_time,
            "totalWorkingEnergy": total_working_energy,
            "fault": fault,
            "category": category,
            "location": location,
            "originator": originator
        }
        self.send_event(event_data, "stopProducing")


# Test the functionality
def test_start_producing(device):
    job_id = "job-12345"
    job_input_unit_count = 1000
    job_output_unit_count = 950
    total_production_time = 3600  # seconds
    total_working_energy = 50000  # energy units

    device.start_producing(job_id, job_input_unit_count, job_output_unit_count, total_production_time, total_working_energy)


def test_stop_producing(device):
    job_id = "job-12345"
    job_input_unit_count = 1000
    job_output_unit_count = 950
    total_production_time = 3600  # seconds
    total_working_energy = 50000  # energy units
    fault = "Unexpected shutdown"
    category = "MechanicalFailure"
    location = 101  # machine or station ID
    originator = "Operator-001"

    device.stop_producing(job_id, job_input_unit_count, job_output_unit_count, total_production_time, total_working_energy, fault, category, location, originator)

def test_telemetry(device):
    output = 150
    speed = 500
    energy = 10000
    for i in range(1, 50):
        device.send_telemetry(speed, output, energy)
        speed += 10
        output += 3
        energy += 250

# Create an instance of the IoTDevice class
iot_device = IoTDevice(CONNECTION_STRING, MACHINE_ID)

# Simulate events
test_start_producing(iot_device)
time.sleep(2)  # Simulate some production time
test_stop_producing(iot_device)

# Test telemetry
test_telemetry(iot_device)
