from os import getenv
from dotenv import (load_dotenv, find_dotenv)
from pathlib import Path

# env_path = Path('.') / '.env'

load_dotenv(find_dotenv())  # dotenv_path=env_path

# flask
SECRET_KEY = getenv('SECRET_KEY')
WTF_CSRF_SECRET_KEY = getenv('WTF_CSRF_SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

# database
SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')

# line bot
CHANNEL_ID = getenv('CHANNEL_ID')
CHANNEL_SECRET = getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = getenv('CHANNEL_ACCESS_TOKEN')

# imgur
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
REFRESH_TOKEN = getenv('REFRESH_TOKEN')
