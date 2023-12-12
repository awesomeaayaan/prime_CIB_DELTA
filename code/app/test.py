# from pathlib import Path
# import os
# import Constants
import os
import Constants
import pandas as pd

# path = os.path.join(Constants.cib_common_path,'Weightage Distribution.xlsx')
    

# df = pd.read_excel(path, sheet_name='Natural', skiprows=[0, 1, 2, 3, 4, 5, 6, 7])

#accuity
path = os.path.join(Constants.Accuity_Weitage_Path,'ACCUITY SCREENING WEIGHTAGE.xlsx')
df = pd.read_excel(path, sheet_name='NATURAL', skiprows=[0, 1, 2, 3,4])   
# df = pd.read_excel(path, sheet_name='LEGAL', skiprows=[0, 1, 2])
print(df.columns)
print(df.head())

# localpath = str(Path.home())
# current_path = os.getcwd()
# desired_path = os.path.abspath(os.path.join(current_path,'..','..','..','Documents'))
# print(f'This is Home path {localpath}')
# print(f"This is current directory file {current_path}")
# print(f"This is Home directory file {desired_path}")
# cib_path = os.path.join(localpath,'Documents','Robotic Process Automation','cib_delta')
# print(cib_path)
# if not os.path.exists(os.path.join(Constants.cib_common_path,'test_email','attachments')):
#     os.mkdir(os.path.join(Constants.cib_common_path,'test_email','attachments'))
# print('successfull')
# #C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening
# #C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents
# import pandas as pd
# date = '2023/12/07 10:07:34'.split()[0]
# print(date)
# import sqlite3
# import Constants
# con = sqlite3.connect(Constants.ACCUITY_DB_NAME)
# # con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()
# cur.execute(f'''
#         SELECT date FROM DATE_TABLE
#         WHERE file_name = 'first_file'
#         ''')
# #feth the rows
# rows = cur.fetchall()
# for row in rows:
    
#     print(f'Row data is {row}')
#     print(row[0])
# # cur.execute(f'Delete date FROM DATE_TABLE where id = 1')
# con.commit()
# con.close()
# print('Successfully extract the institutional pending data')
# import sqlite3
# import Constants
# con = sqlite3.connect(Constants.ACCUITY_DB_NAME)



# query = f'''
#     select * from  {Constants.ACCUITY_TABLE_NAME}
#     where status = 'new'
# '''
# # logger = self.run_item.logger
# con.row_factory = sqlite3.Row
# # logger.info(f'Reading data having status {status} from table  {Constants.ACCUITY_TABLE_NAME}')
# data = con.execute(query).fetchall()
# if data:
#     # logger.info(f'All database data retrivied.')
#     temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
#     # temp_value.to_excel('test_data_cib.xlsx',index=False)
#     # return temp_value
#     print(temp_value)
# else:
#     # return []
#     print('emty value')

# con.commit()
# con.close()
# cursor = conn.cursor()
# table_name = 'ACCUITY_DATA'

# drop_table_query = f'DROP TABLE IF EXISTS {table_name}'

# cursor.execute(drop_table_query)
# print('Successfully drop the table')

# conn.commit()
# conn.close()

# print(f'Table{table_name} has been deleted from the database.')

# import pandas as pd
# df_report = pd.read_excel(r'C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\CIB_DELTA_Screening\Prime-CIB\CIB_BOT_Delta-Screening\output\file.xlsx')

# df_email_file = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\Mail Id Details.xlsx")
# print(df_report.head())
# # branch_code = '218'
# print((df_report['branchcode'].iloc[0]))
# branch_value = str(df_report['branchcode'].iloc[0])

# # if branch_value == branch_code:
# #     print('match the branc code')
# print(str(df_email_file['BranchCode']))
# df = df_email_file[df_email_file['BranchCode'] == int(branch_value)]
# receiver_mail = df['BM Email ID'].iloc[0]
# print(df.head())
# print(df['BM Email ID'].iloc[0])
# for i, item in df_email_file.items():
#     print(i)
#     print(item['BranchCode'])
# for column,series in df_email_file.items():
#     if column == 'BranchCode':
#         for item in series:
#             if item == branch_value:

#                 print(item)
            # print(item)
    # item = str(item['BranchCode'].iloc[0])
    # print(item)
    # # print(type(item))
    # print(item['BranchCode'])
    # item = str(item)
    # print(item['BranchCode'])

# import pandas as pd
# df = pd.read_excel(r"C:\Users\RPA\Documents\RPA\CIB_BOT_Delta-master\Documents\test_email\attachments\33_NEWROAD BRANCH.xlsx")
# print(df['Result of CIB Screening'].iloc[0])
# from datetime import datetime
# import os 
# import Constants
# branch_value = '101'
# branch_name = 'okhaldhunga'
# current_datetime = datetime.now()
# current_datetime = str(current_datetime).split('.')[0]
# # date_time = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
# # print(current_datetime)
# # print(str(date_time))
# print(os.path.join(Constants.REPORT_PATH,f'{branch_value} {branch_name} {current_datetime}'))
# import Constants
# import sqlite3 
# email = 'aayaan.gautam1999@gmail.com'
# branch_name = 'kamalpokhari'
# status = '0'
# con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()
# cur.execute(''' 
#             CREATE TABLE IF NOT EXISTS EMAIL (
#                     Email_ID Text,
#                     Branch_name Text,
#                     Status Text
#             )
#             ''')
# sample_data = [
#     (email,branch_name,status)
# ]
# print(sample_data)

# cur.executemany('INSERT INTO EMAIL (Email_ID,Branch_name,Status) VALUES (?,?,?)',sample_data)
# print('Successfully insert email to the email table')
# con.commit()
# con.close()
# import sqlite3
# import Constants

# con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()

# cur.execute(''' 
#         SELECT Email_ID from Email
#                     WHERE Status == 0
#     ''')
# data = cur.fetchall()
# for email in data:
#      cur.execute(''' 
#                         UPDATE EMAIL 
#                         SET follow_up_count = follow_up_count +1
#                         WHERE Email_ID = ?
#                     ''',(email[0],))
# print('successfully update the follow up count')
# con.commit()
# con.close()
# import Constants
# import sqlite3

# main_code = "12701000000025700153"
# followup_count = 0

# con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()# and 'CBS Remarks' IS NOT NULL and 'CBS Account Status' NOT IN ('credit restrict','normal')
# cur.execute(f''' 
#         UPDATE {Constants.REPORT}
#         SET Delay_by_days = ?
#         WHERE "CBS Account Number" = ?;
#     ''',(followup_count,main_code))
# # display('Successfully update Delay count')
# # cur.execute(f''' 
# #         UPDATE {Constants.REPORT_INSTITUTE}
# #         SET Delay_by_days = ?
# #         WHERE "CBS Account Number" = ?;
# #     ''',(followup_count,main_code))
# # print('Successfully update Delay count')
# print('success')

# con.commit()
# con.close()

# followup_count = 4
# con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()
# cur.execute(f''' 
#         DELETE FROM {Constants.REPORT}
#         WHERE "CBS Account Number" = ?;
#     ''',(followup_count))

# cur.execute(f''' 
#         DELETE FROM {Constants.REPORT_INSTITUTE}
#         WHERE "CBS Account Number" = ?;
#     ''',(followup_count))

# con.commit()
# con.close()
# import pandas as pd
# from datetime import datetime, timedelta
# con = sqlite3.connect(Constants.DB_NAME)
# cur = con.cursor()
# today_date = datetime.now().date()
# query = f'''
#     SELECT * FROM {Constants.REPORT_INSTITUTE}
#     WHERE DATE(created_at) = ?;
#     '''
# # logger = self.run_item.logger
# con.row_factory = sqlite3.Row
# # logger.info(f'Reading data having status pending from table  {Constants.REPORT}')
# data = con.execute(query,(today_date,)).fetchall()
# if data:
#     # logger.info(f'All database data retrivied.')
#     temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
#     # display(f'Pending data is {temp_value}')
#     # temp_value.to_excel('test_data_cib.xlsx',index=False)
#     print(temp_value) 
#     df = pd.DataFrame(temp_value)
#     print(df.columns)
#     df.to_excel('summary_report.xlsx',index=False)
#     column_to_drop = ['created_at','updated_at']
#     df.drop(columns=column_to_drop,inplace=False)
#     print(df.columns)
#     desired_order = ['Branch Code', 'CBS Client Code', 'CBS Account Number',
#        'Account Description',  'CBS Account Name',
#        'Name Match %', 'CBS Father Name', 'Father Name %',
#        'CBS Date of birth(BS)', 'DOB Match %', 'CBS Citizenship No',
#        'Citizenship Match %', 'PAN NUMBER %', 'PASSPORT NUMBER %',
#        'Indian Embassy Reg No %', 'Total Similarity %',
#         'CIB Name', 'CIB Father Name', 'CIB DOB',
#        'CIB Citizenship No', 'CIB PAN No', 'CIB PASSPORT NO',
#        'CIB Indian Embassy NO', 'CIB Gender', 'CIB Black Listed No',
#        'CIB Black Listed Date', 'Driving Licence No', 'Indian Embassy Reg No',
#        'PAN No', 'Passport No', 'CBS Remarks', 'Result of CIB Screening','CBS Account Status','Delay_by_days',
#        'Status']

#     print(df.head())
# else:
#     print("didn't get data from data base of today date")