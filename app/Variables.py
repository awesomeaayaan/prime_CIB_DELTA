"""Runtime Variable"""
import os

class BotVariable:
    LOCAL_PATH: str = ''
    CONFIG_PATH: str = ''
    DOWNLOAD_PATH_SOURCE: str = ''
    DOWNLOAD_PATH_READ: str = ''
    DOWNLOAD_PATH_ERROR: str = ''
    REPORT_GEN_PATH: str = ''
    REPORT_UNMATCHED_PATH: str = ''
    UNMATCHED_SUCESS_PATH:  str = ''
    XML_DOWNLOAD_PATH: str = ''
    
    DATABASE_PATH: str = os.path.join(os.getcwd(), 'output')

    # folder name in ftp server
    FTP_DEFAULT_FOLDER = ""
    FTP_FOLLOW_UP_FOLDER = ""
    FTP_WORKING_FOLDER = ""
    ERROR = 'Error'
    SUCCESS = 'Success'
    READ = 'Read'
    SOURCE = 'Source'
    REPORT = 'Report'
    MATCHED = 'Matched'
    UNMATCHED = 'Unmatched'
