from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import s3fs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlwrapper import Sqlwrapper
from utility import Utility

load_dotenv()
fs = s3fs.S3FileSystem()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
connection = engine.connect()
session = sessionmaker(bind=engine)

sql = Sqlwrapper(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

def read_data_from_s3(bucket_name:str, date:datetime = datetime.now() - timedelta(days=1)) -> pd.DataFrame:
    '''Retrieves yesterdays csv data from s3 and returns them in a pandas dataframe'''
    fs = s3fs.S3FileSystem()
    year = date.year
    month = date.month
    day = date.day
    directory_string = f'{bucket_name}/{year}/{Utility.format_date(month)}/{Utility.format_date(day)}'
    csv_list = fs.ls(directory_string)

    if len(csv_list) == 0:
        print('There is no data from yesterday.')
        return None

    db_list = [pd.read_csv(f's3://{csv_path}') for csv_path in csv_list if csv_path.endswith('.csv')]
    concatenated_db = pd.concat(db_list)
    print('Data received')
    return concatenated_db


def handler(event, context):
    ''' Handler for Lambda function'''
    df = read_data_from_s3('sigma-week4-ecommerce-data')
    print('Data read from s3')

    try:
        Sqlwrapper.write_df_to_table(
            df,
            schema_name='week4_jack_staging',
            table_name='staging_ecommerce')
        print('Data Written to Postgresql table')
    except:
        print('No data is available for yesterdays date.') 