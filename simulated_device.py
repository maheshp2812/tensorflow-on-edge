import threading
import time
import random
import math
import pint
from liota.entities.metrics.metric import Metric
from liota.entities.devices.device import Device
from liota.lib.utilities.utility import systemUUID
from liota.device_comms.mqtt_device_comms import MqttDeviceComms

class SimulatedDevice(Device):

    def __init__(self, name, interval = 1):
        super(SimulatedDevice, self).__init__(
            name = name,
            entity_id = systemUUID().get_uuid(name),
            entity_type = "SimulatedDevice"
        )
        self.mqtt = MqttDeviceComms(url="test.mosquitto.org", port=1883, clean_session=True,conn_disconn_timeout=1000)
        print('Connection to broker established...')
        self.interval = interval
        self.randomVar = 0
        self.run()

    def run(self):
        self.th = threading.Thread(target = self.simulate)
        self.th.daemon = False
        self.th.start()

    def simulate(self):
        print('Simulation beginning...')
        while True:
            self.randomVar = random.randint(0,30)
            self.mqtt.publish("random_data", str(self.randomVar), qos = 2)
            print(self.randomVar)
            time.sleep(self.interval)

if __name__ == '__main__':
    simulated_model = SimulatedDevice('New_Device_Name')
