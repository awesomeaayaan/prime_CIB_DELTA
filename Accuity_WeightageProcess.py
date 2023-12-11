import os
import re
import time
import uuid
import shutil
import traceback
import pandas as pd
import datetime as dt
import ast
from robot.libraries.BuiltIn import BuiltIn

from qrlib.QREnv import QREnv
from qrlib.QRProcess import QRProcess
from qrlib.QRRunItem import QRRunItem
from qrlib.QRDecorators import run_item

import Utils
import Constants

# from TaskLogger import TaskLogger
from qrlib.QRUtils import display
from AccuityDbComponent import AccuityDbComponent
from AccuityFileComponent import AccuityFileComponent
from DBView import DatabaseViewTask



class Accuity_WeightageProcess(QRProcess):
    def __init__(self):
        super().__init__()
      

        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)
        self.db_accuity = AccuityDbComponent()
        self.accuityfile = AccuityFileComponent()
        self.db_view = DatabaseViewTask()
        self.register(self.db_accuity)
        self.register(self.accuityfile)
        self.register(self.db_view)
  

        self.data = []
        self.exe_item = {}
        self.link = ''
        self.filename = None
        self.df_map = {}

        # self.tasklogger.set_folder_name()

    def before_run(self, *args, **kwargs):
        display('Before Run: Weitage Process')
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)
        try:
            self.data = []
            self.db_accuity.connect()
            self.data.extend(self.db_accuity.get_data_with_status('new'))#get accuity data from the database
            display('Connect up to before run')

        except Exception as e:
            # logger.error(e)
            # logger.info('Data Not found or failed to read data from database')
            run_item.report_data['Task'] = 'BeforeRun: Weightage Process'
            run_item.report_data['Reason'] = 'Get data from db failed'
            run_item.set_error()
            run_item.post()
            raise e
        return True if self.data else False
            
        

    # def get_wp_requests(self, *args, **kwargs):
    #     run_item = QRRunItem(is_ticket=False)
    #     self.notify(run_item)
    #     logger = run_item.logger

    #     try:
    #         # logger.info(f"Get all pending requested data")
    #         self.data = []
            
    #         # display(f'this is self_data{self.data}')
    #         # with self.db:
            
    #     #     # self.data.extend(db.get_data_with_status('retry'))
    #         self.db.connect()
    #         #{'Name': 'AKKAL MADIRA PASAL', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '601347267|2070-05-20|Banke', 'CompanyDetails': '22569/070/071|NULL|Department of Commerce', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|91467|2080-08-08|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'SHIVA SHIKHAR MULTIPURPOSE OPERATIVE', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '600799148|2069-08-05|N/A', 'CompanyDetails': '588/069/70|NULL|Department of Cooperative', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|91408|2080-08-08|NON CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},
    #         self.data.extend(self.db.get_data_with_status('new'))#get black list data from the cib table from database
    #         # self.data = [{'Name': 'RAM KUMAR THAPA', 'DOB': '2022-01-09', 'Gender': 'M', 'FatherName': 'RAM KRISHNA THAPA', 'CitizenshipDetails': '295|2042-06-08|Kathmandu', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|92720|2080-08-19|NON CF|Promoter Director', 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'DHARMENDRA LAL KARNA', 'DOB': '2039-10-25', 'Gender': 'M', 'FatherName': 'SURYA DEV LAL KARNA', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '103664592|2070-02-09|Parsa', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|91608|2080-08-10|NON CF|Borrower', 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'SANTA KUMAR TAMANG', 'DOB': '2049-04-03', 'Gender': 'M', 'FatherName': 'INDRA SINGH TAMANG', 'CitizenshipDetails': '04-01-70-22850|2070-09-11|Jhapa', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': "['Bank and Financial Institutions|77074|2080-04-12|NON CF|Proprietor', 'Bank and Financial Institutions|74160|2080-03-27|NON CF|Borrower']", 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'SHAMBHU NAYAK SUDI', 'DOB': '2047-02-02', 'Gender': 'M', 'FatherName': 'MAHENDRA NAYAK SUDI', 'CitizenshipDetails': '171089/29|2065-10-15|Dhanusha', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': "['Bank and Financial Institutions|52223|2079-09-17|NON CF|Borrower', 'Bank and Financial Institutions|70837|2080-03-06|CF|Guarantor']", 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'RAHAMAT MANSURI', 'DOB': '2023-11-18', 'Gender': 'M', 'FatherName': 'SULMAN MIYA MASNURI', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': '13284575|N/A', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|67045|2080-02-10|NON CF|Borrower', 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': "PUBLIC MEDIA PVT.LTD", 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '500181719|2057-10-02|Kathmandu', 'CompanyDetails': '14689|NULL|Office of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|18468|2077-04-13|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'KAJU YAKI ENTERPRISES', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '', 'CompanyDetails': '002-2801-254-1|NULL|Office Of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|1337|2057-09-24|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': "SHAKYAS FINE JEWELLERY AND WORKSHOP", 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '300332733|2058-06-23|Bhaktapur', 'CompanyDetails': ['1831/054/55|NULL|Office of Cottage and Small Industry','1831/054/55|NULL|Office of Cottage and Small Industry'], 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|18468|2077-04-13|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'KAJU YAKI ENTERPRISES', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '', 'CompanyDetails': '002-2801-254-1|NULL|Office Of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|1337|2057-09-24|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'BABURAM SHRESTHA', 'DOB': '2035-10-05', 'Gender': 'M', 'FatherName': 'KULMAN SHRESTHA', 'CitizenshipDetails': '27039-|2055-07-01|Dhading', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|58247|2079-11-21|NON CF|Borrower', 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'SABIN LAMICHHANE', 'DOB': '2053-02-19', 'Gender': 'M', 'FatherName': 'LALARI PRASAD LAMICHHANE', 'CitizenshipDetails': '441008/745|2069-12-30|Gorakha', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|58249|2079-11-21|NON CF|Borrower', 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'BIKRAM PRASAD SAIJU', 'DOB': '2029-08-15', 'Gender': 'M', 'FatherName': 'NANDA KUMAR SAIJU', 'CitizenshipDetails': '2-2212|2046-01-08|Bhaktapur', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': 'nan', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': 'nan', 'BlackLists': "['Bank and Financial Institutions|69779|2080-02-31|NON CF|Borrower', 'Bank and Financial Institutions|74112|2080-03-27|NON CF|Borrower']", 'Account_Nature': 'Individual', 'Status': 'new'},{'Name': 'ROSHAN SHRESTHA', 'DOB': '2035-04-16', 'Gender': 'M', 'FatherName': 'ASHOK SHRESTHA', 'CitizenshipDetails': "", 'PassportDetails': '', 'DrivingLicenseDetails': '', 'VoterIDDetails': '', 'PANDetails': '602298847|2071-04-22|Banke', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': '', 'BlackLists': 'Bank and Financial Institutions|87349|2080-06-24|CF|Guarantor', 'Account_Nature': 'Individual', 'Status': 'new'}]
    #         # self.data = [{'Name': 'RUPALI KHADDAYAN STORES', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '614420548|2077-08-22|Kathmandu', 'CompanyDetails': "['3-35-382-158100/2077/78|NULL|Department of Commerce,Supplies Consumers Protection', '31-29-0114-23670|NULL|Municipality Office']", 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|78685|2080-04-23|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'SWASTIK STORES', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '', 'CompanyDetails': '002-4701-31-1|NULL|Office Of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|1069|2056-05-07|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'SUBEDI KHADYA STORE', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '', 'CompanyDetails': '47987/055/56|NULL|Office Of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': 'Bank and Financial Institutions|2848|2063-01-05|CF|Borrower', 'Account_Nature': 'Institutions', 'Status': 'new'},{'Name': 'STEEL ROLLING', 'DOB': 'nan', 'Gender': 'nan', 'FatherName': 'nan', 'CitizenshipDetails': 'nan', 'PassportDetails': 'nan', 'DrivingLicenseDetails': 'nan', 'VoterIDDetails': 'nan', 'PANDetails': '', 'CompanyDetails': '1206/050/51|NULL|Office Of Company Registrar', 'IndianEmbassyDetails': 'nan', 'BlackLists': "['Bank and Financial Institutions|1815|2059-03-31|CF|Borrower', 'Bank and Financial Institutions|3894|2068-04-13|CF|Borrower']", 'Account_Nature': 'Institutions', 'Status': 'new'}]
    #         # display(f'LIST OF DATA FROM DATABASE WITH STATUS NEW {self.data}')
    #     except Exception as e:
    #         logger.error(e)
    #         logger.info('Data Not found or failed to read data from database')
    #         run_item.report_data['Task'] = 'BeforeRun: Weightage Process'
    #         run_item.report_data['Reason'] = 'Get data from db failed'
    #         run_item.set_error()
    #         run_item.post()
    #         raise e
    #     return True if self.data else False
    
    def before_run_item(self, *args, **kwargs):
        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)
        logger = run_item.logger
        logger.info('Before Run Item: Weightage Process')
        # item_data = args

        item: dict = args[0] #dabase bata acquity ko  incremental data aako 
        # display(f'Item is {item}')
        logger = run_item.logger
        try:
            # item = {'Name': 'ROSHAN SHRESTHA', 'DOB': '16/04/2035', 'Gender': 'M', 'FatherName': 'ASHOK SHRESTHA', 'CitizenshipDetails': "['19-028|2063-11-09|Banke', '19/028/844|2063-11-09|Banke']", 'PassportDetails': '', 'DrivingLicenseDetails': '', 'VoterIDDetails': '', 'PANDetails': '602298847|2071-04-22|Banke', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': '', 'BlackLists': 'Bank and Financial Institutions|87349|2080-06-24|CF|Guarantor', 'Account_Nature': 'Individual', 'Status': 'new'}
            self.exe_item =  self.accuityfile.collect_user_reqiured_data(item)
            # display(f'this is from after collect user required data===>{self.exe_item}')
            logger.info(self.exe_item)
            logger.info('User data collect for weightage process successfull.')
        except Exception as e:
            # with self.db as db:
            #     count = db.get_error_retry_count(item['unique_id'])
            #     db.update_error_retry_count(item['unique_id'],int(count) + 1)
            #     db.update_remarks_on_unique_id(item['unique_id'], 'Failed to collect data in data collection in weightage process.')
            logger.error(e)
            run_item.report_data['Task'] = 'Before run item: WeightageProcess'
            run_item.report_data['Reason'] = 'Failed to collect data for weightage process.'
            run_item.set_error()
            run_item.post()
            raise Exception('No data found')
        
       
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        display('Execute Run Item: Weitage Process')
        run_item: QRRunItem = QRRunItem(is_ticket=True)
        self.notify(run_item)
        # display(f'Args is {args}')
        
        item = args[0]
        display(f'item==========>{item}')

       #ccount_nature': 'individual', 'name': 'PANKAJ KUMAR', 'fathername': 'HARDEV CHAUDHARI', 'dob': '16/04/2035', 'indianembassy_no': '19-028', 'search_list': ['name', 'fathername', 'dob', 'indianembassy_no']}
        
        
        temp_item: dict = args[1]
        # temp_item = {'Name': 'ROSHAN SHRESTHA', 'DOB': '2035-04-16', 'Gender': 'M', 'FatherName': 'ASHOK SHRESTHA', 'CitizenshipDetails': "['19-028|2063-11-09|Banke', '19/028/844|2063-11-09|Banke']", 'PassportDetails': '', 'DrivingLicenseDetails': '', 'VoterIDDetails': '', 'PANDetails': '602298847|2071-04-22|Banke', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': '', 'BlackLists': 'Bank and Financial Institutions|87349|2080-06-24|CF|Guarantor', 'Account_Nature': 'Individual', 'Status': 'new'}
        # temp_item = {'Name': 'ROSHAN SHRESTHA', 'DOB': '2035-04-16', 'Gender': 'M', 'FatherName': 'ASHOK SHRESTHA', 'CitizenshipDetails': "", 'PassportDetails': '', 'DrivingLicenseDetails': '', 'VoterIDDetails': '', 'PANDetails': '602298847|2071-04-22|Banke', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': '', 'BlackLists': 'Bank and Financial Institutions|87349|2080-06-24|CF|Guarantor', 'Account_Nature': 'Individual', 'Status': 'new'}
        # temp_item = {'Name': 'PANKAJ KUMAR', 'DOB': '2035-04-16', 'Gender': 'M', 'FatherName': 'HARDEV CHAUDHARI', 'CitizenshipDetails': "", 'PassportDetails': '', 'DrivingLicenseDetails': '', 'VoterIDDetails': '', 'PANDetails': '', 'CompanyDetails': 'nan', 'IndianEmbassyDetails': '669/2020|NULL', 'BlackLists': 'Bank and Financial Institutions|39207|2079-03-19|NON CF|Borrower', 'Account_Nature': 'Individual', 'Status': 'new'}
        display(f'TEMP_iTEM===================>{temp_item}')
        df_map: dict = args[2]
        logger = run_item.logger
        start_time = time.time()

        display(f'\nWeightage calculation on {item}\n')
        logger.info(f'\nWeightage calculation on {item}\n')

        try:
            status = str(temp_item['Status']).strip()
            search_list: list = item['search_list']
            min_value = 95
            logger.info(f'Search list : {search_list}')

            if str(item['Gender']) != -1:
                search_type = 'natural'
            else:
                search_type = 'legal'

            display(f'Search type is============>{search_type}')

            # weightage = Utils.get_weightage(search_list, search_type)
            # display(f'Weitage is ============>{weightage}')
            weightage = {
                'name': 50,
                'dobs': 25,
                'countryName': 25,
                
            }
            # weightage = {
            #     'name': 40,
            #     'pan_no': 25,
            #     'registration_no': 25,
                
            # }
            display(f'Weitage is ============>{weightage}')
            logger.info(f'Weightage values are {weightage}')

            result = []
            item_list = []
            new_columns_list = []
            required_columns = []
            temp_search_item = []
            temp_result = []

            self.accuityfile.set_dataframe(df_map['client_table'])
            # display(f'CLIENT TABLE {self}')
            temp_search_item.extend(search_list)
            display(f'Search list is {search_list}')
            for search in search_list:
                display(f'Search is {search}')
                # * Condition decide which column from view table weightage going to be calculated.
                # search = search.lower()
                if search == 'name':
                    column = 'name'
                # elif search == 'fathername':
                #     column = 'fathersname'
                elif search == 'dob':
                    column = 'nepdate'
                elif search == 'countryName':
                    column = ''
                # elif search == 'citizenship_no':
                #     column = 'citizenshipno'
                # elif search == 'pan_no':
                #     column = 'pannumber'
                # elif search == 'registration_no':
                #     column = 'comregnum'
                # elif search == 'passport_no':
                #     column = 'passportno'
                # elif search == 'indianembassy_no':
                #     column = 'indianembassyregno'
                # elif search == 'voterid_no':
                #     column = 'voterid'
                # elif search == 'drivinglisence_no':
                #     column = 'dlicenceidno'
                else:
                    raise Exception(f'Wrong search item : {search}')
                
                new_column = f'{column}_weight'
                weight_col = f'{column}_percent'

                required_columns.extend([column, weight_col, new_column]) # Use it if weitage value required
                # required_columns.extend([column, weight_col])
                logger.info(f'Required columns list is {required_columns}')
                new_columns_list.append(new_column)
                logger.info(f'New columns list is {new_columns_list}')
                # * Weitage calculation in given column
                # self.accuityfile.calculate_weightage
                self.accuityfile.calculate_weightage(
                    column,
                    weightage[search],
                    new_column = new_column,
                    match_item = item[search],
                    soundex = False,
                    weight_col = weight_col,
                )
                
            # df.to_excel('weitage.xlsx',index=True)
            # * Filtering data and removing columns that are not required in next iteration
            logger.info('Weightage calculation on all search list completed')
            logger.info(f"New column list ---------------{new_columns_list}")
            self.accuityfile.combine_columns_by_addition(columns=new_columns_list)

            logger.info('File comibination by adding success')
            required_columns.extend(['similarity', 'clientcode','dlicenceidno','indianembassyregno','passportno','pannumber','regnum'])
            column_data = {
                'name':'search_type',
                'values':'Account Holder'
            }
            temp_result = self.accuityfile.get_data_by_value_limit('similarity', min_value, required_columns, add_colum=True, column_data=column_data)
            if not temp_result:
                
                display(f'RESULT is empty')
                logger.info('RESULT is empty')
            else:
                # display(f'TEMP RESULT == > {temp_result}')#what to do if empty result here
                result.extend(temp_result)
                del temp_result

                logger.info('Data by minimum requirement required.')
                new_columns_list.append('similarity')
                self.file.remove_columns(new_columns_list)
                logger.info('Unneccessary columns removed')
                
                # * Generating report for unmatched for multiple and update database if single data found
                logger.info(f'Amount of result found : {len(result)}')
                logger.info(f'Weightage calculation completed by {int(time.time() - start_time)}')
   
                self.report_generation(item, item_list, df_map['client_master'], result, temp_item)
                del result

            # run_item.report_data["Unique ID"] = item['unique_id']
            run_item.report_data['Task'] = 'Execute run item: WeightageProcess'
            run_item.set_success()
            run_item.post()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
           
        display('Completed !!!! Execute Run Item: Weitage Process')

    # def report_generation(self, item, item_list, df_map, result, temp_item: dict):
    #     run_item = QRRunItem()
    #     self.notify(run_item)

    #     display(f'TEMP_ITEM KEYS===> {temp_item.keys()}')
    #     logger = run_item.logger
    #     search_list: list = item['search_list']
    #     # display(f'Item from report generation====>{item}')
    #     # if not result:
    #     #     with self.db as db:
    #     #         db.update_progess_status(item['unique_id'], 'retry')
    #     #         db.update_remarks_on_unique_id(item['unique_id'], f'No data found for mininum filter value')
    #     #         logger.info('Retry status added.')
    #     #     return

    #     df = pd.DataFrame(result)
    #     # df.to_excel('ramkumar.xlsx',index=False)
    #     result = []
    #     self.file.set_dataframe(df)
    #     name = str(item['name'])
    #     display(f'TEMP_ITEM value is {temp_item}')
    #     logger.info(f'TEMP_ITEM value is {temp_item}')
    #     for index, col in enumerate(item_list):
    #         value = item[col]
    #         display(f'THIS IS A VALUE===> {value}')
    #         self.file.insert_column_at_index(index, col, value)

    #     df_len = self.file.get_number_of_row_data()
    #     self.file.add_new_columns_to_datasheet('Result of CIB Screening', '', df_len)
    #     self.file.add_new_columns_to_datasheet('CIB Name',temp_item['Name'],df_len)
    #     self.file.add_new_columns_to_datasheet('CIB Father Name', temp_item['FatherName'],df_len)
    #     self.file.add_new_columns_to_datasheet('CIB Gender',temp_item['Gender'],df_len)
    #     self.file.add_new_columns_to_datasheet('CIB DOB',temp_item['DOB'],df_len)
    #     if 'CitizenshipDetails' in temp_item and temp_item['CitizenshipDetails'] != 'nan':
    #         # display(temp_item['CitizenshipDetails'] is not None)
    #         logger = run_item.logger
    #         citizenship = [temp_item['CitizenshipDetails']]
    #         display(f'CITIZENSHIP Details is ==>{citizenship}')
    #         logger.info(f'CITIZENSHIP Details is ==>{citizenship}')
    #         # citizen_number = ''
    #         for item in citizenship:
    #             if '|' in item:
    #                 citizen_number = item.split('|')[0]
    #                 logger.info(f'CITIZENSHIP_NUMBER==>{citizen_number}')
    #                 self.file.add_new_columns_to_datasheet('CIB Citizenship No',citizen_number,df_len)
    #                 display('New column name CIB Citizenship No is added')
    #                 logger.info('New column name CIB Citizenship No is added')

    #     if 'PANDetails' in temp_item and temp_item['PANDetails'] != 'nan':
    #         display(temp_item['PANDetails'] is not None)
    #         pan = temp_item['PANDetails']
    #         display(f'PAN DETAILS is {pan}')
    #         if '|' in pan:
    #             pan_number = pan.split('|')[0]
    #             display(f'PAN NUMBER IS ===> {pan_number}')
    #             logger.info(f'PAN NUMBER IS ===> {pan_number}')
    #             self.file.add_new_columns_to_datasheet('CIB PAN NO',pan_number,df_len)
    #             display('Successfully added the CIB PAN NO')
    #             logger.info('Successfully added the CIB PAN NO')
    #     if 'IndianEmbassyDetails' in temp_item and temp_item['IndianEmbassyDetails'] != 'nan':
    #         indianembassy = temp_item['IndianEmbassyDetails']
    #         logger.info(f'Indian Embassy Detal is {indianembassy}')
    #         if '|' in indianembassy:
    #             indianembassy_number = indianembassy.split('|')[0]
    #             self.file.add_new_columns_to_datasheet('CIB Indianembassy No',indianembassy_number,df_len)
    #             display('New column CIB Indian embassyr No is added')
    #             logger.info('New column CIB Indian embassyr No is added')
    #     if 'PassportDetails' in temp_item and temp_item['PassportDetails'] != 'nan':
    #         passport = temp_item['PassportDetails']
    #         logger.info(f'Passport Details is {passport}')
    #         if '|' in passport:
    #             passport_number = passport.split('|')[0]
    #             self.file.add_new_columns_to_datasheet('CIB passport no',passport_number,df_len)
    #             display('New column CIB passport  No is added')
    #             logger.info('New column CIB passport  No is added')
    #     if 'VoterIDDetails' in temp_item and temp_item['VoterIDDetails'] != 'nan':
    #         voter = temp_item['VoterIDDetails']
    #         logger.info(f'Voter Details is {voter}')
    #         if '|' in voter:
    #             voter_number = voter.split('|')[0]
    #             self.file.add_new_columns_to_datasheet('CIB Voter No',voter_number,df_len)
    #             display('New column CIB Voter No is added')
    #             logger.info('New column CIB Voter No is added')

    #     if 'CompanyDetails' in temp_item and temp_item['CompanyDetails'] != 'nan':
    #         reg = [temp_item['CompanyDetails']]
    #         display(f'Company DETAILS is {reg}')
    #         logger.info(f'Company DETAILS is {reg}')
    #         for item in reg:
    #             # display(f'ITEM==>{item}')
    #             item = str(item)
    #             # Check if the item is a string or a list
    #             if ',' in item:
    #                 reg_list = ast.literal_eval(item)
    #                 if isinstance(reg_list, list):
    #                     for data in reg_list:
    #                         # Check if '|' exists before splitting
    #                         if '|' in data:
    #                             regnumber = data.split('|')[0]
    #                     self.file.add_new_columns_to_datasheet('CIB Com Registration No',regnumber,df_len)
    #                     # self.file.add_new_columns_to_datasheet('Blacklisted Date',blacklist_date,df_len)
    #             else:
    #                 # Check if '|' exists before splitting
    #                 if '|' in item:
    #                     regnumber = item.split('|')[0]
    #                     # display(f'blacklist_NUMBER==>{blacklist_number}')
    #                     self.file.add_new_columns_to_datasheet('CIB Com Registration No',regnumber,df_len)
    #                     display('New column name CIB Com Registration No is added')
    #                     # self.file.add_new_columns_to_datasheet('Blacklisted Date',blacklist_date,df_len)

    #     # self.file.add_new_columns_to_datasheet('Cib citizenship no',temp_item['CitizenshipDetails'],df_len)
    #     blacklist = [temp_item['BlackLists']]
    #     for item in blacklist:
    #         list_of_blacklist = []
    #         date_of_blacklist = []
    #         # display(f'ITEM==>{item}')
    #         item = str(item)
    #         # Check if the item is a string or a list
    #         if ',' in item:
    #             black_list = ast.literal_eval(item)
    #             if isinstance(black_list, list):
    #                 for data in black_list:
    #                     # Check if '|' exists before splitting
    #                     if '|' in data:
    #                         blacklist_number = data.split('|')[1]
    #                         list_of_blacklist.append(blacklist_number)
    #                         blacklist_date = data.split('|')[2]
    #                         date_of_blacklist.append(blacklist_date)
    #                         # display(f'blacklist_NUMBER==>{blacklist_number}')
    #                 self.file.add_new_columns_to_datasheet('CIB Black Listed No',list_of_blacklist,df_len)
    #                 self.file.add_new_columns_to_datasheet('CIB Black Listed Date',date_of_blacklist,df_len)
    #         else:
    #             # Check if '|' exists before splitting
    #             if '|' in item:
    #                 blacklist_number = item.split('|')[1]
    #                 blacklist_date = item.split('|')[2]
    #                 # display(f'blacklist_NUMBER==>{blacklist_number}')
    #                 self.file.add_new_columns_to_datasheet('CIB Black Listed No',blacklist_number,df_len)
    #                 self.file.add_new_columns_to_datasheet('CIB Black Listed Date',blacklist_date,df_len)

       
    #     self.file.collect_maincode_data(df_map)
        
        
    #     if self.file.get_number_of_row_data() == 0:
           
    #         raise Exception('Inner join gives no result')

    #     self.file.set_dataframe(pd.DataFrame)
    #     # logger.info('=============================================================================')
    #     logger.info(self.file.set_dataframe(pd.DataFrame))
        
    #     # df_result.to_excel
    #     # df.to_excel('report.xlsx',index=True)
        

    # @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        # display('After Run Item: WeightageProcess')
        # Get run item created by decorator. Then notify to all components about new run item.

        # self.tasklogger.write_log_to_logger_file('After Run item: Weitage Process')
        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)
        

    def execute_run(self, df_map: dict):
        run_item = QRRunItem()
        self.notify(run_item)

        # self.tasklogger.write_log_to_logger_file('BeforeRun: Weitage Process')
        display(f'Columns of the df_map is {df_map.keys}')
        logger = run_item.logger
        # display(self.data)
        for index, x in enumerate(self.data):
            # display(x)
            logger.info(x)
            # display(index)
            # display(f'this is from execute_run weitageprocess{x}')
            try:
                self.before_run_item(x)
            except: 
                continue
            
            logger.info('Execute run item')
            # BuiltIn().run_keyword('WeightageProcess.execute_run_item', self.exe_item, x, df_map)
            self.execute_run_item(self.exe_item,x,df_map)
            self.after_run_item()
            # if index + 1 == 5:
            #     raise Exception(f"Completed")

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        logger = run_item.logger