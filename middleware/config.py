import os
from dotenv import load_dotenv
import datetime
import logging

load_dotenv()
mysql_conf = os.getenv('MYSQL')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ROOT_DIR = os.getcwd()

STATUS_LIST = ["Actived", "Disabled", "Banned"]


def get_logger(name=__file__, file=f"logs/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.log", encoding='utf-8'):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').disabled = True

    logging.getLogger('engineio.server').disabled = True

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log

log = get_logger()