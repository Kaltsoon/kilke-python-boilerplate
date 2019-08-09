from socketclusterclient import Socketcluster
import logging
import json
from read_sensors import read_sensors
from pump_configuration import handle_pump_configuration
import threading
from dotenv import load_dotenv
from pathlib import Path
from config import SYSTEM_ID, SYSTEM_IO_HOST, SYSTEM_IO_PORT

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

INPUT_CHANNEL = f'input.{SYSTEM_ID}'
OUTPUT_CHANNEL = 'output'

socket = None

logging.info(f'Using system id {SYSTEM_ID}')

def create_message(type, payload):
  return json.dumps({ 'systemId': SYSTEM_ID, 'type': type, 'payload': payload })

def on_pump_ack(pumpId, rpm):
  socket.publish(OUTPUT_CHANNEL, create_message('pump_fault', { 'pumpId': pumpId, 'data': rpm }))

def on_pump_fault(pumpId):
  socket.publish(OUTPUT_CHANNEL, create_message('pump_ack', { 'pumpId': pumpId }))

def on_sensor_measurement(measurements):
  logging.info(f'Sending measurement {measurements}')
  socket.publish(OUTPUT_CHANNEL, create_message('measurement', measurements))

def input_message(key, message):
  logging.info('Received a message from system-io')
  message = json.loads(message)
  messagePayload = message['payload']
  messageType = message['type']

  if (messageType == 'pump_configuration'):
    handle_pump_configuration(payload, on_pump_ack, on_pump_fault)

def sensor_reader_worker(on_measurement):
  read_sensors(on_measurement)

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
    socket.onchannel(INPUT_CHANNEL, input_message)

    sensorReaderThread = threading.Thread(target = sensor_reader_worker, args = [on_sensor_measurement])
    sensorReaderThread.start()
    
if __name__ == '__main__':
    socket = Socketcluster.socket(f'ws://{SYSTEM_IO_HOST}:{SYSTEM_IO_PORT}/socketcluster/') 
    socket.setBasicListener(on_connect, on_disconnect, on_connect_error)
    socket.setAuthenticationListener(on_set_authentication, on_authentication)
    socket.connect()

