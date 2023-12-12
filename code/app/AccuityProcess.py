from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from AccuityComponent import AccuityComponent
from qrlib.QRUtils import display
from AccuityFileComponent import AccuityFileComponent
from AccuityDbComponent import AccuityDbComponent
import os
import Constants

class AccuityProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.accuity = AccuityComponent()
        self.accuityfile = AccuityFileComponent()
        self.file_path = os.path.join(Constants.ACCUITY_PATH,'ac_UPIDGWL.ZIP')
        self.accuity_db = AccuityDbComponent()
        self.register(self.accuity)
        self.register(self.accuityfile)
        self.data = []

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.accuity._get_vault()
        self.accuity.open_chrome()
        self.accuity.login()

        #first file
        file_name = 'first_file'
        initial_date = self.accuity_db.get_date_from_date_table(file_name)
        display(f'Initial date is {initial_date}')
        self.accuity_db.create_date_table()
        date = self.accuity.scrape_first_file_data(initial_date)
        if initial_date != date:
            self.accuity_db.insert_into_date_table(date,file_name)
            self.accuityfile.check_file_downloaded_or_not()
            self.accuityfile.extract_zipfile()
            df = self.accuityfile.read_the_extracted_file()
            display(f'Data first file {df.head()}')
            display(f'total value_in_data is {df.count()}')
            self.accuity_db.insert_accuity_data(df)
            self.accuityfile.remove_the_file_from_directory()
        else:
            display("Date is Not modify")

        #Secondfile
        file_name = 'second_file'
        # self.accuity_db.create_date_table()
        initial_date = self.accuity_db.get_date_from_date_table(file_name)
        date = self.accuity.scrape_second_file_data(initial_date)
        if initial_date != date:
            self.accuity_db.insert_into_date_table(date,file_name)
            self.accuityfile.check_file_downloaded_or_not()
            self.accuityfile.extract_zipfile()
            df = self.accuityfile.read_the_extracted_file()
            display(f'Data second file {df.head()}')
            display(f'total value_in_data is {df.count()}')
            self.accuity_db.insert_accuity_data(df)
            self.accuityfile.remove_the_file_from_directory()
        else:
            display("Date is Not modify")

        #third file
        # self.accuity_db.create_date_table()
        file_name = 'third_file'
        initial_date = self.accuity_db.get_date_from_date_table(file_name)
        date = self.accuity.scrape_third_file_data(initial_date)
        if initial_date != date:
            self.accuity_db.insert_into_date_table(date,file_name)
            self.accuityfile.check_file_downloaded_or_not()
            self.accuityfile.extract_zipfile()
            df = self.accuityfile.read_the_extracted_file()
            display(f'Data third file {df.head()}')
            display(f'total value_in_data is {df.count()}')
            self.accuity_db.insert_accuity_data(df)
            self.accuityfile.remove_the_file_from_directory()
        else:
            display("Date is Not modify")

        
        #fourth file
        # self.accuity_db.create_date_table()
        file_name = 'fourth_file'
        initial_date = self.accuity_db.get_date_from_date_table(file_name)
        date =  self.accuity.scrape_fourth_file_data(initial_date)
        if initial_date != date:
            self.accuity_db.insert_into_date_table(date,file_name)
            self.accuityfile.check_file_downloaded_or_not()
            self.accuityfile.extract_zipfile()
            df = self.accuityfile.read_the_extracted_file()
            display(f'Data of the fourth file is {df.head()}')
            display(f'total value_in_data is {df.count()}')
            self.accuity_db.insert_accuity_data(df)
            self.accuityfile.remove_the_file_from_directory()
        else:
            display("Date is Not modify")

        #close the browser
        self.accuity.close_browser()

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

        self.default_component.test()
        run_item.report_data["test"] = args[0]

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
        for x in self.data:
            self.before_run_item(x)
            self.execute_run_item(x)
            self.after_run_item(x)