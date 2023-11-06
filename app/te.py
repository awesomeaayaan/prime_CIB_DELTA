# import json
# import pandas as pd

# file = open(r"D:\BOT_Prime\CIB_DELTA_back\output\data.json")
# datas = json.load(file)
# df = pd.DataFrame(columns=[
#         'Name',
#         'DOB', 
#         'Gender', 
#         'FatherName', 
#         'CitizenshipDetails', 
#         'PassportDetails', 
#         'DrivingLicenseDetails',
#         'VoterIDDetails',
#         'PANDetails', 
#         'IndianEmbassyDetails',
#         'BlackLists' 
#     ])

# num = 0
# for data in datas["BulkOffLoading"]["Individuals"]["Item"]:
#     dicts = {}
#     data_keys = list(data.keys())
#     # print(data_keys)
#     for data_key in data_keys[:4]:
#         dicts[data_key] = data[data_key]
#     for data_key in sorted(data_keys[4:]):
#         keys = list(data[data_key].keys())
#         data_count = int(data[data_key][keys[0]])
#         if data_count > 1:
#             details = data[data_key][keys[1]]
#             if "BlackList" in data_key:
#                 dicts[data_key] = ['|'.join(detail.values()) for detail in details]
#                 continue
#             else:  
#                 for detail in details:
#                     dicts[data_key] = '|'.join(detail.values())
#                     df.loc[len(df)] = dicts
#         elif data_count == 0:
#             continue
#         else:
#             details = data[data_key][keys[1]]
#             dicts[data_key] = '|'.join(details.values())

#         if "BlackList" not in data_key:
#             df.loc[len(df)] = dicts
#             del dicts[data_key]
#     num += 1
#     if num == 100:
#         break
    # df.to_excel('final.xlsx',index=False)
# import os

# os.remove(r"D:\BOT_Prime\CIB_DELTA_back\output\email\black_list11.xlsx")
# print('successfully removed the file from the folder')

import pandas as pd
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

# Sample data for the DataFrame
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Father_Name': ['Doe', 'Smith', 'Johnson'],
    'Gender': ['Male', 'Female', 'Male']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Create a new Excel writer object
excel_writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

# Write the DataFrame to Excel
df.to_excel(excel_writer, index=False, sheet_name='Sheet1')

# Get the workbook and worksheet objects
workbook = excel_writer.book
worksheet = excel_writer.sheets['Sheet1']

# Define the list of options for the dropdown
gender_options = ['Male', 'Female']

# Define the range where the dropdown will be applied (assuming Gender column starts from column C)
dropdown_range = 'C2:C{}'.format(len(df) + 1)

# Create a DataValidation object for the dropdown
data_validation = DataValidation(type="list", formula1='"{}"'.format(','.join(gender_options)), allow_blank=True)

# Add the data validation to the specific column
worksheet.add_data_validation(data_validation)
data_validation.add(dropdown_range)

# Save the Excel file
excel_writer.save()
excel_writer.save()

print("Dropdown list added to the 'Gender' column in the Excel file.")
