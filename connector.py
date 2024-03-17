import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

database = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
port = os.getenv('DB_PORT')

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
session = Session(engine)
