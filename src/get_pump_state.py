import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/pump_state.json')

def get_pump_state():
  data = {}

  with open(filename, 'r') as f:
    try:
      data = json.loads(f.read())
    except:
      data = {}
    
  return data
