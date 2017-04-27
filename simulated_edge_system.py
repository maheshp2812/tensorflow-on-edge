import time
import math
import pint
from liota.dcc_comms.socket_comms import SocketDccComms
from liota.dccs.graphite import Graphite
from liota.entities.metrics.metric import Metric
from liota.entities.edge_systems.dell5k_edge_system import Dell5KEdgeSystem
from liota.device_comms.mqtt_device_comms import MqttDeviceComms

sum = ""

def random_function():
    global sum
    temp = sum
    sum = 0
    return temp

def on_message(client, data, msg):
    global sum
    print(msg.payload)
    sum += int(msg.payload)

# getting values from conf file
config = {}
execfile('sampleProp.conf', config)

if __name__ == '__main__':
    edge_system = Dell5KEdgeSystem(config['EdgeSystemName'])
    graphite = Graphite(SocketDccComms(ip = config['GraphiteIP'], port = config['GraphitePort']))
    graphite_reg_dev = graphite.register(edge_system)
    mqtt = MqttDeviceComms(url = "test.mosquitto.org", port = 1883, clean_session=True,conn_disconn_timeout=1000)
    print('Connection to broker established...')
    mqtt.subscribe("random_data", callback = on_message, qos = 2)
    print('Subscribed to random_data')
    metric_name = "model.device_data"
    random_metric = Metric(
        name = metric_name,
        interval = 5,
        sampling_function = random_function
    )
    reg_metric = graphite.register(random_metric)
    graphite.create_relationship(graphite_reg_dev, reg_metric)
    reg_metric.start_collecting()
