
import os
import re
import pytz
import shutil
import subprocess
import Levenshtein
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
from Errors import WeightageParamsError
from abydos import phonetic
from Variables import BotVariable
from robot.libraries.BuiltIn import BuiltIn
from Constants import CODE_1, CODE_2, CODE_3, CODE_4, CODE_5

from qrlib.QRLogger import QRLogger
from qrlib.QREnv import QREnv


def get_weightage(elements: list[str], type: str) -> dict:
    '''
        Required value of elements as per neccessity:
            - name
            - father_name
            - gfather_name
            - citizenship_no
            - pan_no
            - registration_no
            - account_no
        Note : any other value will raise exception Errors.WeightageParamsError
        Type value:
            - account information
            - legal
            - natural
    '''
    logger = QRLogger().logger
    path = BotVariable.CONFIG_PATH + '/Weightage Distribution.xlsx'

    weights = {}
    elements = [i.strip() for i in elements]
    logger.info(f'Elements are {elements}')
    
    if type == 'account information':
        # * weightage for account information 
        logger.info('If account information available')
        df = pd.read_excel(path, sheet_name='Account information provided', skiprows=[0, 1, 2, 3])
        df = df.fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        logger.info('Filtering dataframe completed.')
        if len(elements) == 1:
            logger.info('Calculation weight for account no')
            df = df[df['condition'].str.contains('Only Account', na=False)]
            logger.info(f'1:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights['account_no'] = df.at[index, 'account number']
        else:
            logger.info('Calculation weight for account no and name')
            df = df[df['condition'].str.contains('Name and Account', na=False)]
            logger.info(f'2:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights['name'] = df.at[index, 'name']
            weights['account_no']= df.at[index, 'account number']
        return weights
    elif type == 'natural':
        # * Weightage condition for natural account
        logger.info('If account is natural.')
        df = pd.read_excel(path, sheet_name='Natural', skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
        df = df.drop(columns=df.columns[df.columns.str.contains('Assumption')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        logger.info('Filtering dataframe completed')
        logger.info(f'element length : {len(elements)}')
        
        if len(elements) == 4:
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'3:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights['name'] = df.at[index, 'name']
            weights['citizenship_no'] = df.at[index, 'citizenship number']
            weights['father_name'] = df.at[index, 'father name']
            weights['gfather_name'] = df.at[index, 'grandfather name']
        elif len(elements) == 3:
            # df = df.tail(8)
            if all(x in elements for x in ['name', 'father_name', 'gfather_name']):
                condition = 'Name, Father Name, Grandfather name'
                first, second, third = 'name', 'father_name', 'gfather_name'
                df_first, df_second, df_third = 'name', 'father name', 'grandfather name'
            elif all(x in elements for x in ['name', 'father_name', 'citizenship_no']):
                condition = 'Name, Citizenship number, Father Name'
                first, second, third = 'name', 'citizenship_no', 'father_name'
                df_first, df_second, df_third = 'name', 'citizenship number', 'father name'
            elif all(x in elements for x in ['name', 'gfather_name', 'citizenship_no']):
                condition = 'Name, Citizenship number, Grandfather name'
                first, second, third = 'name', 'citizenship_no', 'gfather_name'
                df_first, df_second, df_third = 'name', 'citizenship number', 'grandfather name'
            elif all(x in elements for x in ['citizenship_no', 'father_name', 'citizenship_no']):
                condition = 'Citizenship number, Father Name, Grandfather name'
                first, second, third = 'citizenship_no', 'father_name', 'gfather_name'
                df_first, df_second, df_third = 'citizenship number', 'father name', 'grandfather name'
            else:
                raise WeightageParamsError(elements)
            df = df[df['condition'].str.contains(condition, na=False)]
            logger.info(f'4:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights[first] = df.at[index, df_first]
            weights[second] = df.at[index, df_second]
            weights[third] = df.at[index, df_third]
        elif len(elements) == 2:
            df = df.tail(20)
            if all(x in elements for x in ['name', 'father_name']):
                condition = 'Name,Father Name'
                first, second = 'name', 'father_name'
                df_first, df_second = 'name', 'father name'
            elif all(x in elements for x in ['name', 'citizenship_no']):
                condition = 'Name,Citizenship number'
                first, second = 'name', 'citizenship_no'
                df_first, df_second = 'name', 'citizenship number'
            elif all(x in elements for x in ['name', 'gfather_name']):
                condition = 'Name,Grandfather name'
                first, second = 'name', 'gfather_name'
                df_first, df_second = 'name', 'grandfather name'
            elif all(x in elements for x in ['citizenship_no', 'father_name']):
                condition = 'Citizenship number,Father Name'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'5:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                first, second = 'citizenship_no', 'father_name'
                df_first, df_second = 'citizenship_no', 'father name'
            elif all(x in elements for x in ['citizenship_no', 'father_name']):
                condition = 'Citizenship number,Grandfather name'
                first, second = 'citizenship_no', 'gfather_name'
                df_first, df_second = 'citizenship_no', 'grandfather name'
            elif all(x in elements for x in ['citizenship_no', 'father_name']):
                condition = 'Father Name,Grandfather name'
                first, second = 'gfather_name', 'father_name'
                df_first, df_second = 'grandfather name', 'father name'
            else:
                raise WeightageParamsError(elements)
            df = df[df['condition'].str.contains(condition, na=False)]
            logger.info(f'6:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights[first] = df.at[index, df_first]
            weights[second] = df.at[index, df_second]
        else:
            if len(elements) != 1:
                raise WeightageParamsError(elements)
            element = elements[0]
            df = df.tail(5)
            df.reset_index()
            
            if element == 'name':
                condition = 'Name'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'7:Shape of dataframe is {df.shape}')
                logger.info(f'8:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['name'] = df.at[index, 'name']
            elif element == 'citizenship_no':
                condition = 'Citizenship Number'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'9:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['citizenship_no'] = df.at[index, 'citizenship number']
            elif element == 'Father Name':
                condition = 'Father Name'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'10:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['father_name'] = df.at[index, 'father name']
            elif element == 'gfather_name':
                condition = 'Grand Father'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'11:Shape of dataframe is {df.shape}')
                logger.info(f'12:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['gfather_name'] = df.at[index, 'grandfather name']
            else:
                raise WeightageParamsError(elements)
        return weights
    elif type == 'legal':
         # * Weightage condition for legal account
        df = pd.read_excel(path, sheet_name='Legal', skiprows=[0, 1, 2, 3])
        df = df.drop(columns=df.columns[df.columns.str.contains('Unnamed')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        if len(elements) == 3:
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'13:Shape of dataframe is {df.shape}')
            index = int(df.index.values[0])
            weights['name'] = df.at[index, 'name']
            weights['pan_no'] = df.at[index, 'pan number']
            weights['registration_no'] = df.at[index, 'registration number']
        elif len(elements) == 2:
            if 'name' in elements and 'pan_no' in elements:
                search = 'Name, Pan'
                first, second = 'name', 'pan_no'
                df_first, df_second = 'name', 'pan number'
            elif 'name' in elements and 'registration_no' in elements:
                search = 'Name, Registration'
                first, second = 'name', 'registration_no'
                df_first, df_second = 'name', 'registration number'
            elif 'pan_no' in elements and 'registration_no' in elements:
                search = 'Pan number, Registration'
                first, second = 'pan_no', 'registration_no'
                df_first, df_second = 'pan number', 'registration number'
            else:
                raise WeightageParamsError(elements)
            logger.info(f'Registration search is {search}')
            df = df[df['condition'].str.contains(search, na=False)]
            logger.info(f'14:Shape of dataframe is {df.shape}')
            logger.info(f'Datafarame index for two elements in legal is {df.index.values}')
            index = int(df.index.values.tolist()[0])
            weights[first] = df.at[index, df_first]
            weights[second] = df.at[index, df_second]
        else:
            df = df.tail(4)
            df.reset_index(inplace=True)
            if elements[0] == 'name':
                search = 'Name'
                first, df_first = 'name', 'name'
            elif elements[0] == 'pan_no':
                search = 'Pan'
                first, df_first = 'pan_no', 'pan number'
            elif elements[0] == 'registration_no':
                search = 'Registration'
                first, df_first = 'registration number', 'registration number'
            else:
                raise WeightageParamsError(elements)
            df = df[df['condition'].str.contains(search, na=False)]
            logger.info(f'15:Shape of dataframe is {df.shape}')
            logger.info(f'Datafarame index for only one in legal is {df.index.values}')
            index = int(df.index.values.tolist()[0])
            weights[first] = df.at[index, df_first]
        return weights
    else:
        raise WeightageParamsError(elements)