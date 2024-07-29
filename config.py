import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///game_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('REGION')


required_env_vars = ['ACCESS_KEY_ID', 'SECRET_ACCESS_KEY', 'REGION']
for var in required_env_vars:
    if not os.environ.get(var):
        raise EnvironmentError(f"Required environment variable {var} is not set.")