import os
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv(dotenv_path='/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/supplier/.env.dev')

class Config: 
    DATABASE_URL = os.getenv('DATABASE_URL')

