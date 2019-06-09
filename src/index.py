from socketclusterclient import Socketcluster
import logging
import os
import json
from read_sensors import readSensors
from pump_configuration import handlePumpConfiguration
import threading

SYSTEM_ID = os.getenv('SYSTEM_ID')
SYSTEM_IO_PORT = os.getenv('SYSTEM_IO_PORT')
SYSTEM_IO_HOST = os.getenv('SYSTEM_IO_HOST')
INPUT_CHANNEL = f'input.{SYSTEM_ID}'
OUTPUT_CHANNEL = 'output'

socket = None

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def createMessage(type, payload):
  return json.dumps({ 'systemId': SYSTEM_ID, 'type': type, 'payload': payload })

def onPumpAck(pumpId, rpm):
  socket.publish(OUTPUT_CHANNEL, createMessage('pump_fault', { 'pumpId': pumpId, 'data': rpm }))

def onPumpFault(pumpId):
  socket.publish(OUTPUT_CHANNEL, createMessage('pump_ack', { 'pumpId': pumpId }))

def onSensorMeasurement(measurements):
  logging.info(f'Sending measurement {measurements}')
  socket.publish(OUTPUT_CHANNEL, createMessage('measurement', measurements))

def inputMessage(key, message):
  logging.info('Received a message from system-io')
  message = json.loads(message)
  messagePayload = message['payload']
  messageType = payload['type']

  if (messageType == 'pump_configuration'):
    handlePumpConfiguration(payload, onPumpAck, onPumpFault)

def sensorReaderWorker(onMeasurement):
  readSensors(onMeasurement)

def onConnect(socket):
    logging.info('Connected to system-io')


def onDisconnect(socket):
    logging.info('Disconnected from system-io')


def onConnectError(socket, error):
    logging.info('Connection error with system-io')


def onSetAuthentication(socket, token):
    socket.setAuthtoken(token)


def onAuthentication(socket, isAuthenticated):
    logging.info('Authenticated to system-io')
    socket.subscribe(INPUT_CHANNEL)
    socket.onchannel(INPUT_CHANNEL, inputMessage)

    sensorReaderThread = threading.Thread(target = sensorReaderWorker, args = [onSensorMeasurement])
    sensorReaderThread.start()
    
if __name__ == '__main__':
    socket = Socketcluster.socket(f'ws://{SYSTEM_IO_HOST}:{SYSTEM_IO_PORT}/socketcluster/') 
    socket.setBasicListener(onConnect, onDisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.connect()

