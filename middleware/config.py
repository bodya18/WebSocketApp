import os
from dotenv import load_dotenv
load_dotenv()

mysql_conf = os.getenv('MYSQL')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

ROOT_DIR = os.getcwd()

STATUS_LIST = ["Actived", "Disabled", "Banned"]