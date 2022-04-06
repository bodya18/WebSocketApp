import os
from dotenv import load_dotenv
load_dotenv()

mysql_conf = os.getenv('MYSQL')

ROOT_DIR = os.getcwd()

STATUS_LIST = ["Actived", "Disabled", "Banned"]