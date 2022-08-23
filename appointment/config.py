import os
from dotenv import load_dotenv


base_dir = os.getcwd()
print(f"dffdfd {base_dir}")
load_dotenv(dotenv_path=f'{str(base_dir).replace("/app","")}/.env.dev')


class Config: 
    """Base configuration"""
    DATABASE_URL = os.getenv('DATABASE_URL')

