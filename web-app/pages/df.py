import os

from dotenv import load_dotenv
from sqlwrapper import Sqlwrapper

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

sql = Sqlwrapper(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

df = sql.read_query("""
    SELECT *
    FROM week4_jack_production.production_ecommerce
""")