import traceback
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from qrlib.QRRunItem import QRRunItem

from RPA.Email.ImapSmtp import ImapSmtp
from robot.libraries.BuiltIn import BuiltIn
from Variables import BotVariable
from datetime import datetime
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from FileComponent import FileComponent
import imaplib
import email
from email.header import decode_header
import os
import pandas as pd
import datetime as dt
import Constants
import shutil


display = BuiltIn().log_to_console


class EmailComponent(QRComponent):
    def __init__(self):
        super().__init__()
        # self.file = FileComponent()
        # send mail values
        self.sending_file_list = []
        self.subject = 'Summary report for News Scrapping'
        self.body = ''
        # self.recipients = 'aayaan.gautam1999@gmail.com'
        self.recipients = ''
        
        # smtp connection
        self.account = ''
        self.password = ''
        self.server = ''
        self.port = ''
        self.configpath = ''
        self.template_folder = ''
        self.cc = ''
        self.__vault_data = {}
        # self.__vault_data_imap = {}

    def _get_vault(self):
        # run_item = QRRunItem()
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['smtp']
        # self.logger.info("Got vault data")
        display('Got vault data ')
    def _imap_from_vault(self):
        # run_item = QRRunItem()
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['imap']
        display('Get imap vault successfully')
        # self.logger.info('Get imap vault successfully')
        

    def _get_imap_creds(self):
        # run_item = QRRunItem()
        # self.logger = self.run_item.logger
        self.imap_account = self.__vault_data['mail_account']
        self.imap_server = self.__vault_data['mail_host']
        self.imap_port = self.__vault_data['imap_port']
        self.imap_password = self.__vault_data['mail_password']
        # self.mail = ImapSmtp(
        #     account = self.imap_account, 
        #     password = self.imap_password, 
        #     imap_server = self.imap_server, 
        #     imap_port= self.imap_port
        # )
        # emails = self.mail.list_messages("UNSEEN")
        # BuiltIn().log_to_console(emails)
        # for email in emails:
        #     self.mail.save_attachment(
        #         email, 
        #         target_folder='output', 
        #         overwrite=False
        #     )
        # display('download successfuly')
        display('get imap creadential successulfy')
        self.logger.info('get imap creadential successulfy')

    def imap_login(self):
        # run_item = QRRunItem()
        # self.logger = self.run_item.logger
        self._imap_from_vault()
        imap = imaplib.IMAP4(self.__vault_data['mail_host'],int(self.__vault_data['imap_port']))
        imap.login(self.__vault_data['mail_account'],self.__vault_data['mail_password'])
        display('Logging imap cread successfully')
        # self.logger.info('Logging imap cread successfully')
        self.imap = imap
    # def download_attachment(self):
    #     self.imap_login()
    #     imap = self.imap
    #     imap.select('INBOX')
    #     emails = self.mail.list_messages('UNSEEN')
    #     for email in emails:
    #         self.mail.save_attachment(email,target_folder='output',overwrite=False)
    #         # self.imap.

    def download_attachment(self):
        self.imap_login()
        # logger = self.run_item.logger
        imap = self.imap

        self.subject_to_search = 'Conduct Rescreening to verify Legal CIB Match of Branch'
        search_criteria = f'UNSEEN SUBJECT "{self.subject_to_search}"'
        imap.select('INBOX')
        result, data = imap.uid('search', None, search_criteria)
        display(f'Data is {data}')
        display(f'Data is {data[0]}')
        display(f'Data at index zero is is {data[0].split()}')
        # data = data[0].split()
        if result == 'OK':
            # for dat in data:
            display(f'Dat is {data}')
            display(f'Dat tye is {type(data)}')
            byte_mail_list = [num for num in data[0].split()]#[::-1]
            display(f'Byte mail list{byte_mail_list}')
            sender_list = []
            if not byte_mail_list:
                # return False
                raise Exception('No mail found')
            print('byte_mail_list')
            # logger.info(byte_mail_list)
            for a in byte_mail_list:
                # _, fetched_data = imap.uid('fetch', byte_mail_list[0], '(RFC822)')
                _, fetched_data = imap.uid('fetch', a, '(RFC822)')
                # display(f'Fetched data is {fetched_data}')
                msg = email.message_from_bytes(fetched_data[0][1])
                sender = msg.get('From')
                sender_list.append(sender)

                # sender, _ = decode_header(msg['From'])[0]
                # BuiltIn().log_to_console(sender)
                # BuiltIn().log_to_console(_)

                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue

                    # Check if the part has a filename (attachment)
                    if part.get('Content-Disposition') is None:
                        continue
                    # Extract the attachment filename
                    filename = part.get_filename()
                    print(f'File name is ===> {filename}')
                    # Download the attachment
                    # current_path = os.getcwd()
                    # dir_path = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','test_email','attachments'))
                    if filename:
                        if not os.path.isdir(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\test_email\attachments"):
                            os.mkdir(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\test_email\attachments")

                        filepath = f"C:/Users/RPA/Documents/RPA/CIB_BOT_Delta-master/Documents/test_email/attachments/{filename}"
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f'Download attachment:{filename}')
            display(f'Sender list is {sender_list}')
            # return filename, send        
        
    # def download_attachment(self):
    #     # display('Apple')
    #     # self._get_vault()
    #     self._imap_from_vault()
    #     self._get_imap_creds()
    #     self.mail = ImapSmtp(imap_server= self.imap_server, imap_port=self.imap_port)
    #     display('no issue in the above ')
    #     self.mail.authorize_imap(account=self.imap_account, password=self.imap_password, imap_server=self.imap_server, imap_port=self.imap_port,)
    #     # self.mail.authorize_imap(account=self.imap_account, password=str(self.imap_password),)
    #     # self.mail.authorize_smtp(account=self.account, password=str(self.password), imap_server=self.server, imap_port=int(self.port),)
    #     display(f'Successfully conncetion stablished')
    #     emails = self.mail.list_messages("UNSEEN")
    #     display(f'Email is {email}')
    #     # BuiltIn.log_to_console(emails)
    #     for email in emails:
    #         self.mail.save_attachment(email,target_folder=Constants.DOWNLOADFILE,overwrite=False)
    
    def _set_smtp_creds(self):
        # logger = self.run_item.logger
        # logger.info("Setting required creds")
        self.account = self.__vault_data['account']
        self.server = self.__vault_data['server']
        self.port = self.__vault_data['port']
        self.configpath = self.__vault_data['config_path']
        # self.configpath = r'"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx"'
        try:
            self.password = self.__vault_data['password']
        except:
            self.password = None

    def get_html_body(self, body: str):
        th = '<th style="border: 2px solid #dddddd; text-align: left; padding: 8px;">'
        td = '<td style="border: 2px solid #dddddd; text-align: left; padding: 8px;">'
        table = 'border="2" style="font-family: arial, sans-serif; border-collapse: collapse; width: 100%;"'
        failed = '<b style="color:#ff0000">failed</b>'
        body = body.replace('border="1"', table)
        body = body.replace('<th>', th)
        body = body.replace('<td>', td)
        body = body.replace('failed', failed)
        return body
    def follow_up_mail(self,branch_value,attachments_path):
        self._get_vault()
        self._set_smtp_creds()

        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        self.body = f''' 
                       Dear Compliance Officers,<br><br>

                        <p>Please be informed that individuals, firms, companies, institutions included in the blacklist
                        as per the instructions of our regulatory are not allowed to open accounts in banks and financial
                        institutions. Also, banking transactions other than depositing money in the existing account of a 
                        blacklisted person,firm, company or institution will not be allowed which is clearly mentioned in 
                        NRB directives no.12.</p>

                        <p>Please refer to the attached excel sheet and conduct the rescreening of the CIB match
                        account in Trust AML system. In case the details of the customer matches in CIB category
                        then Debit(Dr) restrict the account with remarks as CIB match along with Black List no in CBS
                        on urgent basis.</p> 

                        <p>Kindly respond to this mail by downloading the attached excel sheet and selecting the appropriate
                        option from the provided choices (Match with CIB Black List or No Match with CIB Black List) 
                        available in the column of <strong>'Result of CIB Screening'</strong>. Please ensure that you reply is sent in email id
                        cib.blacklist@pcbl.com.np.</p>


                        <p> Please Understood the seriousness of the task and try to complete this task on urgent basis.</p>
                        <strong>Note:</strong>
                        <p>*If the account is already in Debit(Dr) Restricted status due to Dormant Stage, then do insert the 
                        remarks as CIB match along with Black List no in CBS.</p>
                        <p>*If the account is black listed more than one time, then insert the multiple Black List number by using
                        Comma(,).</p>
                        <p>*If the account is already in Blocked Status as per instruction from Nepal Rastra Bank or any other 
                        enforcement agencies then please contact us for further assistance.</p><br>
                        <p>*Requesting you to Debit Restrict all the operating account listed under the blacklisted Client code i.e
                        OD account, MO account etc.</p>
                        <br><br>
                        <strong>Thank you</strong><br><br>

                        <strong>Compliance Department</strong><br><br>

                        <strong>Central Office</strong><br><br>
                        
                    '''
        # df_email_file = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx")
        df_email_file = pd.read_excel(os.path.join(Constants.COMMON_PATH,'Mail Id Details.xlsx'))
        # current_path = os.getcwd()
        # dir_path = os.path.abspath(os.path.join(current_path,'..','..','..','Documents','Mail Id Details.xlsx'))
        # print(df_report.head())
        # branch_code = '218'
        # print('This is the branchcode from report==>',df_report['Branch Code'].iloc[0])
        # branch_value = str(df_report['Branch Code'].iloc[0])
        display(f'{branch_value}')
        # branch_name = str(df_report['BranchName'])


        # if branch_value == branch_code:
        #     print('match the branc code')
        print(str(df_email_file['BranchCode']))
        df = df_email_file[df_email_file['BranchCode'] == int(branch_value)]
        # df.to_excel('extract_email.xlsx')
        receiver_mail = df['BM Email ID'].iloc[0]
        branch_name = df['BranchName'].iloc[0]
        display(f'Branch Name is {branch_name}')

        print(receiver_mail)
        receiver_branch_code = df['BranchCode'].iloc[0]
        display(f'This is a branch code of reciver email {receiver_branch_code} and this is branchcode from file{branch_value}')
        current_datetime = datetime.now()
        date_time = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
        # date_time = self.file.extract_today_date()
        # os.rename(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Email\file.xlsx",f"{Constants.REPORT_PATH}\{branch_value}_{branch_name}.xlsx")
        # display('successfully rename the file')
        # logger.info(f"SMTP connection established.")
        # attachments_path = r'C:/Users/RPA/Documents/RPA/CIB_BOT_Delta-master/CIB_DELTA_Screening/Prime-CIB/CIB_BOT_Delta-Screening/output/file.xlsx'
        
        # attachments_path = r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Email\file.xlsx"
        # display(f"{Constants.REPORT_PATH}\{branch_value}_{branch_name}.xlsx")
        # attachments_path = rf"{Constants.REPORT_PATH}\{branch_value}_{branch_name}.xlsx"
        # attachments_path = ''
        display(f'Attachment_path{attachments_path}')
        self.sending_file_list.append(attachments_path)
        display(self.sending_file_list)
            
        # ) sushil.kc@pcbl.com.np
        
        self.mail.send_message(
            sender=self.account,
            # recipients=self.recipients, binu.shrestha@pcbl.com.np nidhi.shahi@pcbl.com.np
            # 'sushil.kc@pcbl.com.np',
            recipients=['sushil.kc@pcbl.com.np','binu.shrestha@pcbl.com.np','nidhi.shahi@pcbl.com.np',],
            
            # subject=self.subject,
            subject=f'Please choose the appropriate value in column Result of CIB Screening and Conduct Rescreening to verify CIB Match of Branch {branch_value}',
            body=self.body,
            attachments=self.sending_file_list,
            html=True
        )
        # logger.info("Mail Sent Successfully.")
        self.sending_file_list.clear()
        display("MAIL SENT SUCCESSFULLY")
        os.remove(attachments_path)
        display('file delete successfully')


    def _authmail_and_send(self):
        # logger = self.run_item.logger
        try:
            self._get_vault()
            self._set_smtp_creds()
            """Call when send mail only"""
            # logger = self.run_item.logger
            # logger.info('SMTP connection started')
            self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
            self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
            
            self.body = f''' 
                        Dear Compliance Officers,<br><br>
                        
                        <p styles = "text-align: justify;">Please be informed that individuals, firms, companies, institutions included in the blacklist
                        as per the instructions of our regulatory are not allowed to open accounts in banks and financial
                        institutions. Also, banking transactions other than depositing money in the existing account of a 
                        blacklisted person,firm, company or institution will not be allowed which is clearly mentioned in 
                        NRB directives no.12.</p>

                        <p styles = "text-align: justify;">Please refer to the attached excel sheet and conduct the rescreening of the CIB match
                        account in Trust AML system. In case the details of the customer matches in CIB category
                        then Debit(Dr) restrict the account with remarks as CIB match along with Black List no in CBS
                        on urgent basis.</p> 

                        <p styles = "text-align: justify;">Kindly respond to this mail by downloading the attached excel sheet and selecting the appropriate
                        option from the provided choices (Match with CIB Black List or No Match with CIB Black List) 
                        available in the column of <strong>'Result of CIB Screening'</strong>. Please ensure that you reply is sent in email id
                        cib.blacklist@pcbl.com.np.</p>


                        <p styles = "text-align: justify;"> Please Understood the seriousness of the task and try to complete this task on urgent basis.</p>
                        <strong>Note:</strong>
                        <p styles = "text-align: justify;">*If the account is already in Debit(Dr) Restricted status due to Dormant Stage, then do insert the 
                        remarks as CIB match along with Black List no in CBS.</p>
                        <p styles = "text-align: justify;">*If the account is black listed more than one time, then insert the multiple Black List number by using
                        Comma(,).</p>
                        <p styles = "text-align: justify;">*If the account is already in Blocked Status as per instruction from Nepal Rastra Bank or any other 
                        enforcement agencies then please contact us for further assistance.</p><br>
                        <p styles = "text-align: justify;">*Requesting you to Debit Restrict all the operating account listed under the blacklisted Client code i.e
                        OD account, MO account etc.</p>
                        <br><br>
                        <strong>Thank you</strong><br><br>

                        <strong>Compliance Department</strong><br><br>

                        <strong>Central Office</strong><br><br>
                        
                    '''
            print('Start sending the email to the compliance')
            # df_report = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Email\file.xlsx")
            df_report = pd.read_excel(os.path.join(Constants.REPORT_PATH,'file.xlsx'))
            # df_email_file = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx")
            df_email_file = pd.read_excel(os.path.join(Constants.COMMON_PATH,'Mail Id Details.xlsx'))
            print(df_report.head())
            # branch_code = '218'
            print('This is the branchcode from report==>',df_report['Branch Code'].iloc[0])
            branch_value = str(df_report['Branch Code'].iloc[0])
            display(f'{branch_value}')
            # branch_name = str(df_report['BranchName'])
            if 'ComRegister No' in df_report.columns:
                self.subject = f'Conduct Rescreening to verify Legal CIB Match of Branch {branch_value}'
            else:
                self.subject = f'Conduct Rescreening to verify Natural CIB Match of Branch {branch_value}'

            # if branch_value == branch_code:
            #     print('match the branc code')
            print(str(df_email_file['BranchCode']))
            df = df_email_file[df_email_file['BranchCode'] == int(branch_value)]
            # df.to_excel('extract_email.xlsx')
            receiver_mail = df['BM Email ID'].iloc[0]
            branch_name = df['BranchName'].iloc[0]
            display(f'Branch Name is {branch_name}')
            
            
            print(receiver_mail)
            receiver_branch_code = df['BranchCode'].iloc[0]
            display(f'This is a branch code of reciver email {receiver_branch_code} and this is branchcode from file{branch_value}')
            current_datetime = datetime.now()
            current_datetime = str(current_datetime).split('.')[0]
            current_datetime = current_datetime.replace(':','_')
            # date_time = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
            # date_time = self.file.extract_today_date()
            # os.rename(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Email\file.xlsx",f"{Constants.REPORT_PATH}\{branch_value}_{branch_name} {current_datetime}.xlsx")
            os.rename((os.path.join(Constants.REPORT_PATH,'file.xlsx')),os.path.join(Constants.REPORT_PATH,f'{branch_value}_{branch_name} {current_datetime}.xlsx'))
            display('successfully rename the file')
            # logger.info(f"SMTP connection established.")
            # attachments_path = r'C:/Users/RPA/Documents/RPA/CIB_BOT_Delta-master/CIB_DELTA_Screening/Prime-CIB/CIB_BOT_Delta-Screening/output/file.xlsx'
            
            # attachments_path = r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Email\file.xlsx"
            display(os.path.join(Constants.REPORT_PATH,f'{branch_value}_{branch_name} {current_datetime}.xlsx'))
            # attachments_path = rf"{Constants.REPORT_PATH}\{branch_value}_{branch_name} {current_datetime}.xlsx"
            attachments_path = os.path.join(Constants.REPORT_PATH,f'{branch_value}_{branch_name} {current_datetime}.xlsx')
            display(f'Attachment_path{attachments_path}')
            self.sending_file_list.append(attachments_path)
            display(self.sending_file_list)
                
            # ) sushil.kc@pcbl.com.np
            display(f'Subject is {self.subject}')
            self.mail.send_message(
                sender=self.account,
                # recipients=self.recipients, binu.shrestha@pcbl.com.np nidhi.shahi@pcbl.com.np
                # 'sushil.kc@pcbl.com.np',
                recipients=['sushil.kc@pcbl.com.np','binu.shrestha@pcbl.com.np','nidhi.shahi@pcbl.com.np',],
                
                # subject=self.subject,
                subject=self.subject,
                body=self.body,
                attachments=self.sending_file_list,
                # cc=self.cc,
                # cc='aayaangautam2021@gmail.com',
                # body=self.body,
                # attachments=r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\output\file.xlsx',
                html=True
            )
            
            # logger.info("Mail Sent Successfully.")
            self.sending_file_list.clear()
            display("MAIL SENT SUCCESSFULLY")
            source_path = rf"{Constants.REPORT_PATH}\{branch_value}_{branch_name} {current_datetime}.xlsx"
            destination_path = rf"{Constants.COMPLIANCE_FILE_PATH}\{branch_value}_{branch_name} {current_datetime}.xlsx"
            shutil.copy(source_path,destination_path)
            display("Successfully copy the file to destination")
            os.remove(attachments_path)
            display('file delete successfully')
            
        except Exception as e:
            # logger.error(traceback.format_exc())
            raise e
            

    def initiate_connection(self):
        logger = self.run_item.logger
        logger.info("Initiating connection setting")
        self._get_vault()
        self._set_smtp_creds()

    def get_news_list_html(self, report_data: list):
        table = ''
        for item in report_data:
            temp = f'''
                <div style="height: 150px; background-color:powderblue; margin:10px; padding:10px;">
                    <h3>{item['heading_of_news']}</h3>
                    <p><b>Summary:</b>  {item['summary']}</p>
                    <span>Published date : {item['datetime']}</span>
                    <br>
                    <a href="{item['news_link']}">Read more...</a>
                </div>
            '''
            table += temp
        return table

    def get_email_attacment_folder_paths(self) -> str:
        self._get_vault()
        email_folder = str(self.__vault_data['email_attachment'])
        email_folder = email_folder.replace('\\', '/')
        if email_folder.endswith('/'):
            email_folder = email_folder[:-1]

        return email_folder

    # def get_email_template(self, action_type: str) -> tuple:
    #     """
    #     Read email template from the specific location based on the action type

    #     Parameters
    #     ----------
    #     action_type : str
    #         type of requested mail
    #         type will be account_block, account_information, debit_restrict, account_release

    #     Returns
    #     -------
    #     tuple
    #         contains tuple of body message as first element
    #         and footer message as second element
    #     """
    #     # assert not action_type, "Action type is not provided for reading email template"

    #     logger = self.run_item.logger
    #     # * need to add filepath for production
    #     temp_vault = QREnv.VAULTS['work_directory']
    #     self.template_folder = temp_vault['template_folder']
    #     template_filepath = self.template_folder
    #     if action_type == "account_block":
    #         body_file_name = f"{template_filepath}/account_block_body.txt"
    #         footer_file_name = f"{template_filepath}/account_block_footer.txt"
    #     elif action_type == "account_block_high_risk":
    #         body_file_name = f"{template_filepath}/account_block_high_risk_body.txt"
    #         footer_file_name = f"{template_filepath}/account_block_high_risk_footer.txt"
    #     elif action_type == "account_information_natural":
    #         body_file_name = f"{template_filepath}/account_information_natural_body.txt"
    #         footer_file_name = f"{template_filepath}/account_information_natural_footer.txt"
    #     elif action_type == "account_information_legal":
    #         body_file_name = f"{template_filepath}/account_information_legal_body.txt"
    #         footer_file_name = f"{template_filepath}/account_information_legal_footer.txt"
    #     elif action_type == 'debit_restrict':
    #         body_file_name = f"{template_filepath}/debit_restrict_body.txt"
    #         footer_file_name = f"{template_filepath}/debit_restrict_footer.txt"
    #     else:
    #         body_file_name = f"{template_filepath}/account_release_body.txt"
    #         footer_file_name = f"{template_filepath}/account_release_footer.txt"

    #     body_template_message = ''
    #     footer_template_message = ''

    #     logger.info(f"Reading body template of file {body_file_name}")
    #     display(f"Reading body template of file {body_file_name}")

    #     with open(body_file_name, "r") as body:
    #         body_template_message = body.read()

    #     logger.info(f"Reading body template of file {body_file_name}")
    #     display(f"Reading body template of file {body_file_name}")
    #     with open(footer_file_name, "r") as body:
    #         footer_template_message = body.read()

    #     return (body_template_message, footer_template_message)
    
    # def send_mail_to_respective_branch(self):
    #     print('Start sending the email to the compliance')
    #     df_report = pd.read_excel(r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\output\file.xlsx')
    #     df_email_file = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx")
    #     print(df_report.head())
    #     # branch_code = '218'
    #     print((df_report['branchcode'].iloc[0]))
    #     branch_value = str(df_report['branchcode'].iloc[0])

    #     # if branch_value == branch_code:
    #     #     print('match the branc code')
    #     print(str(df_email_file['BranchCode']))
    #     df = df_email_file[df_email_file['BranchCode'] == int(branch_value)]
    #     receiver_mail = df['BM Email ID'].iloc[0]

    #     self._get_vault()
    #     self._set_smtp_creds()
    #     """Call when send mail only"""
    #     logger = self.run_item.logger
    #     logger.info('SMTP connection started')        
    #     mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
    #     mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
    #     logger.info(f"SMTP connection established.")
    #     attachments_path = r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\output\file.xlsx'
    #     attachment = open(attachments_path,'rb')
    #     mail.send_message(
    #         sender=self.account,
    #         # recipients=self.recipients,
    #         recipients='aayaan.gautam1999@gmail.com',
    #         subject=self.subject,
    #         subject='test',
    #         body='This mail is sent for the propose of test',
    #         attachments=attachment,
    #         # cc=self.cc,
    #         # cc='aayaangautam2021@gmail.com',
    #         # body=self.body,
    #         # attachments=r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\output\file.xlsx',
    #         # html=True
    #     )


        #         email_report_path = ""
        