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


from datetime import datetime, timedelta
con = sqlite3.connect(Constants.DB_NAME)
cur = con.cursor()
today_date = datetime.now().date()
query = (f'''
    SELECT * FROM {Constants.REPORT}
    WHERE DATE(created_date) = ?;
    ''',(today_date,))
# logger = self.run_item.logger
con.row_factory = sqlite3.Row
# logger.info(f'Reading data having status pending from table  {Constants.REPORT}')
data = con.execute(query).fetchall()
if data:
    # logger.info(f'All database data retrivied.')
    temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
    # display(f'Pending data is {temp_value}')
    # temp_value.to_excel('test_data_cib.xlsx',index=False)
    print(temp_value) 
else:
    print("didn't get data from data base of today date")
