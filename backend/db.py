from dotenv import load_dotenv
from sqlalchemy import create_engine
from psycopg2 import connect
import os

load_dotenv()

protocol = os.getenv('DB_PROTOCOL')
databaseConfig = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

databaseURL = '{protocol}://{user}:{password}@{host}:{port}/{database}'.format(protocol=protocol, **databaseConfig)

print(databaseURL)
engine = create_engine(databaseURL)
conn = connect(**databaseConfig)
