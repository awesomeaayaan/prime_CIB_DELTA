import json
import pandas as pd

file = open(r"D:\BOT_Prime\CIB_DELTA_back\output\data.json")
datas = json.load(file)
df = pd.DataFrame(columns=[
        'Name',
        'DOB', 
        'Gender', 
        'FatherName', 
        'CitizenshipDetails', 
        'PassportDetails', 
        'DrivingLicenseDetails',
        'VoterIDDetails',
        'PANDetails', 
        'CompanyDetails',
        'IndianEmbassyDetails',
        'BlackLists' 
    ])

num = 0
for data in datas["BulkOffLoading"]["Individuals"]["Item"]:
    # for key_value in data:
    print("--------------------------- REal Data --------------------- \n")
    print(data)
    dicts = {}
    data_keys = list(data.keys())
    for data_key in data_keys:
        if isinstance(data[data_key], str):
            dicts[data_key] = data[data_key]
        else:
            # maintain Citizenship details
            keys = list(data[data_key].keys())
            data_count = int(data[data_key][keys[0]])
            if data_count > 1:
                details = data[data_key][keys[1]]
                dicts[data_key] = ['|'.join(entry.values()) for entry in details]
            elif data_count == 0:
                dicts[data_key] = ""
            else:
                details = data[data_key][keys[1]]
                dicts[data_key] = '|'.join(details.values())

    print(f"--------------- Processed Data number {num} -----------------------" )
    print(dicts)
    num += 1
    if num == 3:
        break

#     # appending to df
#     df.loc[len(df)] = dicts
# # df = pd.DataFrame(columns=[
# #         'Name',
# #         'PANDetails', 
# #         'CompanyDetails',
# #         'BlackLists' 
# #     ])

# # num = 0
# for data in datas["BulkOffLoading"]["Institutions"]["Item"]:
#       # for key_value in data:
#     print("--------------------------- REal Data --------------------- \n")
#     print(data)
#     dicts = {}
#     data_keys = list(data.keys())
#     for data_key in data_keys:
#         if isinstance(data[data_key], str):
#             dicts[data_key] = data[data_key]
#         else:
#             # maintain Citizenship details
#             keys = list(data[data_key].keys())
#             data_count = int(data[data_key][keys[0]])
#             if data_count > 1:
#                 details = data[data_key][keys[1]]
#                 dicts[data_key] = ['|'.join(entry.values()) for entry in details]
#             elif data_count == 0:
#                 dicts[data_key] = ""
#             else:
#                 details = data[data_key][keys[1]]
#                 dicts[data_key] = '|'.join(details.values())

#     print(f"--------------- Processed Data number {num} -----------------------" )
#     print(dicts)
#     num += 1
#     # if num == 11:
#     #     break

#     # appending to df
#     df.loc[len(df)] = dicts


# df.to_excel("black_list_new.xlsx", index=False)
    