import os
import json
from run_pump import run_pump

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/pump_rpm.json')

def persisted_run_pump(pump, rpm):
  data = {}

  with open(filename, 'r+') as f:
    try:
      data = json.loads(f.read())
    except:
      data = {}
    
    result = run_pump(pump, rpm)
  
    if result != '':
      data[pump] = rpm
      f.seek(0)
      f.write(json.dumps(data))
      f.truncate()

    f.close()
    

  
  
  
