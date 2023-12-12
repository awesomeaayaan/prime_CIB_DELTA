from qrlib.QRComponent import QRComponent
from Variables import BotVariable
from robot.libraries.BuiltIn import BuiltIn

import os


class TaskLogger(QRComponent):
    def __init__(self):
        super().__init__()
        self.filename = 'TaskLogger.txt'
        self.foldername = ''

    def set_folder_name(self):
        # logger = self.run_item.logger
        # logger.info('Set folder location for logger file')
        self.foldername = BotVariable.CONFIG_PATH

    def create_logger_file(self):
        # logger = self.run_item.logger
        try:
            self.set_folder_name()
            path = f'{self.foldername}/{self.filename}'
            if os.path.exists(path):
                # logger.info('Removing file if alread exists')
                os.remove(path)
            with open(path, 'w') as file:
                file.write('Task Logger for Letter Actions\n')
        except Exception as e:
            BuiltIn().log_to_console(e)

    def write_log_to_logger_file(self, message: str):
        # logger = self.run_item.logger

        path = f'{self.foldername}/{self.filename}'
        try:
            self.set_folder_name()
            date = BuiltIn().get_time()
            with open(path, '+a') as file:
                file.write(f'\n[{date}] INFO : {message}.')
        except Exception as e:
            # logger.error(e)
            BuiltIn().log_to_console(e)

