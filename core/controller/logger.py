import os
import logging
from config import BASE_DIR
import traceback
from functools import wraps


# appdata_path = os.getenv('APPDATA')
# logs_dir = os.path.join(appdata_path, 'Chat')

# os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(BASE_DIR, 'logs.log')

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%DD/%mm/%Y %H:%M:%S'
)

#logs sincronos
def log(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            result = fun(*args, **kwargs)
            logging.info(f"Funcion {fun.__name__} completada. Retornó: {result}")
            return result
        except Exception as e:
            logging.error(f"Error en {fun.__name__}:\n{e}")
            raise
    
    return wrapper


#logs asincronos
def async_log(fun):
    @wraps(fun)
    async def wrapper(*args, **kwargs):
        try:
            result = await fun(*args, **kwargs)
            logging.info(f"Funcion {fun.__name__} completada. Retornó: {result}")
            return result
        except Exception as e:
            logging.error(f"Error en {fun.__name__}:\n{e}")
            raise
    
    return wrapper