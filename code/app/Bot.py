import time

from qrlib.QRBot import QRBot
from qrlib.QRRunItem import QRRunItem

from TaskLogger import TaskLogger
from DBView import DatabaseViewTask
from FileComponent import FileComponent
from EmailComponent import EmailComponent
from CIBDeltaProcess import CIBDeltaProcess
from WeightageProcess import WeightageProcess
from AccuityProcess import AccuityProcess
from AccuityComponent import AccuityComponent
from Accuity_WeightageProcess import Accuity_WeightageProcess


class Bot(QRBot):

    def __init__(self):
        super().__init__()
        self.setup_platform_components()
        self.cibprocess = CIBDeltaProcess()
        self.weightprocess = WeightageProcess()
        self.email = EmailComponent()
        self.db_view = DatabaseViewTask()
        self.tasklogger = TaskLogger()
        self.file = FileComponent()
        self.accuity = AccuityComponent()
        self.accuityprocess = AccuityProcess()
        self.accuity_weightageprocess = Accuity_WeightageProcess()


        self.register(self.db_view)
        self.register(self.email)
        self.register(self.tasklogger)
        self.register(self.file)
        self.register(self.accuity)
        self.register(self.accuityprocess)
        self.register(self.accuity_weightageprocess)
        self.df_map:dict = {}
        

    def start(self):
        run_item: QRRunItem = QRRunItem(is_ticket=False)
        self.notify(run_item)

        test = True
        logger = run_item.logger
        hour_changed = False
        current_time = time.time()

        with self.db_view as view:
            # self.db_view.__enter__()
            self.df_map = view.collect_all_view_table()

        # self.accuityprocess.before_run()
        weightageaccuity = self.accuity_weightageprocess.before_run()
        if weightageaccuity:
            self.accuity_weightageprocess.execute_run(self.df_map)

        # self.accuity.open_chrome()
        # self.email.download_attachment()
        # self.file.read_file_and_send_email()
        # self.email.send_mail_to_respective_branch()
        # self.email._authmail_and_send()
        # self.email.imap_login()
        # self.email._get_imap_creds()
        # self.email.download_attachment()
        # next_hour_time = time.time() + Constants.HOUR_TIME
        # self.cibprocess.before_run()

        logger.info(f"Gathering information from jump server")
        # self.tasklogger.write_log_to_logger_file(f"Gathering information from jump server")
        # self.tasklogger.write_log_to_logger_file('Getting view table from jump server')

        with self.db_view as view:
            # self.db_view.__enter__()
            self.df_map = view.collect_all_view_table()


        # # temporarily called from here 
        # self.email.download_attachment()
        # self.cibprocess.read_file_and_send_email()
        # logger.info(f"Extracting followup data")
        # acct_info_followup = self.cibprocess.get_follow_up_data()
        # logger.info(f'followup account is {acct_info_followup}')
        # logger.info(f"Extracting followup data completed")

        # if acct_info_followup:
        #     # * follow up should be done with pending data
        #     logger.info(f'Yesterday followup data data found and proceed to cib action process')
        #     # self.tasklogger.write_log_to_logger_file(f'Working on account information followup')
        #     self.cibprocess.execute_run(self.df_map)
        # else:
        #     logger.info(f'Follow up data of account information and release not found')



        # self.tasklogger.write_log_to_logger_file('Getting view table from jump server successful')
        logger.info(f"Gathering information from jump server completed")
        # self.tasklogger.write_log_to_logger_file(f"Gathering information from jump server completed")

        wresult = self.weightprocess.before_run()

        wp_requests = self.weightprocess.get_wp_requests()
        if wp_requests:
                # self.tasklogger.write_log_to_logger_file('Performing weightage calculation in current file.')
                # self.df_map = pd.read_excel(r'D:\prime_bot_dev\Prime-CIB\CIB_BOT_Delta-Screening\client_tablee.xlsx')
                self.weightprocess.execute_run(self.df_map)
        # self.setup_platform_components()
        logger.info(f"Gathering information from jump server")
        # self.tasklogger.write_log_to_logger_file(f"Gathering information from jump server")
        # self.tasklogger.write_log_to_logger_file('Getting view table from jump server')
        with self.db_view as view:
            self.db_view.__enter__()
            self.df_map = view.collect_all_view_table()
        # self.df_map = pd.read_excel(r'D:\prime_bot_dev\Prime-CIB\CIB_BOT_Delta-Screening\output\client_tablee.xlsx')
        # self.weightprocess.execute_run(self.df_map)
        # self.cibprocess.before_run()
        # self.cibprocess.execute_run()
        self.email.download_attachment()
        self.cibprocess.read_file_and_send_email()
        self.email.follow_up_email_with_no_reply_from_branch()

        logger.info(f"Extracting followup data")
        acct_info_followup = self.cibprocess.get_follow_up_data()
        logger.info(f"Extracting followup data completed")

        if acct_info_followup:
            # * follow up should be done with pending data
            logger.info(f'Yesterday followup data data found and proceed to cib action process')
            # self.tasklogger.write_log_to_logger_file(f'Working on account information followup')
            self.cibprocess.execute_run(self.df_map)
        else:
            logger.info(f'Follow up data of account information and release not found')

    def teardown(self):
        self.cibprocess.after_run()
