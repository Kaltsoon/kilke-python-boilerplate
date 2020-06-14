import os
import json
from run_pump import run_pump

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../nemo/pump_config.json')

def update_pump_config(pump, config):
  data = {}

  with open(filename, 'r+') as f:
    try:
      data = json.loads(f.read())
    except:
      data = {}
    
    data[pump] = config
    f.seek(0)
    f.write(json.dumps(data))
    f.truncate()
  