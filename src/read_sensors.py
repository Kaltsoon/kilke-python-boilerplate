import time
import random

def readSensors(onMeasurement):
   while True:
    onMeasurement({
        'type': 'sensor',
        'time': int(round(time.time(), 0)),
        'data': {
            'cond': round(random.random() * 10, 2),
            'tco': round(random.random() * 10, 2),
            'phd': round(random.random() * 10, 2),
            'phf': round(random.random() * 10, 2),
            'wd': round(random.random() * 10, 2),
            'wf': round(random.random() * 10, 2),
            'tamb': round(random.random() * 10, 2)
        }
    })
    
    time.sleep(4)