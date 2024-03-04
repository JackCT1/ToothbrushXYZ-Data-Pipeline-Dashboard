import os

from dotenv import load_dotenv
import pandas as pd

from sqlwrapper import Sqlwrapper
from utility import Utility

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

sql = Sqlwrapper(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

staging_df = sql.read_query("""
SELECT *
FROM week4_jack_staging.staging_ecommerce
""")

def snake_case_column_names(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Converts dataframes column names to snake case.
        """
        staging_df.columns = [Utility.make_snake_case(column_name) for column_name in staging_df.columns]
        return staging_df

def format_column_postcode(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Formats all postcodes for easy analysis.
        """
        staging_df['delivery_postcode'] = staging_df['delivery_postcode'].apply(Utility.format_postcode)
        staging_df['billing_postcode'] = staging_df['billing_postcode'].apply(Utility.format_postcode)
        return staging_df