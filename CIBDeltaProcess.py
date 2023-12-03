from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from DefaultComponent import DefaultComponent
from DBComponent import DBComponent
from APIComponent import APIComponent
from EmailComponent import EmailComponent
from datetime import datetime,timedelta
from Variables import BotVariable
from qrlib.QRUtils import display
from FileComponent import FileComponent
from robot.libraries.BuiltIn import BuiltIn
# from WeightageProcess import WeightageProcess
import Constants
import Levenshtein as lev
import pandas as pd
from DBView import DatabaseViewTask
import nepali_datetime
import json
import os
import ast

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
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        run_item = QRRunItem()

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
        logger = run_item.logger
        try:
            self.db.connect()
            # self.db.create_cib_users_table()
        except Exception as e:
            run_item.report_data = {"Remarks": "Database error error"}
            raise e
        
        try:
            self.api.load_vault_api()

            self.db_view.__enter__()
            self.df_map = self.db_view.collect_all_view_table()
            # self.api.get_data()
            # local_hashed_code = self.api.generate_local_hash_code()
            api_hash_code = self.api.get_hash_code()
            # display(f"Local_Hash_code_is: {local_hashed_code}")
            hash_data = {
                "api_hash_code":api_hash_code
            }
            # display(f"API_Hash_code_is: {api_hash_code}")
            with open(Constants.HASH_FILE_PATH,'w') as json_file:
                json.dump(hash_data, json_file)


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
                    display('IF PART')
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
                    display('PASS THE DATA TO THE DATABASE TO INSERT')
                    logger.info('PASS THE DATA TO THE DATABASE TO INSERT')

            else:
                logger.info('performing the substituent run action')
                display("performing the substituent run action")
                # self.db_view.__enter__()
                # self.db_view.collect_all_view_table()
                local_hashed_code = self.api.generate_local_hash_code()
                # display(f"{local_hashed_code}")
                with open(Constants.hash_code_file_path,'r') as file:
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

                    Found_blacklist_number_in_database =filtered_df[filtered_df['Found_number'].notnull()]
                    
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
        # todo: does given data exist in cbs
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
        
    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        # run_item: QRRunItem = kwargs["run_item"]
        # self.notify(run_item)
        start_time = BuiltIn().get_time()
        run_item: QRRunItem = QRRunItem(is_ticket=True)
        self.notify(run_item)

        display('ExecuteRunItem: CIB Action Process')
        # todo: do weightage process, also required generation
        item = args[0]
        df_map = args[1]
        display(f'Item consit of (cib process) ==>{item}')
        display(f'columns of the items are {item.keys()}')
        display(len(item['CBS Account Number']))
        # display(f'Client code is {item['CBS Client Code']}')
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
        length_remarks = len(result_data['remarks'])
        display(f'Length of remarks is {length_remarks}')
        not_empty_remarks = result_data['remarks'].notnull()
        display(f'Result remarks is {not_empty_remarks}')
        # if empty_remarks:
        # if len(result_data['remarks']) > 0:
        if not_empty_remarks:
            # display('Apple')
            try:
                # self.db.update_pending_status_of_individual(item['CBS Account Number'])
                if 'CIB Father Name' in item.keys():
                    display('Apple')
                    self.db.update_pending_status_of_individual(item['CBS Account Number'])
                elif item['ComRegister No'] in item:
                    self.db.update_pending_status_of_institutional(item['CBS Account Number'])
                    display('Apple')
            except Exception as e:
            # logger.error(traceback.format_exc())
                # raise e
                display(f'Exception is ===> {e}')
        else:
            delay_day = result_data['Delay_by_days']
            display(f'Delay by days is ==> {delay_day}')
            if result_data['Delay_by_days'] == 0:
                self.db.update_delay_status(item['CBS Account Number'],result_data['Delay_by_days']+1)
                df = pd.DataFrame(item)
                df.to_excel(f'{Constants.FOLLOW_UP_REPORT}',index=False)
                display('sucessfully download the followup mail')
                # attachment_path = os.path.join(Constants.FOLLOW_UP_PATH,'followup_file.xlsx')
                # self.email


        
        # df = self
        # display(df.head())
        # display(f'Client_table_columns name are {df_map['client_table']}')

        # Sample DataFrames (replace these with your actual DataFrames)
       
    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        # todo: send mail to branches after calculating weightage process

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        # todo: send summary report at the EOD
 
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
