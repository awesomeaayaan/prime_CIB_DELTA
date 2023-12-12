from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn
from Errors import DataNotFoundError
from datetime import datetime
from EmailComponent import EmailComponent
from DBComponent import DBComponent
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import PatternFill
import ast
import os
import re
import time
import Utils
import sqlite3
import Constants
import csv
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

display = BuiltIn().log_to_console

def cal_weights(row, *args):
    return float(row) * float(args)
 
class AccuityFileComponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.dataframe = pd.DataFrame()
        self.db = DBComponent()
        self.email = EmailComponent()
        self.file_path = os.path.join(Constants.ACCUITY_PATH,'ac_UPIDGWL.ZIP')

    def set_dataframe(self, df: pd.DataFrame = pd.DataFrame()):
        self.dataframe = df
        # display(f'DATAFRAME FROM FILE COMPONENT{df.columns}')
    def extract_today_date():
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    def collect_maincode_data(self, other_df: pd.DataFrame):
        logger = self.run_item.logger
        client_code = self.dataframe['clientcode'].to_list()
        # display(f'CLIENT_CODE==>{client_code}')
        client_code = [str(x).zfill(Constants.CLIENTCODE_LENGTH) for x in client_code]
        result = other_df[other_df['clientcode'].isin(client_code)][['clientcode', 'maincode', 'branchcode', 'isblocked', 'name','actypedesc','remarks']]
        display(f'RESULT_COLUMN ARE ==> {result.columns}')
        result.rename(columns={'name':'Account Holder'}, inplace=True)
        self.dataframe = pd.merge(self.dataframe, result, left_on='clientcode', right_on='clientcode', how='inner')
        self.change_status_column_value()
        display(self.dataframe.head())
        display(self.dataframe.columns)
        self.dataframe.to_excel('accuity_matched_report.xlsx',index=False)
        
    def get_columns_name_of_sheet(self) -> list:
        return self.dataframe.columns.to_list()
    
    def change_status_column_value(self, col_name: str = 'isblocked', length: int = 0):
        logger = self.run_item.logger
        logger.info(f'Given input length is {length}')
        columns = self.dataframe.columns.to_list()
        if col_name in columns:
            self.dataframe.rename(columns={col_name:'CBS Account Status'}, inplace=True)
            self.dataframe['CBS Account Status'] = self.dataframe['CBS Account Status'].apply(lambda x : Constants.REVRSE_RESTRICTION[str(x).strip().lower()]
                if str(x).strip().lower() in Constants.REVRSE_RESTRICTION.keys() else 'null')
            

    def extract_zipfile(self):
        download_directory = f'{Constants.ACCUITY_PATH}'
        zip_file = os.listdir(download_directory)
        # zip_files = [file for file in zip_file if file.endswith('.zip')]
        display(f'zip file list is ==> {zip_file}')
        for file in zip_file:
            zip_file_path = os.path.join(download_directory,file)
            extract_directory = download_directory
            with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
                zip_ref.extractall(extract_directory)
        display('Successfully extract the zip files in its location')

    def remove_the_file_from_directory(self):
        dir_path = f'{Constants.ACCUITY_PATH}'
        files = os.listdir(dir_path)
        for file_name in files:
            file_path = os.path.join(dir_path,file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        display('successfully remove the file from the directory')

    def check_file_downloaded_or_not(self):
        while True:
            file_exists = os.path.exists(self.file_path)
            if file_exists:
                break
    def insert_column_at_index(self, index: int, column: str, value: str):
        logger = self.run_item.logger
        column = column.title()
        # display(f'THIS IS FROM INSERT COLUMN AT INDEX:  {column}====>{value}')
        self.dataframe.insert(index, column, value)
        logger.info('Column insertion successful')

    def add_new_columns_to_datasheet(self, col_name: str, values, length: int = 0):
        '''
            Must contains total number of values
        '''
        logger = self.run_item.logger
        # values = str(values).strip()
        logger.info(f'Given input length is {length}')
        display(f'Columns is {col_name}')
        display(f'given input length is {length}')
        display(f'Value is {values}')
        if not isinstance(values, list):
            values = [str(values).strip() for _ in range(length)]
        display(self.dataframe.shape[0])
        display(f'Value is {values}')
        display(f'Value length is {len(values)}')
        # if self.dataframe.shape[0] != len(values):
        #     logger.error(f'Values length is not equals to {self.dataframe.shape[0]}')
        #     return False
        logger.info('Adding new columns with values')
        if len(values) >1:
            # values = [item + '&' for item in values]
            display(f'List value is ==> {values}')
            if all(str(val).isspace() for val in values):
                # default_value = ''
                self.dataframe['col_name'] = values[0]
            else:
                values = [' '.join(values)]
                display(f'Values in list is {values}')
                display(f'Valus is {values[0]}')
                self.dataframe[col_name] = values[0]
        else:
            values = values
            self.dataframe[col_name] = values
        return True
    
    def add_new_columns_to_datasheet(self, col_name: str, values, length: int = 0):
        '''
            Must contains total number of values
        '''
        logger = self.run_item.logger
        # values = str(values).strip()
        logger.info(f'Given input length is {length}')
        display(f'Columns is {col_name}')
        display(f'given input length is {length}')
        display(f'Value is {values}')
        if not isinstance(values, list):
            values = [str(values).strip() for _ in range(length)]
        display(self.dataframe.shape[0])
        display(f'Value is {values}')
        display(f'Value length is {len(values)}')
        # if self.dataframe.shape[0] != len(values):
        #     logger.error(f'Values length is not equals to {self.dataframe.shape[0]}')
        #     return False
        logger.info('Adding new columns with values')
        if len(values) >1:
            # values = [item + '&' for item in values]
            display(f'List value is ==> {values}')
            if all(str(val).isspace() for val in values):
                # default_value = ''
                self.dataframe['col_name'] = values[0]
            else:
                values = [' '.join(values)]
                display(f'Values in list is {values}')
                display(f'Valus is {values[0]}')
                self.dataframe[col_name] = values[0]
        else:
            values = values
            self.dataframe[col_name] = values
        return True
    
    def get_number_of_row_data(self, df=pd.DataFrame()) -> int:
        return self.dataframe.shape[0]
    def calculate_weightage(self, column: str, value: int, by_match: bool=True,  df: pd.DataFrame = pd.DataFrame(), **kwargs):
        '''
            Required kwargs value:
                new_column: string
                match_item: string
                soundex: boolean
                weight_col: string
        '''
        start_time = time.time()
        logger = self.run_item.logger
        weight_col = kwargs['weight_col']
        float_weight = float(value/100)
        logger.info(f'Columns : {self.dataframe.columns.to_list()}')

        required_data = ['new_column', 'match_item', 'soundex']
        if not all(x in kwargs.keys() for x in required_data):
            raise Exception(f'{required_data} datas are required')
        
        new_column = str(kwargs['new_column'])

        if df.empty:
           was_empty = True
           df = self.dataframe
        else:
            was_empty = False

        if by_match:
            soundex: bool = kwargs['soundex']
            df[weight_col] = df[column].apply(
                Utils.compare_two_stirngs_in_df,
                string2 = str(kwargs['match_item']),
                soundex = soundex
            )
            column = weight_col
    
        logger.info(f'Making sure {column} column is int or float data type')
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        df[new_column] = df[column] * float_weight
        
        logger.info(f'Dataframe shapt = {df.shape}')
        if was_empty:
            self.dataframe = df
        finish_time = time.time()
        logger.info(f'Time consumed for weightage calculation of {column} is {int(finish_time - start_time)}.')
        logger.info(f"Weightage dataframe columns: {df.columns}")
        return df
    
    def combine_columns_by_addition(self,columns: list[str], new_col_name: str='similarity'):#hereichange
        logger = self.run_item.logger
        logger.info('Add up the values of each column')
        logger.info(self.dataframe)
        column_sum = self.dataframe[columns].sum(axis=1)
        logger.info('Create a new column with the sum values')
        self.dataframe[new_col_name] = column_sum
        result_cib = self.dataframe
        display(f'This is the column ==> {result_cib.columns}')
        # if result_cib['similarity'] <= 90.00:
        # result = result_cib[result_cib['similarity'] <= 90.00]
        # result.drop(columns=[],inplace=True)
        # self.db.insert_report_not_matched_with_cib_data(result)
        # res = result_cib[result_cib['total'] > 90.000]
        # res.to_excel('cib_result.xlsx')
        # print(self.dataframe)
        # display(F'FILE COMPONENT DATAFRAME FROM COMBINE COLUMN BY ADDITION{self.dataframe.columns}')

    def get_data_by_value_limit(self, column: str,
                                value: float or int,
                                required_columns: list[str],
                                add_colum: bool = False,
                                column_data: dict = {}) -> list[dict]:
        '''
        key value pair in column_data parameter:
            name: str, name of column going to be added
            values: Any, value of data to be inserted
        '''
        logger = self.run_item.logger
        display(f'required columns = {required_columns}')
        query = f'{column} > {value}'
        logger.info('==========Get data by value limi is called==========')
        required_columns.append(column)
        # try:
        #     res = self.dataframe[self.dataframe[column] == 100.0]
        #     if res.shape[0] == 1:
        #         logger.info('Single data found from data frame.')
        #         res = res[required_columns]
        #         if add_colum and column_data:
        #             column_name = column_data['name']
        #             column_values = column_data['values']
        #             res.insert(0, column_name, column_values)
        #         res = res.to_dict(orient='records')
        #         return res
        #     del res
        #     logger.info('Data with 100 percent match did not found.')
        # except Exception as e:
        #     logger.info(e)
        # if self.dataframe[self.dataframe[column] > float(value)]:
        result = self.dataframe[self.dataframe[column] > float(value)]
        # if result is not None:
        # display(f'RESULT COLUMN ARE == > {result.columns}')
        logger.info('Dataframe query successfull.')
        display(f'Dataframe columns = {self.dataframe.columns.to_list()}')
        result = result[required_columns]
        # display(f'RESULT COLUMN ARE == > {result.columns}')
        logger.info(f'add_column = {add_colum}, column_data = {column_data}')
        if add_colum and column_data:
            column_name = column_data['name']
            column_values = column_data['values']
            result.insert(0, column_name, column_values)
        display(f'result columns1 = {result.columns.to_list()}')
        if 'maincode' in result.columns.to_list():
            result.rename(columns={'maincode':'account_no'}, inplace=True)
        display(f'result columns2 = {result.columns.to_list()}')
        result  = result.to_dict(orient='records')
        logger.info('List of dictionary ready from dataframe.')
        return result
    
    def collect_user_reqiured_data(self, user_data: dict) -> dict:#handle cib black list incremental data
        # columns = user_data.keys()
       
        # def filter_name(name: str) -> str:
        #     # * Regex to find correct name using regex pattern(Only for name)
        #     res = re.match("[a-zA-Z .()_\\\/&'+-]*", name)
        #     if res and (name.find('None') < 0):
        #         name = res.group()
        #     else:
        #         name = ''
        #     return name.strip()

        logger = self.run_item.logger
        logger.info('Combining personal information name')
        columns = user_data.keys()
        display(f'columns is {columns}')
        search_list = []
        account_nature = [i for i in user_data.keys() if i.find('Gender') != -1]
        account_nature = str(user_data[account_nature[0]]).lower().strip()
        if account_nature:
            name = user_data.get('name')
            search_list.append('name') if name else None

            gender = user_data.get('Gender')

            dob = user_data.get('dobs')
            search_list.append('dobs') if dob  else None

            countryName = user_data.get('countryName')
            search_list.append('countryName') if countryName else None
            return{
                'account_nature':'natural',
                'Gender':gender,
                'name':str(name).strip(),
                'dobs':str(dob).strip(),
                'countryName':str(countryName).strip(),
                'search_list':search_list
            }
        # elif account_nature is None:
        else:
            name = user_data.get('name')
            search_list.append('name') if name else None

            countryName = user_data.get('countryName')
            search_list.append('countryName') if countryName else None
            return{
                'account_nature':'Legal',
                'name':str(name).strip(),
                'countryName':str(countryName).strip(),
                'search_list':search_list
            }
        # account_nature = [i for i in user_data.keys() if i.find('Account_Nature') >= 0]
        # account_nature = str(user_data[account_nature[0]]).lower().strip()
        # logger.info(f'Nature of account is {account_nature}')
        # if account_nature == 'individual':
        #     name = user_data.get('Name')
        #     search_list.append('name') if name and (user_data['Account_Nature'] == 'Individual') else None
        #     # display(f'this is search list{search_list}')

        #     father_name = user_data.get('FatherName')
        #     search_list.append('fathername') if father_name and (user_data['Account_Nature'] == 'Individual') else None

    def read_the_extracted_file(self):
        # xml_file = r"D:\primeaccuityScreening\ac_UPIDGWL1\ENTITY.XML"
        xml_file_path = f'{Constants.ACCUITY_PATH}'
        xml_file = os.path.join(xml_file_path,'ENTITY.XML')
        # Parse the XML data
        root = ET.parse(xml_file) 

        # Create empty lists to store data
        entity_data = []
        columns = ['id', 'name', 'listId', 'listCode', 'entityType', 'createdDate', 'lastUpdateDate', 'source', 'OriginalSource','dobs','Alias','OtherID','NATIONAL NO', 'pob','title', 'OtherInformation', 'DirectID', 'EntityLevel', 'NameSource','Org_PID','Gender', 'OriginalID','Relationship', 'SubCategory','address1', 'city', 'state', 'stateName', 'country', 'countryName','province','postalCode','Status']

        # Extract data from XML and append to the entity_data list
        for entity in root.findall('./entities/entity'):
            entity_dict = {}
            entity_dict['id'] = entity.get('id')
            entity_dict['name'] = entity.find('name').text
            entity_dict['listId'] = entity.find('listId').text
            entity_dict['listCode'] = entity.find('listCode').text
            entity_dict['entityType'] = entity.find('entityType').text
            entity_dict['createdDate'] = entity.find('createdDate').text
            entity_dict['lastUpdateDate'] = entity.find('lastUpdateDate').text
            entity_dict['source'] = entity.find('source').text
            entity_dict['OriginalSource'] = entity.find('OriginalSource').text
            entity_dict['dobs'] = entity.find('dobs/dob').text if entity.find('dobs/dob') is not None else ''
            entity_dict['pob'] = entity.find('pobs/pob').text if entity.find('pobs/pob') is not None else ''

            aliases_element = entity.find('aliases/alias[@type="Alias"]')
            entity_dict['Alias'] = aliases_element.text if aliases_element is not None else ''
            # OtherID
            other_id_element = entity.find('ids/id[@type="OtherID"]')
            entity_dict['OtherID'] = other_id_element.text if other_id_element is not None else ''
            # entity_dcit['OtherID'] = entity.find('ids/id[@type="OtherID"]').text if entity.find('ids/id[@type = "OtherID"]') is not None else ''
            # NATIONAL NO
            national_no_element = entity.find('ids/id[@type="NATIONAL NO"]')
            entity_dict['NATIONAL NO'] = national_no_element.text if national_no_element is not None else ''
            # entity_dicts['NATIONAL NO'] = entity.find('ids/id[@type="NATIONAL NO"]').text if entity.find('ids/id[@type = "NATIONAL NO"]') is not None else ''
            entity_dict['title'] = entity.find('titles/title').text if entity.find('titles/title') is not None else ''
            entity_dict['OtherInformation'] = entity.find('sdfs/sdf[@name="OtherInformation"]').text if entity.find('sdfs/sdf[@name="OtherInformation"]') is not None else ''
            entity_dict['DirectID'] = entity.find('sdfs/sdf[@name="DirectID"]').text if entity.find('sdfs/sdf[@name="DirectID"]') is not None else ''
            entity_dict['EntityLevel'] = entity.find('sdfs/sdf[@name="EntityLevel"]').text if entity.find('sdfs/sdf[@name="EntityLevel"]') is not None else ''
            # entity_dict['EntityLevel'] = entity.find('sdfs/sdf[@name="EntityLevel"]').text if entity.find('sdfs/sdf[@name="EntityLevel"]') is not None else ''
            entity_dict['NameSource'] = entity.find('sdfs/sdf[@name="NameSource"]').text if entity.find('sdfs/sdf[@name="NameSource"]') is not None else ''
            entity_dict['Org_PID'] = entity.find('sdfs/sdf[@name="Org_PID"]').text if entity.find('sdfs/sdf[@name="Org_PID"]') is not None else ''
            entity_dict['Gender'] = entity.find('sdfs/sdf[@name="Gender"]').text if entity.find('sdfs/sdf[@name="Gender"]') is not None else ''
            entity_dict['OriginalID'] = entity.find('sdfs/sdf[@name="OriginalID"]').text if entity.find('sdfs/sdf[@name="OriginalID"]') is not None else ''
            entity_dict['Relationship'] = entity.find('sdfs/sdf[@name="Relationship"]').text if entity.find('sdfs/sdf[@name="Relationship"]') is not None else ''
            entity_dict['SubCategory'] = entity.find('sdfs/sdf[@name="SubCategory"]').text if entity.find('sdfs/sdf[@name="SubCategory"]') is not None else ''
            entity_dict['address1'] = entity.find('addresses/address/address1').text if entity.find('addresses/address/address1') is not None else ''
            entity_dict['city'] = entity.find('addresses/address/city').text if entity.find('addresses/address/city') is not None else ''
            entity_dict['state'] = entity.find('addresses/address/state').text if entity.find('addresses/address/state') is not None else ''
            entity_dict['stateName'] = entity.find('addresses/address/stateName').text if entity.find('addresses/address/stateName') is not None else ''
            entity_dict['country'] = entity.find('addresses/address/country').text if entity.find('addresses/address/country') is not None else ''
            entity_dict['countryName'] = entity.find('addresses/address/countryName').text if entity.find('addresses/address/countryName') is not None else ''
            entity_dict['province'] = entity.find('addresses/address/province').text if entity.find('addresses/address/province') is not None else ''
            entity_dict['postalCode'] = entity.find('addresses/address/postalCode').text if entity.find('addresses/address/postalCode') is not None else ''
            entity_dict['Status'] = 'new'

            entity_data.append(entity_dict)


        # Create DataFrame
        df = pd.DataFrame(entity_data, columns=columns)
        return df
        # df.to_excel('accuity_data.xlsx',index=False)
        # Display DataFrame
        # print(df)
            