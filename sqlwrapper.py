from datetime import datetime

import pandas as pd
import sqlalchemy


class Sqlwrapper:
    def __init__(self,username:str,password:str,host:str,port:str,db_name:str):
        engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@{host}:{port}/{db_name}")
        self.engine = engine
    
    def read_query(self,query:str) -> pd.DataFrame:
        """
        Executes a query on a table and returns a pandas dataframe.
        """
        con = self.engine.connect()
        results = con.execute(query)
        returns =  results.fetchall()
        con.close()
        return pd.DataFrame(returns)
    
    def drop_table(self,table_name:str,schema_name:str) -> str:
        """
        Drops specified table from database.
        """
        con = self.engine.connect()
        con.execute(f"""
        DROP TABLE IF EXISTS {schema_name}.{table_name};
        """)
        con.close()
        return "Table dropped successfully"

    def write_df_to_table(self,data:pd.DataFrame,schema_name:str,table_name:str = None) -> str:
        """
        Writes a pandas dataframe to a postgresql table.
        """

        if table_name == None:
            table_name = Sqlwrapper.get_readable_date(datetime.now())

        self.drop_table(table_name,schema_name)
        data.to_sql(table_name,self.engine,schema = schema_name,index = False)
        return "Table successfully added to schema"