import os
from pathlib import Path

localpath = str(Path.home())
cib_common_path = os.path.join(localpath,'Documents','Robotic Process Automation','cib_delta')
Accuity_Weitage_Path = os.path.join(localpath,'Documents','Robotic Process Automation','accuity_document')
ACCUITY_PATH = os.path.join(localpath,'Documents','Robotic Process Automation','accuity_data')
ACCUITY_DB_NAME = os.path.join(localpath,'Documents','Robotic Process Automation','accuity_database','accuity_screening.db')
ACCUITY_TABLE_NAME = 'ACCUITY_DATA'
ACCUITY_REPORT_PATH = os.path.join(cib_common_path,'Accuity_screening_report')

DB_NAME = os.path.join(cib_common_path, 'database','cib_delta_screening.db')
CIB_USER_TABLE_NAME = 'cib_users'


REPORT = 'Individual_data'
REPORT_INSTITUTE = 'Institutional_data'

REPORT_PATH = os.path.join(cib_common_path,'Email')
FINAL_REPORT = os.path.join(REPORT_PATH, 'file.xlsx')
FOLLOW_UP_PATH = os.path.join(cib_common_path,'Follow_up_email')
FOLLOW_UP_REPORT = os.path.join(FOLLOW_UP_PATH,'followup_file.xlsx')

COMPLIANCE_FILE_PATH = os.path.abspath(os.path.join(cib_common_path,'Compliance'))
COMPLIANCE_REPORT_INDIVIDUAL = os.path.join(COMPLIANCE_FILE_PATH,'summary_individual_report.xlsx')
COMPLIANCE_REPORT_INSTITUTIONAL = os.path.join(COMPLIANCE_FILE_PATH,'summary_institutional_report.xlsx')

hash_code_file_path = os.path.join(cib_common_path,'config','hashcode.txt')

FLAG_FILE_PATH = os.path.join(cib_common_path,'first_run_flag.txt')

HASH_FILE_PATH = os.path.join(cib_common_path,'config','hashcode.json')


TIMEOUT = "30"
# current_path = os.getcwd()
# # DB_PATH = os.path.join(os.getcwd(), 'output')
# # DB_PATH = r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents'
# COMMON_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents'))
# DB_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents'))
# DB_NAME = os.path.join(DB_PATH, 'cib_delta_screening.db')
# CIB_USER_TABLE_NAME = 'cib_users'
# # FINAL_REPORT = 'similarity_report_table'
# REPORT = 'Individual_data'
# REPORT_INSTITUTE = 'Institutional_data'
# NOT_MATCH_REPORT = 'not_match_report'
# # INSTITUTIONAL_TABLE_NAME = 'Institutions'
# # DOWNLOADFILE = 'reply_mail'
# REPORT_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Email'))
# FOLLOW_UP_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Follow_up_email'))
# FOLLOW_UP_REPORT = os.path.join(FOLLOW_UP_PATH,'followup_file.xlsx')
# COMPLIANCE_FILE_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Compliance'))
# COMPLIANCE_REPORT_INDIVIDUAL = os.path.join(COMPLIANCE_FILE_PATH,'summary_individual_report.xlsx')
# COMPLIANCE_REPORT_INSTITUTIONAL = os.path.join(COMPLIANCE_FILE_PATH,'summary_institutional_report.xlsx')
# FINAL_REPORT = os.path.join(REPORT_PATH, 'file.xlsx')
# # DESTINATION_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Mail_file'))
# # hash_code_file_path = os.path.join(os.getcwd(),'output','hashcode.txt')
# # hash_code_file_path = os.path.join(r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents','hashcode.txt')
# hash_code_file_path = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','hashcode.txt'))
# # excel_file_path = os.path.join(os.getcwd(), 'output','data.xlsx')
# # FLAG_FILE_PATH = os.path.join(os.getcwd(), 'output','first_run_flag.txt')
# # FLAG_FILE_PATH = os.path.join(r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents','first_run_flag.txt')
# FLAG_FILE_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','first_run_flag.txt'))
# # HASH_FILE_PATH = os.path.join(os.getcwd(),"hashcode.json")
# # HASH_FILE_PATH = os.path.join(r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents',"hashcode.json")
# HASH_FILE_PATH = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','hashcode.json'))


BRANCH_CODE_LENGTH = 3
MAINCODE_LENGTH = 20
CLIENTCODE_LENGTH = 8

RESTRICTION = {
    'normal': 'f',
    'block': 'b',
    'debit restrict': '+',
    'credit restrict': "-",
    'link block':'l',
    'disputed block':'d',
    'waiting':'o',
    'true block':'t',
    'closed':'c',
}

REVRSE_RESTRICTION = {
    'f': 'normal',
    'b': 'block',
    '+': 'debit restrict',
    '-': 'credit restrict',
    'l': 'link block',
    'd': 'disputed block',
    'o': 'waiting',
    't': 'true block',
    'c': 'closed'
    }

VIEW_TABLE = {
    "client_table":"v_RPA_ClientTable",
    "client_table1":"v_RPA_ClientTable1",
    "client_beneficial":"v_RPA_ClientBenfDetail",
    "client_sign":"v_RPA_ClientSignDetail",
    "client_master":'v_RPA_Master'
}

VIEW_TABLE_COLUMNS = {
    "client_table":['typeofclient','clientcategory','ownershiptype','clientcode','name','firstname','middlename',
                    'lastname','jointname','address1','dateofbirth','citizenshipno','citizendistrict','fathersname','gfathersname',
                    'spousename','clientstatus','mobileno','phone','key_risk_grade','reason','pannumber','regnum'],
    "client_table1":['clientcode','name','firstname','middlename','lastname','address1',
                    'dateofbirth','citizenshipno','citizendistrict','fathersname','gfathersname','spousename'],
    "client_beneficial":['clientcode','firstname','middlename','lastname','address1','dateofbirth','bidtype','bidnum',
                        'biddistrict','bfathersname','bgfathersname','bspousename'],
    "client_sign":['clientcode','firstname','middlename','lastname','address1','dateofbirth','sidtype','sidnum',
                    'siddistrict','sfathersname','sgfathersname','sspousename','nameweight'],
    "client_master":['clientcode','branchcode','actype','cycode','maincode','name','isblocked','remarks']
}