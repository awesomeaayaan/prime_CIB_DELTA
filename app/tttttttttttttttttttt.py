import os


flag_file_path = 'first_run_flag.txt'
if not os.path.exists(flag_file_path):
    first_run_flag = True
    with open(flag_file_path, 'w') as flag_file:
        flag_file.write('1')
else:
    first_run_flag = False
if first_run_flag:
    print("Performing first run actions...")
    print("apple")
else:
    print("Performing subsequent run actions...")
    print("orange")


def follow_up_pending_mail(self,branch_value,attachments_path):
        self._get_vault()
        self._set_smtp_creds()

        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        self.body = f''' 
                       Dear Compliance Officers,<br><br>
                       <p> We are contacting you to follow-up on our previous email of CIB match customers. We have found
                       that your branch has not completed the task of verifying the CIB match customer.</p>

                        <p>Please be informed that individuals, firms, companies, institutions included in the blacklist
                        as per the instructions of our regulatory are not allowed to open accounts in banks and financial
                        institutions. Also, banking transactions other than depositing money in the existing account of a 
                        blacklisted person,firm, company or institution will not be allowed which is clearly mentioned in 
                        NRB directives no.12.</p>

                        <p>So, we request you to understand the seriousness of the task and complete the task of rescreening
                         of the CIB match account in Trust AML system. In case the details of the customer matches in CIB category
                         then Debit(Dr) restrict the account with remarks as CIB match along with Black List no in CBS without 
                         further delay.</p> 

                        <p>Kindly respond to this mail by downloading the attached excel sheet and selecting the appropriate
                        option from the provided choices (Match with CIB Black List or No Match with CIB Black List) 
                        available in the column of <strong>'Result of CIB Screening'</strong>. Please ensure that your reply is sent in email id
                        cib.blacklist@pcbl.com.np.</p>


                       
                        <strong>Thank you</strong><br><br>

                        <strong>Compliance Department</strong><br><br>

                        <strong>Central Office</strong><br><br>
                        
                    '''
        # df_email_file = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx")
        df_email_file = pd.read_excel(os.path.join(Constants.COMMON_PATH,'Mail Id Details.xlsx'))
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
        display(receiver_mail)

        receiver_branch_code = df['BranchCode'].iloc[0]
        display(f'This is a branch code of reciver email {receiver_branch_code} and this is branchcode from file{branch_value}')
        current_datetime = datetime.now()
        date_time = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
        
        display(f'Attachment_path{attachments_path}')
        self.sending_file_list.append(attachments_path)
        display(self.sending_file_list)
            
        # ) sushil.kc@pcbl.com.np
        
        self.mail.send_message(
            sender=self.account,
            # recipients=self.recipients, binu.shrestha@pcbl.com.np nidhi.shahi@pcbl.com.np
            # 'sushil.kc@pcbl.com.np', 'binu.shrestha@pcbl.com.np','nidhi.shahi@pcbl.com.np',
            recipients=['sushil.kc@pcbl.com.np','binu.shrestha@pcbl.com.np','nidhi.shahi@pcbl.com.np',],
            
            # subject=self.subject,
            subject=f'CIB Match followup mail',
            body=self.body,
            attachments=self.sending_file_list,
            html=True
        )
        # logger.info("Mail Sent Successfully.")
        self.sending_file_list.clear()
        display("MAIL SENT SUCCESSFULLY")
        os.remove(attachments_path)
        display('file delete successfully')


