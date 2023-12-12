import sqlite3
from datetime import datetime
import nepali_datetime

import Constants
from qrlib.QRUtils import display
from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv 


class DBComponent(QRComponent):
    def __init__(self) -> None:
        self.con = None
        self.cur = None
        
    def connect(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()

    def insert_first_run_data(self,df):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        df.to_sql(
            Constants.CIB_USER_TABLE_NAME,
            self.con,
            if_exists='append',
            index=False
            )
        display('SUCCESSFULLY INSERTED DATA TO THE DATABASE AT FIRST RUN')

    def create_individual_table(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(f''' 
                CREATE TABLE IF NOT EXISTS {Constants.REPORT} (
                'Branch Code' TEXT,
                'CBS Client Code' TEXT,
                'CBS Account Number' TEXT,
                'Account Description' TEXT,
                'CBS Account Status' TEXT,
                'CBS Account Name' TEXT,
                'Name Match %' TEXT,
                'CBS Father Name' TEXT,
                'Father Name %' TEXT,
                'CBS Date of birth(BS)' TEXT,
                'DOB Match %' TEXT,
                'CBS Citizenship No' TEXT,
                'Citizenship Match %' TEXT,
                'PAN NUMBER %' TEXT,
                'PASSPORT NUMBER %' TEXT,
                'Indian Embassy Reg No %' TEXT,
                'Total Similarity %' TEXT,
                'Result of CIB Screening' TEXT,
                'CIB Name' TEXT,
                'CIB Father Name' TEXT,
                'CIB DOB' TEXT,
                'CIB Citizenship No' TEXT,
                'CIB PAN No' TEXT,
                'CIB PASSPORT NO' TEXT,
                'CIB Indian Embassy NO' TEXT,
                'CIB Gender' TEXT,
                'CIB Black Listed No' TEXT,
                'CIB Black Listed Date' TEXT,
                'Driving Licence No' TEXT,
                'Indian Embassy Reg No' TEXT,
                'PAN No' TEXT,
                'Passport No' TEXT,
                'CBS Remarks' TEXT,
                'Delay_by_days' integer default 0,
                created_at DATETIME DEFAULT (datetime('now', 'localtime')), 
                updated_at DATETIME,
                'Status' TEXT
                )
            ''')
        self.con.commit()
        self.con.close()

    def create_institutional_table(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(f''' 
                CREATE TABLE IF NOT EXISTS {Constants.REPORT_INSTITUTE} (
                'Branch Code' TEXT,
                'CBS Client Code' TEXT,
                'CBS Account Number' TEXT,
                'Account Description' TEXT,
                'CBS Account Status' TEXT,
                'CBS Account Name' TEXT,
                'Name Match %' TEXT,
                'ComRegister No' TEXT,
                'Company RegMatch %' TEXT,
                'PAN No' TEXT,
                'PAN Match %' TEXT,
                'Total Similarity %' TEXT,
                'Result of CIB Screening' TEXT,
                'CIB Name' TEXT,
                'CIB Com Registration No' TEXT,
                'CIB PAN NO' TEXT,
                'CIB Black Listed No' TEXT,
                'CIB Black Listed Date' TEXT,
                'Passport No' TEXT,
                'CBS Remarks' TEXT,
                'Delay_by_days' integer default 0,
                created_at DATETIME DEFAULT (datetime('now', 'localtime')), 
                updated_at DATETIME,
                'Status' TEXT
                )
            ''')
        self.con.commit()
        self.con.close()


    def insert_dataframe_into_database(self, df):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        # self.cur.execute(f'''PRAGMA tableinfo({Constants.CIB_USER_TABLE_NAME});''')
        # columns = self.cur.fetchall()
        # status_column_exists = any(column[1] == 'Status' for column in columns)
        # if not status_column_exists:
        #     self.cur.execute(f'''
        #                 ALTER TABLE {Constants.CIB_USER_TABLE_NAME}
        #                 ADD COLUMN Status TEXT;
        #             ''')
        self.cur.execute(f''' 
                UPDATE {Constants.CIB_USER_TABLE_NAME}
                SET Status = 'old'
                WHERE Status = 'new';
            ''')
        # df['Status'] = 'new'
        df.to_sql(
            Constants.CIB_USER_TABLE_NAME,
            self.con,
            if_exists='append',
            index=False
            )
        # logger = self.run_item.logger
        # logger.info('successfully inserted data to the database')
        display('SUCCESSFULLY INSERTED DATA TO THE DATABASE')

    def insert_report(self,report):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        report.to_sql(
            Constants.REPORT,
            # Constants.FINAL_REPORT,
            self.con,
            if_exists='append',
            index=False
            )
        # logger = self.run_item.logger
        # logger.info('successfully inserted report to the database')
        display('SUCCESSFULLY INSERTED report TO Individual table to THE DATABASE')

    def update_database_progress_status_with_individual_table(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()#and 'CBS Remarks' IS NOT NULL and 'CBS Account Status'  IN ('debit restrict','normal')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT}
                SET Status = 'Completed'
                WHERE "Result of CIB Screening" = 'Match with CIB Black List' and "CBS Remarks" IS NOT NULL and "CBS Account Status"  NOT IN ('credit restrict','normal') ;
            ''')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT}
                SET Status = 'Completed'
                WHERE "Result of CIB Screening" = 'No Match with CIB Black List' and "CBS Remarks" IS NULL and "CBS Account Status"  IN ('credit restrict','normal') ;
            ''')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT}
                SET Status = 'Pending'
                WHERE "Result of CIB Screening" = 'Match with CIB Black List' and "CBS Remarks" IS NULL and "CBS Account Status" IN ('normal', 'credit restrict') ;
            ''')
        self.con.commit()
        self.con.close()
        display('Successfully update the status')

    def update_pending_status_of_individual(self,main_code):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()# and 'CBS Remarks' IS NOT NULL and 'CBS Account Status' NOT IN ('credit restrict','normal')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT}
                SET Status = 'Complete', updated_at = datetime('now', 'localtime')
                WHERE "CBS Account Number" = {main_code};
            ''')
        display('Successfully update the pending status of individual data status')
        self.con.commit()
        self.con.close()

    def update_pending_status_of_institutional(self,main_code):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()# and 'CBS Remarks' IS NOT NULL and 'CBS Account Status' NOT IN ('credit restrict','normal')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT_INSTITUTE}
                SET Status = 'Complete', updated_at = datetime('now', 'localtime')
                WHERE "CBS Account Number" = {main_code};
            ''')
        display('Successfully update the pending status of institutional data status')
        self.con.commit()
        self.con.close()

    def update_delay_status(self,main_code,followup_count : int):
        display(f'main code is {main_code} and follow up count is {followup_count}')
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()# and 'CBS Remarks' IS NOT NULL and 'CBS Account Status' NOT IN ('credit restrict','normal')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT}
                SET Delay_by_days = ?
                WHERE "CBS Account Number" = ?;
            ''',(followup_count,main_code))
        # display('Successfully update Delay count')
        try:
            self.cur.execute(f''' 
                    UPDATE {Constants.REPORT_INSTITUTE}
                    SET Delay_by_days = ?
                    WHERE "CBS Account Number" = ?;
                ''',(followup_count,main_code))
            display('Successfully update Delay count')
        except Exception as e:
            display(e)

        self.con.commit()
        self.con.close()

    def remove_the_pending_status(self,followup_count):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(f''' 
                DELETE FROM {Constants.REPORT}
                WHERE "Delay_by_days" = ?;
            ''',(followup_count,))
        
        self.cur.execute(f''' 
                DELETE FROM {Constants.REPORT_INSTITUTE}
                WHERE "CDelay_by_days" = ?;
            ''',(followup_count,))
        
        self.con.commit()
        self.con.close()

    def update_database_progress_status_with_institutional_table(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()# and 'CBS Remarks' IS NOT NULL and 'CBS Account Status' NOT IN ('credit restrict','normal')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT_INSTITUTE}
                SET Status = 'Complete'
                WHERE "Result of CIB Screening" = 'Match with CIB Black List' and "CBS Remarks" IS NOT NULL and "CBS Account Status" NOT IN ('credit restrict','normal');
            ''')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT_INSTITUTE}
                SET Status = 'Complete'
                WHERE "Result of CIB Screening" = 'No Match with CIB Black List' and "CBS Remarks" IS NULL and "CBS Account Status" IN ('credit restrict','normal');
            ''')
        self.cur.execute(f''' 
                UPDATE {Constants.REPORT_INSTITUTE}
                SET Status = 'Pending'
                WHERE "Result of CIB Screening" = 'Match with CIB Black List' and "CBS Remarks" IS NULL and "CBS Account Status" IN ('normal', 'credit restrict') ;
            ''')
        display('Successfully update the status')
        self.con.commit()
        self.con.close()

    def insert_into_email_table(self,email,branch_name,status):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(''' 
                    CREATE TABLE IF NOT EXISTS EMAIL (
                         Email_ID Text,
                         Branch_name Text,
                         Status Text,
                         Insertion_Date DATETIME DEFAULT (datetime('now','localtime')),
                         follow_up_count integer default 0
                         
                    )
                    ''')
        sample_data = [
            (email,branch_name,status)
        ]
        display(sample_data)

        self.cur.executemany('INSERT INTO EMAIL (Email_ID,Branch_name,Status) VALUES (?,?,?)',sample_data)
        display('Successfully insert email to the email table')
        self.con.commit()
        self.con.close()
    
    def extract_institutional_data_with_pending_status(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute(f'''
                SELECT * FROM {Constants.REPORT_INSTITUTE}
                WHERE Status = 'pending'
             ''')
        #feth the rows
        rows = self.cur.fetchall()
        for row in rows:
            
            display(f'Row data is {row}')
            return row
        
        self.con.commit()
        self.con.close()
        display('Successfully extract the institutional pending data')

    def extract_individual_data_with_pending_status(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        query = f'''
        select * from  {Constants.REPORT}
        where status = 'pending'
    '''
        logger = self.run_item.logger
        self.con.row_factory = sqlite3.Row
        logger.info(f'Reading data having status pending from table  {Constants.REPORT}')
        data = self.con.execute(query).fetchall()
        if data:
            logger.info(f'All database data retrivied.')
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            # display(f'Pending data is {temp_value}')
            # temp_value.to_excel('test_data_cib.xlsx',index=False)
            return temp_value
        else:
            return []

    def get_the_value_with_status_Zero(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()

        self.cur.execute(''' 
                SELECT Email_ID from Email
                            WHERE Status == 0
            ''')
        data = self.cur.fetchall()
        for email in data:
            self.cur.execute(''' 
                                UPDATE Email 
                                SET follow_up_count = follow_up_count +1
                                WHERE Email_ID = ?
                            ''',(email[0],))
            return email[0]
        
        
        self.con.commit()
        self.con.close()

    # def delete_the_follow_up_with_count_three(self):
    #     self.con = sqlite3.connect(Constants.DB_NAME)
    #     self.cur = self.con.cursor()
    #     self.cur.execute('DELETE FROM Email WHERE follow_up_count = ?',(3,))
    #     display('Successfully delete the row with the followup count is 3')
    #     self.con.commit()
    #     self.con.close()

            
    def get_summary_report__of_individual_for_compliance(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        today_date = datetime.now().date()
        query = f'''
            SELECT * FROM {Constants.REPORT}
            WHERE DATE(created_at) = ?;
         '''
        # logger = self.run_item.logger
        self.con.row_factory = sqlite3.Row
        # logger.info(f'Reading data having status pending from table  {Constants.REPORT}')
        data = self.con.execute(query,(today_date,)).fetchall()
        if data:
            # logger.info(f'All database data retrivied.')
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            # display(f'Pending data is {temp_value}')
            # temp_value.to_excel('test_data_cib.xlsx',index=False)
            return temp_value
        else:
            return []
    def get_summary_report__of_institutional_for_compliance(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        today_date = datetime.now().date()
        query = f'''
            SELECT * FROM {Constants.REPORT_INSTITUTE}
            WHERE DATE(created_at) = ?;
         '''
        # logger = self.run_item.logger
        self.con.row_factory = sqlite3.Row
        # logger.info(f'Reading data having status pending from table  {Constants.REPORT}')
        data = self.con.execute(query,(today_date,)).fetchall()
        if data:
            # logger.info(f'All database data retrivied.')
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            # display(f'Pending data is {temp_value}')
            # temp_value.to_excel('test_data_cib.xlsx',index=False)
            return temp_value
        else:
            return []

    def update_status_of_email_table(self,email_list):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        for email in email_list:
            self.cur.execute(''' 
                        UPDATE EMAIL 
                        SET Status = 1
                        WHERE Email_ID = ?
                    ''',(email,))
        self.con.commit()
        self.con.close()
        
    def insert_institution_report(self,report):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        report.to_sql(
            Constants.REPORT_INSTITUTE,
            # Constants.FINAL_REPORT,
            self.con,
            if_exists='append',
            index=False
            )
        # logger = self.run_item.logger
        # logger.info('successfully inserted report to the database')
        display('SUCCESSFULLY INSERTED to Institutional table TO THE DATABASE')

 
            
    def get_data_with_status(self, status: str) -> list:

        query = f'''
        select * from  {Constants.CIB_USER_TABLE_NAME}
        where status = '{status}'
    '''
        logger = self.run_item.logger
        self.con.row_factory = sqlite3.Row
        logger.info(f'Reading data having status {status} from table  {Constants.CIB_USER_TABLE_NAME}')
        data = self.con.execute(query).fetchall()
        if data:
            logger.info(f'All database data retrivied.')
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            # temp_value.to_excel('test_data_cib.xlsx',index=False)
            return temp_value
        else:
            return []


    def add_status_column_in_database(self):
        self.cur.execute(f'''
                ALTER TABLE {Constants.CIB_USER_TABLE_NAME}
                ADD COLUMN Status Text;
      ''')
        
    def update_status_column(self):
        self.cur.execute(f'''
            UPDATE {Constants.CIB_USER_TABLE_NAME}
            SET Status = 'new';
        ''')
    def fetch_black_listed_data_from_database(self):
        self.cur.execute(f'''
                    SELECT BlackLists FROM {Constants.CIB_USER_TABLE_NAME};
        ''')
        black_lists_tuples = self.cur.fetchall()
        black_lists_number_database = [black_list[0].split("|")[1] for black_list in black_lists_tuples]
        # print(black_lists_number_database[0])
        return black_lists_number_database

    def fetch_latest_blacklisted_date_from_database(self):
        # Query to extract the latest blacklisted date
        self.cur.execute(f'SELECT BlackLists FROM {Constants.CIB_USER_TABLE_NAME};')

        # Fetch the result
        black_lists_tuples = self.cur.fetchall()

        # Extract dates and split them
        black_lists_dates = [black_list[0].split("|")[2] for black_list in black_lists_tuples]
        # Convert date strings to datetime objects, handling invalid dates
        date_objects = []
        for date_str in black_lists_dates:
            try:
                date_object = nepali_datetime.datetime.strptime(date_str, '%Y-%m-%d')
                date_objects.append(date_object)
            except ValueError:
                print(f"Skipping invalid date: {date_str}")

        
        # Find the latest date
        if date_objects:
            # print('date-object',date_objects)
            latest_date = max(date_objects)
            parsed_date = datetime.strptime(str(latest_date), "%Y-%m-%d %H:%M:%S%z")
            latest_blacklisted_date = parsed_date.strftime("%Y-%m-%d")
            # print("Latest Blacklisted Date:", latest_blacklisted_date)
            # return latest_blacklisted_date
        else:
            print("No valid dates found in the database.")
        return latest_blacklisted_date
    
    def update_remarks_on_unique_id(self, unique_id: str, remarks: str):
        logger = self.run_item.logger
        query = f'''
            update {self.table_name}
            set remark = '{remarks}'
            where unique_id = '{unique_id}'
        '''
        self.cursor.execute(query)
        logger.info('updating status successfull.')
    
    def update_progess_status(self, unique_id: str, status: str):
        logger = self.run_item.logger
        query = f'''
            update {self.table_name}
            set status = '{status}', updated_at = datetime('now', 'localtime')
            where unique_id = '{unique_id}'
        '''
        self.cursor.execute(query)
        logger.info('updating status successfull.')