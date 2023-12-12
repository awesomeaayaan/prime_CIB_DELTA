import json 
import Constants
from pathlib import Path

from qrlib.QRComponent import QRComponent
from Variables import BotVariable

class ConfigComponent(QRComponent):
    def __init__(self, local_work_dir = None):
        super().__init__()
        if isinstance(local_work_dir, str):
            self.local_path = local_work_dir + "/"  + "Robotic Process Automation/LetterActions"
        else:
            self.local_path = str(Path.home()).replace('\\', '/') + "/"  + "Documents/Robotic Process Automation/LetterActions"
        self.config_path = self.local_path + "/" + "config"
        self.database_path = self.local_path + "/" + "database"
        self.download_path_source = self.local_path + "/" + "download"
        self.download_path_read = self.local_path + "/" + "read"
        self.download_path_error = self.local_path + "/" + "error"
        self.report_path = self.local_path + "/" + "report"
        self.unmatched_path = self.local_path + '/' + 'unmatched'
        self.unmatched_success = self.local_path + '/' + 'unmatched_success'
        self.xml_download_path = str(Path.home()).replace('\\', '/') + "/"  + "Documents"
    
    def set_config_file(self):
        """Config file is read and load required runtime variable"""
        logger = self.run_item.logger

        config_path = self.config_path + "/" + Constants.CONFIG_FILE_NAME
        logger.info(f"Config path {config_path}")
        with open(config_path) as f:
            data = json.load(f)

        BotVariable.LOCAL_PATH = self.local_path
        BotVariable.CONFIG_PATH = self.config_path
        BotVariable.DOWNLOAD_PATH_SOURCE = self.download_path_source
        BotVariable.DOWNLOAD_PATH_READ = self.download_path_read
        BotVariable.DOWNLOAD_PATH_ERROR = self.download_path_error
        BotVariable.REPORT_GEN_PATH = self.report_path
        BotVariable.REPORT_UNMATCHED_PATH = self.unmatched_path
        BotVariable.DATABASE_PATH = self.database_path
        BotVariable.XML_DOWNLOAD_PATH = self.xml_download_path 
        BotVariable.UNMATCHED_SUCESS_PATH = self.unmatched_success
        
        # BotVariable.FTP_DEFAULT_FOLDER = data['ftp_default_folder']
        # BotVariable.FTP_WORKING_FOLDER = data['ftp_working_folder']
        # BotVariable.FTP_FOLLOW_UP_FOLDER = data['ftp_follow_up_folder']
