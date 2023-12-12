import re
import pandas as pd
import numpy as np
import Levenshtein
import os
from abydos import phonetic
from Variables import BotVariable
from Errors import WeightageParamsError
from robot.libraries.BuiltIn import BuiltIn
# from Constants import CODE_1, CODE_2, CODE_3, CODE_4, CODE_5
import Constants
from qrlib.QRLogger import QRLogger
from qrlib.QRUtils import display
from qrlib.QREnv import QREnv
# from FTPComponent import FTPComponent

logger = QRLogger().logger
def compare_two_stirngs_in_df(string1: str, *args, **kwargs):
    '''
        Required kwargs key value:
            string2: str ==> value that required to compare with
            soundex: bool ==> if soundex is need to be applie
    '''
    if not all(x in kwargs.keys() for x in ['string2', 'soundex']):
        return np.nan
    string2: str = str(kwargs['string2']).strip()

    string1 = re.sub(r'\s+', ' ', str(string1)).upper()
    string2 = re.sub(r'\s+', ' ', str(string2)).upper()

    try:
        string1 = str(int(float(string1)))
    except:
        pass
    
    similarity = float(Levenshtein.ratio(str(string1).strip(), string2.strip()) )
    return float(round(similarity * 100.0, 2))

def get_weightage(elements: list[str], type: str) -> dict:
    '''
        Required value of elements as per neccessity:
            - name
            - fathername
            - DOB
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
    logger.info(f'Elements====>{elements}')
    # logger = QRLogger().logger
    # path = BotVariable.CONFIG_PATH + '/Weightage Distribution.xlsx'
    #"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Weightage Distribution.xlsx"
    # current_path = os.getcwd()
    # current_path = os.getcwd()
    # path = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Weightage Distribution.xlsx'))
    #C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\Weightage Distribution.xlsx
    # path = r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Weightage Distribution.xlsx"
    # path = r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\Weightage Distribution.xlsx"
    path = os.path.join(Constants.cib_common_path,'Weightage Distribution.xlsx')
    
    weights = {}
    elements = [i.strip() for i in elements]
    logger.info(f'Elements are {elements}')
    
    
    if type == 'individual':
        # * Weightage condition for natural account
        logger.info('If account is natural.')
        df = pd.read_excel(path, sheet_name='Natural', skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
        df = df.drop(columns=df.columns[df.columns.str.contains('Assumption')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        logger.info('Filtering dataframe completed')
        logger.info(f'element is : {elements}')
        logger.info(f'element length : {len(elements)}')
        
        if len(elements) == 4:
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'3:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights['name'] = df.at[index, 'name']
            logger.info(f'WITAGE COLUMN ===> {weights}')
            if 'citizenship_no' in elements:
                weights['citizenship_no'] = df.at[index, 'id']
            elif 'pan_no' in elements:
                weights['pan_no'] =  df.at[index, 'id']
            elif 'passport_no' in elements:
                weights['passport_no'] = df.at[index, 'id']
            elif 'drivinglisence_no' in elements:
                weights['drivinglisence_no'] = df.at[index, 'id']
            elif 'voterid_no' in elements:
                weights['voterid_no'] = df.at[index, 'id']
            elif 'indianembassy_no' in elements:
                weights['indianembassy_no'] = df.at[index, 'id']
            # if  weights['citizenship_no']:
            #     weights['citizenship_no'] = df.at[index, 'id']
            # elif weights['pan_no']:
            # weights['pan_no'] =  df.at[index, 'id']
            weights['fathername'] = df.at[index, 'father name']
            weights['dob'] = df.at[index, 'dob']
        elif len(elements) == 3:
            elements = [element.lower() for element in elements]
            if all(x in elements for x in ['name', 'fathername', 'dob']):
                condition = 'Name, Father Name, DOB'
                first, second, third = 'name', 'fathername', 'dob'
                df_first, df_second, df_third = 'name', 'father name', 'dob'
            elif all(x in elements for x in ['name', 'fathername', 'citizenship_no']):
                condition = 'Name, id, Father Name'
                first, second, third = 'name', 'citizenship_no', 'fathername'
                df_first, df_second, df_third = 'name', 'id', 'father name'
            elif all(x in elements for x in ['name', 'dob', 'citizenship_no']):
                condition = 'Name, id, DOB'
                first, second, third = 'name', 'citizenship_no', 'dob'
                df_first, df_second, df_third = 'name', 'id', 'dob'
            elif all(x in elements for x in ['citizenship_no', 'fathername', 'citizenship_no']):
                condition = 'id, Father Name, DOB'
                first, second, third = 'citizenship_no', 'fathername', 'dob'
                df_first, df_second, df_third = 'id', 'father name', 'dob'
            else:
                raise WeightageParamsError(elements)
            df = df[df['condition'].str.contains(condition, na=False)]
            logger.info(f'4:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            weights[first] = df.at[index, df_first]
            weights[second] = df.at[index, df_second]
            weights[third] = df.at[index, df_third]
        elif len(elements) == 2:
            elements = [element.lower() for element in elements]
            df = df.tail(20)
            if all(x in elements for x in ['name', 'fathername']):
                condition = 'Name,Father Name'
                first, second = 'name', 'fathername'
                df_first, df_second = 'name', 'father name'
            elif all(x in elements for x in ['name', 'citizenship_no']):
                condition = 'Name,id'
                first, second = 'name', 'citizenship_no'
                df_first, df_second = 'name', 'id'
            elif all(x in elements for x in ['name', 'dob']):
                condition = 'Name,DOB'
                first, second = 'name', 'dob'
                df_first, df_second = 'name', 'dob'
            elif all(x in elements for x in ['citizenship_no', 'fathername']):
                condition = 'id,Father Name'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'5:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                first, second = 'citizenship_no', 'fathername'
                df_first, df_second = 'citizenship_no', 'father name'
            elif all(x in elements for x in ['citizenship_no', 'fathername']):
                condition = 'id,DOB'
                first, second = 'citizenship_no', 'dob'
                df_first, df_second = 'citizenship_no', 'dob'
            elif all(x in elements for x in ['citizenship_no', 'fathername']):
                condition = 'Father Name,DOB'
                first, second = 'dob', 'fathername'
                df_first, df_second = 'dob', 'father name'
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
                condition = 'id'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'9:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['citizenship_no'] = df.at[index, 'id']
            elif element == 'Father Name':
                condition = 'Father Name'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'10:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['fathername'] = df.at[index, 'father name']
            elif element == 'dob':
                condition = 'DOB'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'11:Shape of dataframe is {df.shape}')
                logger.info(f'12:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])
                weights['dob'] = df.at[index, 'dob']
            elif element == 'pan_no':
                condition = 'id'
                df = df[df['condition'].str.contains(condition, na=False)]
                logger.info(f'9:Shape of dataframe is {df.shape}')
                index = int(df.index.values.tolist()[0])

            else:
                raise WeightageParamsError(elements)
        return weights
    elif type == 'institutions':
         # * Weightage condition for legal account
        df = pd.read_excel(path, sheet_name='Legal', skiprows=[0, 1, 2, 3])
        df = df.drop(columns=df.columns[df.columns.str.contains('Unnamed')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        if len(elements) == 3:
            logger.info(f'All Information are ==>{elements}')
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'13:Shape of dataframe is {df.shape}')
            index = int(df.index.values[0])
            weights['name'] = df.at[index, 'name']
            weights['pan_no'] = df.at[index, 'pan number']
            weights['registration_no'] = df.at[index, 'registration number']
        elif len(elements) == 2:

            logger.info(f'Length of the element is {len(elements)}')
            logger.info(f'ELEMENTS ARE {elements}')
            elements = [element.lower() for element in elements]
            logger.info(f'ELEMENTS AFTER LOWERING ARE {elements}')
            if 'name' in elements and 'pan_no' in elements:
                search = 'Name, Pan'
                first, second = 'name', 'pan_no'
                df_first, df_second = 'name', 'pan number'
            elif 'name' in elements and 'registration_no' in elements:
                logger.info(f'NAME AND REGISTRATION NUMBER IS FOUND ')
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
    
def get_accuity_weightage(elements: list[str], type: str) -> dict:
    '''
        Required value of elements as per neccessity:
            - name
            - dob
            - countryName
            
            
        Note : any other value will raise exception Errors.WeightageParamsError
        Type value:
            - legal
            - natural
    '''
    logger.info(f'Elements====>{elements}')
    path = os.path.join(Constants.Accuity_Weitage_Path,'ACCUITY SCREENING WEIGHTAGE.xlsx')
    
    weights = {}
    elements = [i.strip() for i in elements]
    logger.info(f'Elements are {elements}')
    
    display(f'Type is =====================>{type}')
    if type == 'natural':
        # * Weightage condition for natural account
        logger.info('If account is natural.')
        # df = pd.read_excel(path, sheet_name='NATURAL', skiprows=[0, 1, 2, 3,4,7,10]) 
        df = pd.read_excel(path, sheet_name='NATURAL', skiprows=[0, 1, 2, 3,4]) 

        # df = df.drop(columns=df.columns[df.columns.str.contains('Assumption')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        display(df.head(10))
        display(f'Columns of the dataframe is {df.columns}')
        logger.info('Filtering dataframe completed')
        display('Filtering dataframe completed')
        display(f'element is :{elements}')
        display(f'element length is {len(elements)}')
        # logger.info(f'element is : {elements}')
        # logger.info(f'element length : {len(elements)}')
        
        if len(elements) == 3:
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'3:Shape of dataframe is {df.shape}')
            display(f'Shape of the dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            display(f'Index is {index}')
            display(f'Dataframe is when lenth is 3  {df.head(10)}')
            weights['name'] = df.at[index, 'name']
            display(f'WITAGE COLUMN ===>{weights}')
            weights['dobs'] = df.at[index,'dob']
            weights['countryName'] = df.at[index,'country name']
            logger.info(f'WITAGE COLUMN ===> {weights}')
            # if 'citizenship_no' in elements:
            #     weights['citizenship_no'] = df.at[index, 'id']
            # elif 'pan_no' in elements:
            #     weights['pan_no'] =  df.at[index, 'id']
            # elif 'passport_no' in elements:
            #     weights['passport_no'] = df.at[index, 'id']
            # elif 'drivinglisence_no' in elements:
            #     weights['drivinglisence_no'] = df.at[index, 'id']
            # elif 'voterid_no' in elements:
            #     weights['voterid_no'] = df.at[index, 'id']
            # elif 'indianembassy_no' in elements:
            #     weights['indianembassy_no'] = df.at[index, 'id']
            # # if  weights['citizenship_no']:
            # #     weights['citizenship_no'] = df.at[index, 'id']
            # # elif weights['pan_no']:
            # # weights['pan_no'] =  df.at[index, 'id']
            # weights['fathername'] = df.at[index, 'father name']
            # weights['dob'] = df.at[index, 'dob']
        elif len(elements) == 1:
            elements = [element.lower() for element in elements]
            if all(x in elements for x in ['name']):
                condition = 'Name'
                first = 'name'
                df_first = 'name'
            # elif all(x in elements for x in ['name', 'fathername', 'citizenship_no']):
            #     condition = 'Name, id, Father Name'
            #     first, second, third = 'name', 'citizenship_no', 'fathername'
            #     df_first, df_second, df_third = 'name', 'id', 'father name'
            # elif all(x in elements for x in ['name', 'dob', 'citizenship_no']):
            #     condition = 'Name, id, DOB'
            #     first, second, third = 'name', 'citizenship_no', 'dob'
            #     df_first, df_second, df_third = 'name', 'id', 'dob'
            # elif all(x in elements for x in ['citizenship_no', 'fathername', 'citizenship_no']):
            #     condition = 'id, Father Name, DOB'
            #     first, second, third = 'citizenship_no', 'fathername', 'dob'
            #     df_first, df_second, df_third = 'id', 'father name', 'dob'
            else:
                raise WeightageParamsError(elements)
            display(f'Condition one is {condition}')
            display(f'Weights is {weights}')
            df = df[df['condition'].str.contains(condition, na=False)]
            logger.info(f'4:Shape of dataframe is {df.shape}')
            index = int(df.index.values.tolist()[0])
            display(f'Index is {index}')
            weights[first] = df.at[index, df_first]
            display(f'Weitage of one element is {weights}')
            display(f'Length one dataframe is {df}')
            # weights[second] = df.at[index, df_second]
            # weights[third] = df.at[index, df_third]
        elif len(elements) == 2:
            elements = [element.lower() for element in elements]
            display(f'Elements is {elements}')
            # df = df.tail(20)
            display(f'Element of lenth of element 2 is {df.head(20)}')
            if all(x in elements for x in ['name', 'dobs']):
                condition = 'Name,DOB'
                first, second = 'name', 'dobs'
                df_first, df_second = 'name', 'dob'
                # first, second = 'name', 'dob'
                # df_first, df_second = 'name', 'dobs'
                
            elif all(x in elements for x in ['name', 'countryname']):
                condition = 'Name,Country Name'
                first, second = 'name', 'countryname'
                df_first, df_second = 'name', 'country name'
                display(f'First Name is {first} and second is countryname {second}')

           
            else:
                raise WeightageParamsError(elements)
            display(f'Condition is {condition}')
            # display(f'Weights is {weights}')
            df = df[df['condition'].str.contains(condition, na=False)]
            display(f'Data of the two lenth is {df.head()}')
            display(f'Shape of the dataframe is {df.shape}')
            logger.info(f'6:Shape of dataframe is {df.shape}')
            # display(int(df.index.values.tolist()[0]))
            display(df.head(10))
            # index = int(df.index.values.tolist()[0])
            index = int(df.index.values.tolist()[0])
            # index = 9
            display(f'Index of the lenth two is {index}')
            weights[first] = df.at[index, df_first]
            weights[second] = df.at[index, df_second]
            
        else:
            # if len(elements) != 1:
            #     raise WeightageParamsError(elements)
            # element = elements[0]
            # df = df.tail(5)
            # df.reset_index()
            
            # if element == 'name':
            #     condition = 'Name'
            #     df = df[df['condition'].str.contains(condition, na=False)]
            #     logger.info(f'7:Shape of dataframe is {df.shape}')
            #     logger.info(f'8:Shape of dataframe is {df.shape}')
            #     index = int(df.index.values.tolist()[0])
            #     weights['name'] = df.at[index, 'name']
            # elif element == 'citizenship_no':
            #     condition = 'id'
            #     df = df[df['condition'].str.contains(condition, na=False)]
            #     logger.info(f'9:Shape of dataframe is {df.shape}')
            #     index = int(df.index.values.tolist()[0])
            #     weights['citizenship_no'] = df.at[index, 'id']
            # elif element == 'Father Name':
            #     condition = 'Father Name'
            #     df = df[df['condition'].str.contains(condition, na=False)]
            #     logger.info(f'10:Shape of dataframe is {df.shape}')
            #     index = int(df.index.values.tolist()[0])
            #     weights['fathername'] = df.at[index, 'father name']
            # elif element == 'dob':
            #     condition = 'DOB'
            #     df = df[df['condition'].str.contains(condition, na=False)]
            #     logger.info(f'11:Shape of dataframe is {df.shape}')
            #     logger.info(f'12:Shape of dataframe is {df.shape}')
            #     index = int(df.index.values.tolist()[0])
            #     weights['dob'] = df.at[index, 'dob']
            # elif element == 'pan_no':
            #     condition = 'id'
            #     df = df[df['condition'].str.contains(condition, na=False)]
            #     logger.info(f'9:Shape of dataframe is {df.shape}')
            #     index = int(df.index.values.tolist()[0])

            # else:
            raise WeightageParamsError(elements)
        return weights
    elif type == 'legal':
         # * Weightage condition for legal account
        df = pd.read_excel(path, sheet_name='LEGAL', skiprows=[0, 1, 2])
        # df = pd.read_excel(path, sheet_name='LEGAL', skiprows=[0, 1, 2, 3])
        df = df.drop(columns=df.columns[df.columns.str.contains('Unnamed')])
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all').fillna('')
        df.columns = [ str(x).strip().lower() for x in df.columns.to_list()]
        if len(elements) == 2:
            logger.info(f'All Information are ==>{elements}')
            df = df[df['condition'].str.contains('All information', na=False)]
            logger.info(f'13:Shape of dataframe is {df.shape}')
            index = int(df.index.values[0])
            weights['name'] = df.at[index, 'name']
            weights['countryName'] = df.at[index, 'country name']
            # weights['registration_no'] = df.at[index, 'registration number']
        elif len(elements) == 1:

            logger.info(f'Length of the element is {len(elements)}')
            logger.info(f'ELEMENTS ARE {elements}')
            elements = [element.lower() for element in elements]
            logger.info(f'ELEMENTS AFTER LOWERING ARE {elements}')
            weights['name'] = df.at[index,'name']
            # if 'name' in elements and 'pan_no' in elements:
            #     search = 'Name,'
            #     first, second = 'name', 'pan_no'
            #     df_first, df_second = 'name', 'pan number'
            # elif 'name' in elements and 'registration_no' in elements:
            #     logger.info(f'NAME AND REGISTRATION NUMBER IS FOUND ')
            #     search = 'Name, Registration'
            #     first, second = 'name', 'registration_no'
            #     df_first, df_second = 'name', 'registration number'
            # elif 'pan_no' in elements and 'registration_no' in elements:
            #     search = 'Pan number, Registration'
            #     first, second = 'pan_no', 'registration_no'
            #     df_first, df_second = 'pan number', 'registration number'
            # else:
            #     raise WeightageParamsError(elements)
            logger.info(f'Registration search is {search}')
            df = df[df['condition'].str.contains(search, na=False)]
            logger.info(f'14:Shape of dataframe is {df.shape}')
            logger.info(f'Datafarame index for two elements in legal is {df.index.values}')
            index = int(df.index.values.tolist()[0])
            # index = 9
            weights[first] = df.at[index, df_first]
            # weights[second] = df.at[index, df_second]
        else:
            df = df.tail(4)
            df.reset_index(inplace=True)
            if elements[0] == 'name':
                search = 'Name'
                first, df_first = 'name', 'name'
            elif elements[0] == 'country name':
                search = 'countryName'
                first, df_first = 'countryName', 'country name'
            # elif elements[0] == 'registration_no':
            #     search = 'Registration'
            #     first, df_first = 'registration number', 'registration number'
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