import sqlite3
from datetime import datetime
import nepali_datetime

import Constants
from qrlib.QRUtils import display
from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv 

class AccuityDbComponent(QRComponent):
    def __init__(self) -> None:
        self.con = None
        self.cur = None
        
    def connect(self):
        self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
        self.cur = self.con.cursor()

    def insert_accuity_data(self,df):
        self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
        self.cur = self.con.cursor()
        df.to_sql(
            Constants.ACCUITY_TABLE_NAME,
            self.con,
            if_exists='append',
            index=False
            )
        display('SUCCESSFULLY INSERTED DATA TO ACUITY TABLE')

    def create_date_table(self):
        self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS DATE_TABLE (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         date TEXT,
                         file_name TEXT
            )
         ''')
        self.con.commit()
        self.con.close()
        
    def insert_into_date_table(self,date,file_name):
        self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
        self.cur = self.con.cursor()
        values = (date,file_name)
        insert_query = 'INSERT INTO DATE_TABLE (date,file_name) VALUES (?,?)'

        self.cur.execute(insert_query,values)

        self.con.commit()
        self.con.close()

    def get_data_with_status(self, status: str) -> list:

        query = f'''
        select name, dobs, countryName,OriginalSource, SubCategory, title, Gender,Status from  {Constants.ACCUITY_TABLE_NAME}
        where status = '{status}'
    '''
        logger = self.run_item.logger
        self.con.row_factory = sqlite3.Row
        logger.info(f'Reading data having status {status} from table  {Constants.ACCUITY_TABLE_NAME}')
        data = self.con.execute(query).fetchall()
        if data:
            logger.info(f'All database data retrivied.')
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            # temp_value.to_excel('test_data_cib.xlsx',index=False)
            return temp_value
        else:
            return []
    
    def get_date_from_date_table(self,file_name):
        self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(f'''
        SELECT date FROM DATE_TABLE
        WHERE file_name = ?
        ''',(file_name,))
        #feth the rows
        rows = self.cur.fetchall()
        for row in rows:
            
            display(f'Row data is {row}')
            # display(row[0])
            return row[0]
        # cur.execute(f'Delete date FROM DATE_TABLE where id = 1')
        self.con.commit()
        self.con.close()
        display('Successfully extract the institutional pending data')
    # def insert_or_get_date(self):
    #     self.con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
    #     self.cur = self.con.cursor()
    #     self.cur.execute('''
    #         SELECT date FROM DATE_TABLE WHERE file_name = 'first'
    #         )
    #      ''')
    #     self.con.commit()
    #     self.con.close()

