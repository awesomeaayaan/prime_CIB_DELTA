import json
import os
import ast

from datetime import datetime, timedelta

import pandas as pd
import nepali_datetime
from robot.libraries.BuiltIn import BuiltIn

from qrlib.QRUtils import display
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem

import Constants

from Variables import BotVariable
from DBComponent import DBComponent
from APIComponent import APIComponent
from FileComponent import FileComponent
from EmailComponent import EmailComponent
from DefaultComponent import DefaultComponent
# from WeightageProcess import WeightageProcess
from DBView import DatabaseViewTask


class CIBDeltaProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.default_component = DefaultComponent()
        self.register(self.default_component)
        self.data = []
        self.db = DBComponent()
        self.api = APIComponent()
        self.file = FileComponent()
        self.db_view = DatabaseViewTask()
        self.email = EmailComponent()
        # self.weightage = WeightageProcess()

        self.register(self.db)
        self.register(self.api)
        self.register(self.db_view)
        self.register(self.email)
        self.register(self.file)
        # self.register(self.weightage)

        self.data = []

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        """
        before run
        step 1: Initiliaze database table, and required vault
        step 2: validate hash values
        step 3: get bulk data from cibnepal api
        step 4: check local db is empty or not
            if empty: push all bulk data into local database and stop bot, need to add differenet status for this in local db
            if not empty: compare data and find incremenntal data, and insert to local db
        step 5: get all pending data
        
        execute run
        step 6: 
        for each pending data
            before_run_item, execute_run_item, after_run_item
            step 7: check data exist in cbs
            step 8: 
                if exist, 
                    i. calculate weightage process
                    ii. send mail to respective branch and update status
                if not exist, send mail to main department for respective data does not exist in cbs
        
        before_run
        step 9:
            followup:
            i. check if previous mail send mail has reply back or not
            ii. check matched row from the excel file in mail
            iii. check if matched row are blocked

        """
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        run_item = QRRunItem()

        logger = run_item.logger
        try:
            self.db.connect()
            # self.db.create_cib_users_table()
        except Exception as e:
            run_item.report_data = {"Remarks": "Database error error"}
            raise e

        try:
            self.api.load_vault_api()
        except Exception as e:
            run_item.report_data = {"Remarks": "Loading CIB vault data error"}
            raise e
            
        try:
            # self.db_view.__enter__()
            with self.db_view as local_db:
                self.df_map = local_db.collect_all_view_table()

            # self.api.get_data()
            # local_hashed_code = self.api.generate_local_hash_code()
            api_hash_code = self.api.get_hash_code()
            # display(f"Local_Hash_code_is: {local_hashed_code}")
            hash_data = {
                "api_hash_code": api_hash_code
            }
            # display(f"API_Hash_code_is: {api_hash_code}")
            # if not os.path.exists(Constants.HASH_FILE_PATH):
            #     os.makedirs(Constants.HASH_FILE_PATH)
            with open(Constants.HASH_FILE_PATH, 'w') as json_file:
                json.dump(hash_data, json_file)
            # if not os.path.exists(Constants.FLAG_FILE_PATH):
            #     os.makedirs(Constants.FLAG_FILE_PATH)
            if not os.path.exists(Constants.FLAG_FILE_PATH):
                first_run_flag = True
                with open(Constants.FLAG_FILE_PATH,'w') as flag_file:
                    flag_file.write('1')
            else:
                first_run_flag = False

            if first_run_flag:
                logger.info("performing the first run action")
                display("performing the first run action")

                local_hashed_code = self.api.generate_local_hash_code()
                # display(f"{local_hashed_code}")

                with open(Constants.HASH_FILE_PATH,'r') as json_file:
                    loaded_api_hash_code = json.load(json_file)
                # display(f"{local_hashed_code}=============={loaded_api_hash_code}")

                if loaded_api_hash_code == local_hashed_code:
                    display('loaded api hash code and local hash code is same')
                    cib_df = self.api.get_data()
                    display('GET DATA FROM THE API COMPONENT')
                    logger.info('GET DATA FROM THE API COMPONENT')
                    self.db.insert_first_run_data(cib_df)
                    # self.db.insert_dataframe_into_database(cib_df)
                    display(f"dataframe=====>{cib_df.head()}")
                    logger.info(f"dataframe=====>{cib_df.head()}")
                else:
                    self.api.get_hash_code()
                    # self.api.get_data()
                    display('CALL ELSE PART')
                    cib_df = self.api.get_data()
                    display('GET DATA FROM THE API COMPONENT')
                    logger.info('GET DATA FROM THE API COMPONENT')
                    self.db.insert_first_run_data(cib_df)
                    # self.db.insert_dataframe_into_database(cib_df)
                    display('INSERT FIRST RUN DATA INTO THE DATABASE')
                    logger.info('PASS THE DATA TO THE DATABASE TO INSERT')
            else:
                logger.info('performing the substituent run action')
                display("performing the substituent run action")
                # self.db_view.__enter__()
                # self.db_view.collect_all_view_table()
                local_hashed_code = self.api.generate_local_hash_code()
                # display(f"{local_hashed_code}")
                if not os.path.exists(Constants.hash_code_file_path):
                    os.makedirs(Constants.hash_code_file_path)
                with open(Constants.hash_code_file_path, 'r') as file:
                    api_hashed_data = file.read()
                # display(f"{local_hashed_code}=============={api_hashed_data}")

                if api_hashed_data == local_hashed_code:
                    self.cib_df = self.api.get_data()
                    
                    # filtering the previous day data and stored it in the filtered_df 
                    
                    self.from_date = self.db.fetch_latest_blacklisted_date_from_database()
                    print('from_date',self.from_date)

                    def filter_dates(blacklist_entry):
                        start_date = self.from_date
                        date = nepali_datetime.date.today()
                        end_date = str(date)
                        if isinstance(blacklist_entry, list):
                            return any(start_date <= item.split('|')[2] <= end_date for item in blacklist_entry)
                        else:
                            return start_date <= blacklist_entry.split('|')[2] <= end_date

                    filtered_df = self.cib_df[self.cib_df['BlackLists'].apply(filter_dates)]
                    # filtered_df.to_excel('filtertoday.xlsx',index = False)
                    print(f"{filtered_df}")
                    logger.info(f'Filtered Dataframe is {filtered_df}')
                    # print(f"filtereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed==>{filtered_df['BlackLists'].count()}")
                    black_lists_number_from_database = self.db.fetch_black_listed_data_from_database()

                    for index,data in filtered_df['BlackLists'].items():
                        if ',' in data:
                            item_list = ast.literal_eval(data)
                            if isinstance(item_list,list):
                                for item in item_list:
                                    black_list = item.split('|')[1]
                                    # print(black_list)
                                    filtered_df.at[index, 'BlackListNumber'] = black_list
                        else:
                            black_list = data.split('|')[1]
                            filtered_df.at[index, 'BlackListNumber'] = black_list

                    for index, data in filtered_df['BlackListNumber'].items():
                        if data in black_lists_number_from_database:
                            filtered_df.at[index, 'Found_number'] = data
                        else:
                            filtered_df.at[index, 'Not_Found_number'] = data
                    # filtered_df.to_excel('filtered.xlsx',index=False)

                    # Found_blacklist_number_in_database = filtered_df[filtered_df['Found_number'].notnull()]
                    
                    self.incremental_data =filtered_df[filtered_df['Not_Found_number'].notnull()]
                    self.incremental_data.drop(columns=['BlackListNumber','Found_number','Not_Found_number'],inplace=True)
                    logger.info('delete unnecessary file')
                    display(self.incremental_data)
                    logger.info(f'Incremental Data is == > {self.incremental_data.shape}')
                    self.db.insert_dataframe_into_database(self.incremental_data)
                else:
                    self.api.get_hash_code()
                    self.api.get_data()
        except Exception as e:
            run_item.report_data = {"Remarks": "Load vault error"}
            raise e
                        
    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

    def get_follow_up_data(self,*args,**kwargs):
         # * Collect remainig data from database
        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)

        logger = run_item.logger
        self.data = []
        try:
            # with self.db as db:
            self.data.extend(self.db.extract_individual_data_with_pending_status())
            # self.data.extend(self.db.extract_institutional_data_with_pending_status())
            # display(f'Extracted data is ==> {self.data}')
            if self.data:
                return True
            else:
                return False
        except Exception as e:
            display(e)
            display('Data Not found or failed to read data from database')
            run_item.report_data['Task'] = 'follow up  Data Collection: CIB Action Process'
            run_item.report_data['Reason'] = 'Failed to collect yesterday matched data from database.'
            run_item.set_error()
            run_item.post()
            raise e

    def read_file_and_send_email(self):
        # directory = r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\test_email\attachments"
        directory = os.path.join(Constants.cib_common_path,'downloaded_attachment')
        if not os.path.exists(directory):
            os.makedirs(directory)
        # self.db.extract_institutional_data_with_pending_status()
        # current_path = os.getcwd()
        # directory = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','test_email','attachments'))
        display(os.listdir(directory))
        for file in os.listdir(directory):
            if file.endswith('.xlsx'):
                display(f'File is ==> {file}')
                df = pd.read_excel(os.path.join(directory,file))
                if 'CBS Father Name' in df:
                    if df['Result of CIB Screening'].iloc[0] == 'Match with CIB Black List' or df['Result of CIB Screening'].iloc[0] == 'No Match with CIB Black List' and 'CBS Father Name' in df:
                    # if 'CBS Father Name' in df:
                        df['CBS Account Number'] = df['CBS Account Number'].astype(str)
                        display(df['Result of CIB Screening'].iloc[0])
                        self.db.create_individual_table()
                        self.db.insert_report(df)
                        self.db.update_database_progress_status_with_individual_table()

                        # if df['CBS Account Status'] == 'normal' or df['CBS Account Status'] == 'credit restrict' and df['CBS Remarks'] is not None:

                        #     pass
                        file_path = os.path.join(directory,file)
                        os.remove(file_path)
                elif 'CIB Com Registration No' in df:
                    if df['Result of CIB Screening'].iloc[0] == 'Match with CIB Black List' or df['Result of CIB Screening'].iloc[0] == 'No Match with CIB Black List' and 'CIB Com Registration No' in df:
                        display(df['Result of CIB Screening'].iloc[0])
                        df['CBS Account Number'] = df['CBS Account Number'].astype(str)
                        self.db.create_institutional_table()
                        self.db.insert_institution_report(df) 
                        self.db.update_database_progress_status_with_institutional_table()
                        file_path = os.path.join(directory,file)
                        os.remove(file_path)
                elif df['Result of CIB Screening'].iloc[0] == 'none':
                    df = pd.read_excel(os.path.join(directory,file))
                    branch_value = str(df['Branch Code'].iloc[0])
                    file_path = os.path.join(directory,file)
                    display(file_path)
                    display(branch_value)
                    display(df['Result of CIB Screening'].iloc[0])
                    self.email.follow_up_mail(branch_value,file_path)
                    os.remove(file_path)

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        # run_item: QRRunItem = kwargs["run_item"]
        # self.notify(run_item)
        start_time = BuiltIn().get_time()
        run_item: QRRunItem = QRRunItem(is_ticket=True)
        self.notify(run_item)

        display('ExecuteRunItem: CIB Action Process')
        item = args[0]
        df_map = args[1]
        display(f'Item consit of (cib process) ==>{item}')
        display(f'columns of the items are {item.keys()}')
        display(len(item['CBS Account Number']))
        # display(f'Client code is {item['CBS Client Code']}')
        display(f'DF MAP column are == > {df_map.keys}')
        display(f'Column of the df_map are {df_map.keys()}')
        self.file.set_dataframe(df_map['client_table'])
        data = self.file.collect_maincode_data_and_join_table(df_map['client_table'],df_map['client_master'])
        display(f'Data is {data}')
        main_code = str(item['CBS Account Number']).zfill(Constants.MAINCODE_LENGTH)
        display(main_code)
        result_data = data[data['maincode'] == main_code]
        display(f'Column of the data frame is {result_data.columns}')
        display(result_data)
        display(f'Columns of the data are ==>{data.columns}')
        display(result_data['remarks'].str.strip())
        result_data['remarks'] = result_data['remarks'].str.strip()
        length_remarks = len(result_data['remarks'])
        display(f'Length of remarks is {length_remarks}')
        not_empty_remarks = result_data['remarks'].notnull() & (result_data['remarks'] != '')
        display(f'Result remarks is {not_empty_remarks}')
        # if empty_remarks:
        # if len(result_data['remarks']) > 0:
        if not_empty_remarks.any():
            # display('Apple')
            try:
                # self.db.update_pending_status_of_individual(item['CBS Account Number'])
                if 'CIB Father Name' in item.keys():
                    # display('Apple')
                    self.db.update_pending_status_of_individual(item['CBS Account Number'])
                elif item['ComRegister No'] in item:
                    self.db.update_pending_status_of_institutional(item['CBS Account Number'])
                    # display('Apple')
            except Exception as e:
            # logger.error(traceback.format_exc())
                # raise e
                display(f'Exception is ===> {e}')
        else:
            # display('Apple')
            delay_day = item['Delay_by_days']
            display(f'Delay by days is ==> {delay_day+1}')
            if  item['Delay_by_days'] < 4:
                self.db.update_delay_status(item['CBS Account Number'],item['Delay_by_days']+1)
                df = pd.DataFrame(item,index=[0])
                columns_to_drop = ['Delay_by_days','created_at','updated_at','Status']
                df.drop(columns=columns_to_drop,inplace=True)
                display(df.head())
                if not os.path.exists(Constants.FOLLOW_UP_PATH):
                    os.makedirs(Constants.FOLLOW_UP_PATH)
                df.to_excel(f'{Constants.FOLLOW_UP_REPORT}',index=False)
                display('sucessfully get the followup data to mail to respective branch')
                branch_value = str(df['Branch Code'].iloc[0])
                if not os.path.exists(Constants.FOLLOW_UP_PATH):
                    os.makedirs(Constants.FOLLOW_UP_PATH)
                attachment_path = os.path.join(Constants.FOLLOW_UP_PATH,'followup_file.xlsx')
                self.email.follow_up_pending_mail(branch_value,attachment_path)

            elif item['Delay_by_days'] == 4:

                self.db.remove_the_pending_status(item['Delay_by_days'])
                display('Successfully remove the pending status')

        summary_data_individual = self.db.get_summary_report__of_individual_for_compliance()
        df = pd.DataFrame(summary_data_individual)
        display(df.head())
        # df.to_excel('summary_report.xlsx',index=False)
        column_to_drop = ['created_at','updated_at']
        df.drop(columns=column_to_drop,inplace=False)
        desired_order = ['Branch Code', 'CBS Client Code', 'CBS Account Number',
       'Account Description',  'CBS Account Name',
       'Name Match %', 'CBS Father Name', 'Father Name %',
       'CBS Date of birth(BS)', 'DOB Match %', 'CBS Citizenship No',
       'Citizenship Match %', 'PAN NUMBER %', 'PASSPORT NUMBER %',
       'Indian Embassy Reg No %', 'Total Similarity %',
        'CIB Name', 'CIB Father Name', 'CIB DOB',
       'CIB Citizenship No', 'CIB PAN No', 'CIB PASSPORT NO',
       'CIB Indian Embassy NO', 'CIB Gender', 'CIB Black Listed No',
       'CIB Black Listed Date', 'Driving Licence No', 'Indian Embassy Reg No',
       'PAN No', 'Passport No', 'CBS Remarks', 'Result of CIB Screening','CBS Account Status','Delay_by_days',
       'Status']
        df = df[desired_order]
        df.to_excel(f'{Constants.COMPLIANCE_REPORT_INDIVIDUAL}',index=False)
        # df.to_excel('summary_report_individual.xlsx',index=False)
        try:
            summary_data_institutional = self.db.get_summary_report__of_institutional_for_compliance()
            df = pd.DataFrame(summary_data_institutional)
            display(df.head())
            display(f'Columns of the institutional data is {df.columns}')
            # df.to_excel('summary_report.xlsx',index=False)
            column_to_drop = ['created_at','updated_at']
            df.drop(columns=column_to_drop,inplace=False)
            desired_order = ['Branch Code', 'CBS Client Code', 'CBS Account Number',
                'Account Description',  'CBS Account Name',
                'Name Match %', 'ComRegister No', 'Company RegMatch %', 'PAN No',
                'PAN Match %', 'Total Similarity %', 
                'CIB Name', 'CIB Com Registration No', 'CIB PAN NO',
                'CIB Black Listed No', 'CIB Black Listed Date', 'Passport No',
                'CBS Remarks','Result of CIB Screening','CBS Account Status', 'Delay_by_days','Status']
            df = df[desired_order]
            df.to_excel(f'{Constants.COMPLIANCE_REPORT_INSTITUTIONAL}',index=False)
            # df.to_excel('institutional_summary.xlsx',index=False)


        except Exception as e:
            display(e)
        # attachment_path =  os.path.join(Constants.COMPLIANCE_FILE_PATH,'summary_individual_report.xlsx')
        self.email.summary_mail_to_compliance()
       
    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

 
    def execute_run(self,*args):
        display('Excute Run: CIB DELTA Action Process')
        run_item = QRRunItem()
        self.notify(run_item)

        logger = run_item.logger
        df_map: dict = args[0]
        display(f'Length of data in data execution {len(self.data)}')

        for row in self.data:
            display(f"Working data in cib delta Process {row}")
            # BuiltIn().run_keyword('CIBDeltaProcess.execute_run_item', row, df_map)
            self.execute_run_item(row,df_map)

        # self.execute_run_item()   
