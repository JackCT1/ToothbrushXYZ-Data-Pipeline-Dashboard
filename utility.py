from datetime import datetime
from datetime import timedelta

import pandas as pd


class Utility:
    """
    Helper class for utility functions.
    """
    @staticmethod
    def make_snake_case(string:str) -> str:
        """
        Converts string to snakecase format (converts spaces to underscores and upper case to lower case)
        """
        updated_string = string.replace(' ','_').lower()
        return updated_string

    @staticmethod
    def format_postcode(postcode:str) -> str:
        """
        Takes a postcode and removes spaces and converts entirely to uppercase.
        """
        updated_postcode = postcode.replace('%20','').replace(' ','').upper()
        return updated_postcode
    
    @staticmethod
    def format_date(number:int) -> str:
        """
        Format a singular digit number into the form '0x' for csv format.
        """
        if number < 10:
            return '0'+str(number)
        else:
            return str(number)
    
    @staticmethod
    def get_readable_date(date:datetime) -> str:
        """
        Returns the contents of a datetime object as 'yyyy/mm/dd'.
        """
        readable_date_list = [str(date.year),Utility.format_date(date.month),Utility.format_date(date.day)]
        readable_date = '_'.join(readable_date_list)
        return readable_date
    
    @staticmethod
    def convert_to_datetime(series:pd.Series) -> pd.Series:
        """
        Converts elements of a pandas series into datetime objects
        """
        return pd.to_datetime(series, errors='coerce')

    @staticmethod
    def get_today_datetime():
        """
        Returns current datetime
        """
        return datetime.today()

    @staticmethod
    def get_yesterdays_final_datetime():
        """
        Returns final datetime of previous day
        """
        yesterday = datetime.today() - timedelta(1)
        return datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 999999)