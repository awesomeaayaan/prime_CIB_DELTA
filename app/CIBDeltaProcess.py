from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from DefaultComponent import DefaultComponent
from DBComponent import DBComponent
from APIComponent import APIComponent
from Variables import BotVariable
from qrlib.QRUtils import display
import Constants
import pandas as pd
import os


class CIBDeltaProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.default_component = DefaultComponent()
        self.register(self.default_component)
        self.data = []
        self.db = DBComponent()
        self.api = APIComponent()


        self.register(self.db)
        self.register(self.api)

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        try:
            self.db.connect()
            self.db.create_table()
            
        except Exception as e:
            run_item.report_data = {"Remarks": "Database error error"}
            raise e
        
        try:
            self.api.load_vault_api()
            # self.api.get_data()
        except Exception as e:
            run_item.report_data = {"Remarks": "Load vault error"}
            raise e
        self.default_component.login()
        self.data = ["a", "b"]

    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        
        if not os.path.exists(Constants.FLAG_FILE_PATH):
            first_run_flag = True
            with open(Constants.FLAG_FILE_PATH, 'w') as flag_file:
                flag_file.write('1')
        else:
            first_run_flag = False
        if first_run_flag:
            print("Performing first run actions...")
            self.api.get_data()
            detail_individual_data = self.api.get_individual_data()
            for items in detail_individual_data:
                self.db.insert_into_the_database(items)
            institutional_data = self.api.get_institutional_data()
            for items in institutional_data:
                self.db.insert_into_the_database(items)

        else:
            print("Performing subsequent run actions...")
            # self.api.get_data()
            detail_individual_data = self.api.get_individual_data()

            df = pd.DataFrame(detail_individual_data)
            display(f"dataframe is: {df}")

            






        # self.api.get_data()
        # detail_data = self.api.get_individual_data()
        # for items in detail_data:
        #     self.db.insert_into_the_database(items)
        # institutional_data = self.api.get_institutional_data()
        # for items in institutional_data:
        #     self.db.insert_into_the_database(items)

        
        
        

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

        self.default_component.logout()
 
    def execute_run(self):
        self.execute_run_item()
        # for x in self.data:
        #     self.before_run_item(x)
        #     self.execute_run_item(x)
        #     self.after_run_item(x)

