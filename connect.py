import sys
import configparser
from mongoengine import connect

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

user = config.get('DB', 'USER')
passw = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
db = config.get('DB', 'DB_NAME')

conn_str = f"""mongodb+srv://{user}:{passw}@{domain}/{db}?retryWrites=true&w=majority"""

try:
    connect(host=conn_str, ssl=True)
    print("Connected to MongoDB")
except Exception as e:  # noqa
    print(f"Error: {e}")
    print("Connection failed")
    sys.exit(1)
