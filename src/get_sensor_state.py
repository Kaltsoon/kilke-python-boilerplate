import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../nemo/sensor_state.json')

def get_sensor_state():
  data = {}

  with open(filename, 'r') as f:
    try:
      data = json.loads(f.read())
    except:
      data = {}
    
  return data
