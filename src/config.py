from dotenv import load_dotenv
from pathlib import Path
import os

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))
except:
    pass

SYSTEM_ID = os.getenv('SYSTEM_ID')
SYSTEM_IO_PORT = os.getenv('SYSTEM_IO_PORT')
SYSTEM_IO_HOST = os.getenv('SYSTEM_IO_HOST')
API_URL = os.getenv('API_URL')


def get_error_message(variable_name):
    return '%s is not defined. Either define it in the .env file or as and environment variable' % variable_name


if (SYSTEM_ID == None):
    raise Exception(get_error_message('SYSTEM_ID'))

if (SYSTEM_IO_HOST == None):
    raise Exception(get_error_message('SYSTEM_IO_HOST'))

if (SYSTEM_IO_PORT == None):
    raise Exception(get_error_message('SYSTEM_IO_PORT'))
