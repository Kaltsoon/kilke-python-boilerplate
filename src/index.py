import logging
import json
import threading
import time
from pathlib import Path
from socketclusterclient import Socketcluster

from config import SYSTEM_ID, SYSTEM_IO_HOST, SYSTEM_IO_PORT, API_URL
from api import ApiClient
from get_pump_state import get_pump_state
from get_sensor_state import get_sensor_state
from update_pump_config import update_pump_config
from update_system_config import update_system_config

apiClient = ApiClient(API_URL)
socket = None

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

INPUT_CHANNEL = 'input.%s' % SYSTEM_ID
OUTPUT_CHANNEL = 'output'
READ_STATE_INTERVAL = 5

logging.info('Using system id %s' % SYSTEM_ID)


def create_message(type, payload):
    return json.dumps({'systemId': SYSTEM_ID, 'type': type, 'payload': payload})


def publish_measurement(measurements):
    logging.info('Sending measurement %s' % measurements)
    socket.publish(OUTPUT_CHANNEL, create_message('measurement', measurements))


def handle_pump_configuration(payload):
    config = {
        'mode': payload['mode']
    }

    type = payload['type']

    if ('manualRpm' in payload):
        config['manrpm'] = payload['manualRpm']

    if ('automaticRpm' in payload):
        config['autorpm'] = payload['automaticRpm']

    update_pump_config(type, config)


def get_time_now():
    return int(round(time.time(), 0))


def handle_input_message(key, message):
    logging.info('Received a message from system-io')
    message = json.loads(message)
    message_payload = message['payload']
    message_type = message['type']

    if (message_type == 'pump_configuration'):
        handle_pump_configuration(message_payload)


def read_state_worker():
    while True:
        now = get_time_now()

        try:
            pump_state = get_pump_state()
            mtime = pump_state['time']

            logging.info('Pump state is %s' % pump_state)

            if (mtime > now - READ_STATE_INTERVAL):
                pump_measurement = {
                    'type': 'pump',
                    'time': mtime,
                    'data': pump_state['data']
                }

                publish_measurement(pump_measurement)
        except:
            logging.error('Failed to publish pump state')

        try:
            sensor_state = get_sensor_state()
            mtime = sensor_state['time']

            logging.info('Sensor state is %s' % sensor_state)

            if (mtime > now - READ_STATE_INTERVAL):
                sensor_measurements = {
                    'type': 'sensor',
                    'time': mtime,
                    'data': sensor_state['sen'],
                    'calibrated': True
                }

                publish_measurement(sensor_measurements)

                binary_sensor_measurements = {
                    'type': 'binary',
                    'time': mtime,
                    'data': sensor_state['bin']
                }

                publish_measurement(binary_sensor_measurements)
        except:
            logging.error('Failed to publish sensor state')

        time.sleep(READ_STATE_INTERVAL)


def sync_system_config_worker():
    while True:
        try:
            system = apiClient.get_system(SYSTEM_ID)

            config = {}

            if ('config' in system):
                config = system['config']

            update_system_config(config)
        except:
            logging.error('Failed to sync system config')

        time.sleep(10)


def on_connect(socket):
    logging.info('Connected to system-io')


def on_disconnect(socket):
    logging.info('Disconnected from system-io')


def on_connect_error(socket, error):
    logging.info('Connection error with system-io')


def on_set_authentication(socket, token):
    socket.setAuthtoken(token)


def on_authentication(socket, isAuthenticated):
    logging.info('Authenticated to system-io')
    socket.subscribe(INPUT_CHANNEL)
    socket.onchannel(INPUT_CHANNEL, handle_input_message)

    read_state_thread = threading.Thread(target=read_state_worker)
    read_state_thread.start()

    sync_system_config_thread = threading.Thread(
        target=sync_system_config_worker)
    sync_system_config_thread.start()


if __name__ == '__main__':
    socket = Socketcluster.socket(
        'ws://%s:%s/socketcluster/' % (SYSTEM_IO_HOST, SYSTEM_IO_PORT))
    socket.setBasicListener(on_connect, on_disconnect, on_connect_error)
    socket.setAuthenticationListener(on_set_authentication, on_authentication)
    socket.connect()
