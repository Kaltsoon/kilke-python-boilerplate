import json
import logging

from run_pump import run_pump

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/pump_rpm.json')

def initialize_pumps(on_ack, on_fault):
  with open(filename, 'r') as f:
    data = {}

    try:
      data = json.loads(f.read())
    except:
      data = {}
    
    logging.info(f'Initializing pumps with data {data}')

    for type in data: 
      rpm = data[type]
      result = run_pump(type, rpm)
      
      if result == '':
        on_ack(type, rpm)
      else:
        on_fault(type)

