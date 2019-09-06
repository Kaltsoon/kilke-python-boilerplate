import json

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/reactor_state.json')

def get_reactor_state():
  data = {}

  with open(filename, 'r') as f:
    try:
      data = json.loads(f.read())
    except:
      data = {}
    
  return data
