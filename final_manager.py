import json
import pandas as pd

file = open("data.json")
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
        'IndianEmbassyDetails',
        'BlackLists' 
    ])

num = 0
for data in datas["BulkOffLoading"]["Individuals"]["Item"]:
    # for key_value in data:
    print("--------------------------- REal Data --------------------- \n")
    print(data)
    dicts = {}
    #name
    dicts["Name"] = data["Name"]
    dicts["DOB"] = data["DOB"]
    dicts["Gender"] = data["Gender"]
    dicts["FatherName"] = data["FatherName"]
    # maintain Citizenship details
    keys = list(data["CitizenshipDetails"].keys())
    citizenshp_count = int(data["CitizenshipDetails"][keys[0]])
    citizenship_data = data["CitizenshipDetails"][keys[1]]
    if citizenshp_count > 1:
        dicts["CitizenshipDetails"] = ['|'.join(entry.values()) for entry in citizenship_data]
    elif citizenshp_count == 0:
        dicts["CitizenshipDetails"] = ""
    else:
        dicts["CitizenshipDetails"] = '|'.join(citizenship_data.values())

    # maintain blacklist details
    keys = list(data["BlackLists"].keys())
    blacklist_count = int(data["BlackLists"][keys[0]])
    blacklist_data = data["BlackLists"][keys[1]]
    if blacklist_count > 1:
        dicts["BlackLists"] = ['|'.join(entry.values()) for entry in blacklist_data]
    elif blacklist_count == 0:
        dicts["BlackLists"] = ""
    else:
        dicts["BlackLists"] = '|'.join(blacklist_data.values())

    print(f"--------------- Processed Data number {num} -----------------------" )
    print(dicts)
    num += 1
    if num == 51:
        break

    # appending to df
    df.loc[len(df)] = dicts

df.to_excel("black_list.xlsx", index=False)
    