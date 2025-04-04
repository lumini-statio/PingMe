import os
import logging
from config import BASE_DIR
from datetime import datetime


# appdata_path = os.getenv('APPDATA')
# logs_dir = os.path.join(appdata_path, 'Chat')

# os.makedirs(logs_dir, exist_ok=True)

logs_dir = os.path.join(BASE_DIR, 'Chat')

log_file = os.path.join(logs_dir, 'logs.log')

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%DD/%mm/%Y %H:%M:%S'
)


def log(fun):
    def wrapper(*args, **kwargs):
        logging.info(fun(*args, **kwargs))
    
    return wrapper