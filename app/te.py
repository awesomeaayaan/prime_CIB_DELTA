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
        'IndianEmbassyDetails',
        'BlackLists' 
    ])

num = 0
for data in datas["BulkOffLoading"]["Individuals"]["Item"]:
    dicts = {}
    data_keys = list(data.keys())
    # print(data_keys)
    for data_key in data_keys[:4]:
        dicts[data_key] = data[data_key]
    for data_key in sorted(data_keys[4:]):
        keys = list(data[data_key].keys())
        data_count = int(data[data_key][keys[0]])
        if data_count > 1:
            details = data[data_key][keys[1]]
            if "BlackList" in data_key:
                dicts[data_key] = ['|'.join(detail.values()) for detail in details]
                continue
            else:  
                for detail in details:
                    dicts[data_key] = '|'.join(detail.values())
                    df.loc[len(df)] = dicts
        elif data_count == 0:
            continue
        else:
            details = data[data_key][keys[1]]
            dicts[data_key] = '|'.join(details.values())

        if "BlackList" not in data_key:
            df.loc[len(df)] = dicts
            del dicts[data_key]
    num += 1
    if num == 100:
        break
    df.to_excel('final.xlsx',index=False)