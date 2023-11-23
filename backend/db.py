from dotenv import load_dotenv
from sqlalchemy import create_engine
from psycopg2 import connect
import os

protocol = "postgresql"
host = "localhost" 
port = 5432  
user = "docassist"
password = "aakashchaitanya"
database = "medicine"

databaseConfig = {
    'host': host,
    'port': port,
    'user': user,
    'password': password,
    'database': database,
}



databaseURL = '{protocol}://{user}:{password}@{host}:{port}/{database}'.format(protocol=protocol, **databaseConfig)

print(databaseURL)
engine = create_engine(databaseURL)
conn = connect(**databaseConfig)
