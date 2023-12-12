import pyodbc
import time
import pandas as pd
import pymysql
import time
import datetime

from Constants import VIEW_TABLE, VIEW_TABLE_COLUMNS
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn

display = BuiltIn().log_to_console

class SQLServer(QRComponent):
    def __init__(self) -> None:
        self.server = ''
        self.database = ''
        self.cnxn: pyodbc.Connection
        self.cursor: pyodbc.Cursor
        # self.cnxn: sqlalchemy.Connection
        # self.cursor: sqlalchemy.Engine
        self.mysql_vault = {}
        self.min_value: float = 0.0

    def __get_credential(self) -> dict:
        vault: dict = QREnv.VAULTS['cbs']
        return vault
    
    # def get_mysql_credential(self) -> dict:
    #     vault: dict = QREnv.VAULTS['mysql_database']
    #     return vault

    def __enter__(self, *args, **kwargs):
        logger = self.run_item.logger
        vault = self.__get_credential()
        server = str(vault['server'])
        database = str(vault['database'])
        username = str(vault['username'])
        password = str(vault['password'])
        port = str(vault['port'])
        # self.min_value = float(vault['min_value'])
        
        conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+f'{server}, {port};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=YES'
        # conn_str = f'mssql://{username}:{password}@{server}:{port}/{database}'
        self.conn_str = conn_str
        logger.info(f'conn_str = {conn_str}')
        logger.info('Connecting ms-sql database')
        self.cnxn = pyodbc.connect(conn_str)
        # BuiltIn().log_to_console('conn---------------------------------------------------')
        # self.cnxn = sqlalchemy.create_engine(url=conn_str).connect()
        logger.info('Connection to ms-sql database successful')
        self.cursor = self.cnxn.cursor()
        logger.info('Cursor object created.')
        return self
    
    def __exit__(self, *args, **kwargs):
        logger = self.run_item.logger
        logger.info('Closing connection to database.')
        self.cnxn.commit()
        self.cnxn.close()
        logger.info('Connection to ms-sql database closed.')
        if any(args):
            logger.error(f'Error : {args}')
            raise Exception(args)
        

class DatabaseViewTask(SQLServer):
    def __init__(self) -> None:
        super().__init__()

    def get_data_by_query_name(self, view_table: str) -> pd.DataFrame:
        '''
            view table value are keys form Constants.VIEW_TABLE
        '''
        start_time = time.time()
        # mysql_credential = self.get_mysql_credential()
        view_table = view_table.strip()
        if not view_table in VIEW_TABLE.keys():
            raise Exception('Incorrect view_table value')
        logger = self.run_item.logger
        query = f"select * from {VIEW_TABLE[view_table]}"
        logger.info('Query about name')
        df = pd.read_sql_query(query, self.cnxn) # type: ignore
        df.columns = df.columns.str.lower().str.strip()
        logger.info(f'Columns : {df.columns.to_list()}')
        display(f'Columns : {df.columns.to_list()}')
        logger.info(f'{view_table} shape is {df.shape}')
        return df
    
    def collect_all_view_table(self):
        run_item = self.run_item
        self.notify(run_item)

        logger = run_item.logger
        df_map = {}
        try:
            start_time_db = time.time()
            logger.info('gather client_table started')
            df_map['client_table'] = self.get_data_by_query_name('client_table')
            logger.info('client_table completed')
            display('gather client_table completed')

            logger.info('gather client_master started')
            display('gather client_master started')
            df_map['client_master'] = self.get_data_by_query_name('client_master')
            display(df_map['client_master'].keys())
            logger.info('gather client_master completed')
            display('gather client_master completed')

            finish_time = time.time()
            logger.info(f'Time required to get data from jump server is {int(finish_time - start_time_db)}')
            display(f'Time required to get data from jump server is {int(finish_time - start_time_db)}')
        except Exception as e:
            run_item.report_data['Task'] = 'Initial: Table Collection'
            run_item.report_data['Reason'] = 'Failed to read data from jump server (view).'
            run_item.set_error()
            run_item.post()
            raise e
        return df_map
