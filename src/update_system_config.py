import os
import json
from run_pump import run_pump

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../nemo/system_config.json')


def update_system_config(config):
    with open(filename, 'w') as f:
        f.seek(0)
        f.write(json.dumps(config))
        f.truncate()
        f.close()
