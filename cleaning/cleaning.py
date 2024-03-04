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

def remove_negative_age(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Removes rows with negative ages from the dataframe.
        """
        staging_df = staging_df.query('customer_age > 0')
        return staging_df

def format_is_first(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Checks that is_first is either 0 or 1, if not then removes those rows.
        """
        staging_df = staging_df.query('is_first == 0 or is_first == 1')
        return staging_df

def get_positive_order_quantities(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Returns the rows with positive order quantities.
        """
        staging_df = staging_df.query('order_quantity > 0')
        return staging_df

def change_columns_to_datetime(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Change columns' datatype to datetime.
        """
        staging_df['delivery_date'] = Utility.convert_to_datetime(staging_df['delivery_date'])
        staging_df['order_date'] = Utility.convert_to_datetime(staging_df['order_date'])
        staging_df['dispatched_date'] = Utility.convert_to_datetime(staging_df['dispatched_date'])
        return staging_df

def get_correct_timings(staging_df:pd.DataFrame) -> pd.DataFrame:
        """
        Returns rows that satisfy: ORDER DATE < DISPATCH DATE < DELIVERY DATE.
        """
        correct_timing_order_dispatched = staging_df['order_date'] < staging_df['dispatched_date'] 
        correct_timing_dispatched_delivered = staging_df['dispatched_date'] < staging_df['delivery_date']
        is_null = (staging_df['delivery_date'].isnull()) | (staging_df['dispatched_date'].isnull())

        timing_filter = correct_timing_dispatched_delivered | correct_timing_order_dispatched | is_null

        staging_df = staging_df[timing_filter]
        
        return staging_df

def handler(event,context):
        """
        Handler for Lambda function
        """
        print('Writing production table...')
        staging_df = snake_case_column_names(staging_df)
        staging_df = format_column_postcode(staging_df)
        staging_df = remove_negative_age(staging_df)
        staging_df = format_is_first(staging_df)
        staging_df = get_positive_order_quantities(staging_df)
        staging_df = change_columns_to_datetime(staging_df)
        production_df = get_correct_timings(staging_df)
        sql.write_df_to_table(
                production_df,
                schema_name='week4_jack_production',
                table_name='production_ecommerce')
        print('Success, production table written to database')