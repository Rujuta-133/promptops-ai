from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os 

load_dotenv()

db_name = os.getenv('POSTGRES_DB')
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

if db_name is None or db_username is None or db_password is None:
    raise ValueError("Specify all the database config values")

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=db_username,
    password=db_password,
    host='localhost',
    port=5432,
    database=db_name
)

engine = create_engine(database_url)