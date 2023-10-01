import requests
from qrlib.QREnv import QREnv
from qrlib.QRRunItem import QRRunItem
from qrlib.QRComponent import QRComponent
import Constants
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QRUtils import display
from bs4 import BeautifulSoup
import pandas as pd
import xmltodict
import json

class APIComponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.detail_data_list = []
    def load_vault_api(self):
        self.logger.info("Accessing vault data for apis")
        # self._authorization =  QREnv.VAULTS['authorization']['authorization']
        self._CIB_url = QREnv.VAULTS['urls']['CIB_url']
        self.logger.info("Vault data for APIs accessed successfully")    

    def get_data(self):
        with open(r'D:\BOT_Prime\CIB_DELTA\output\response.xml', 'r') as xml_file:
            xml_data = xml_file.read()
        # self.logger.info("Calling API")
        # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        # response = requests.get(
        #     f"{self._CIB_url}",
        #     timeout=30,
        #     headers=headers
        # )
        # data = response.content
        data_dict = xmltodict.parse(xml_data)
        data = json.dumps(data_dict, indent=4)
        # display(json_data)
        self.data = json.loads(data)
        

        # return data
    def get_individual_data(self):
        # display(self.data)
        # print('individual-->',self.data)
        
        for item in self.data["BulkOffLoading"]["Individuals"]["Item"]:
            name = item["Name"]
            print('Name---->',name)
            dob = item["DOB"]
            gender = item["Gender"]
            father_name = item["FatherName"]
            
            passport_data = item["PassportDetails"]
            # print('passport_ddata',passport_data)
            passport_count = passport_data["PassportCount"]
            # print('passportcount-->',passport_count)
            passport_detail_item = passport_data.get("Passport",[])
            print(passport_detail_item)
            if isinstance(passport_detail_item,list):
                # print("the item is list")
                if passport_detail_item:
                    for items in passport_detail_item:
                        passport_number = items.get("PassportNumber","")
                        passport_expiry_date = items.get("PassportExpiryDate","")
                        print(f"passport number is :{passport_number}")
                else:
                    passport_number = ""
                    passport_expiry_date = "" 
                    print(f"passport number is :{passport_number}")
            elif isinstance(passport_detail_item,dict):
                print("the item is DICT")
                if passport_detail_item:
                    passport_number = passport_detail_item.get("PassportNumber","")
                    passport_expiry_date = passport_detail_item.get("PassportExpiryDate","")
                else:
                    passport_number = ""
                    passport_expiry_date = "" 
                print(f"passport number is :{passport_number}")
            else:
                # print("the item is neither dict nor list")
                passport_number = ""
                passport_expiry_date = ""
                # print(f"passport number is :{passport_number}")
            
            driving_lisence_data = item["DrivingLicenseDetails"]
            driving_license_count = driving_lisence_data["DrivingLicenseCount"]
            driving_license_item = driving_lisence_data.get("DrivingLicense",[])
            if isinstance(driving_license_item,list):
                if driving_license_item:
                    for items in driving_license_item:
                            driving_license_no = items.get("DrivingLicenseNo","")
                            driving_license_issuedate = items.get("DrivingLicenseIssuedDate","")
                else:
                    driving_license_no = ""
                    driving_license_issuedate = ""
            
            if isinstance(driving_license_item,dict):
                if driving_license_item:
                    driving_license_no = driving_license_item.get("DrivingLicenseNo","")
                    driving_license_issuedate = driving_license_item.get("DrivingLicenseIssuedDate","")
                else:
                    driving_license_no = ""
                    driving_license_issuedate = "" 

            voter_id_data = item["VoterIDDetails"]
            voter_id_count = voter_id_data["VoterIdCount"]
            voter_id_list_item = voter_id_data.get("VoterID",[])
            if isinstance(voter_id_list_item,list):
                if voter_id_list_item:
                    for items in voter_id_list_item:
                        voter_id_no = items.get("VoterIdNo","")
                        voter_id_issued_date = items.get("VoterIdIssuedDate","")
                else:
                    voter_id_no = ""
                    voter_id_issued_date = ""
            if isinstance(voter_id_list_item,dict):
                display(f"voter_id list-->{voter_id_list_item}")
                if voter_id_list_item:
                    voter_id_no = voter_id_list_item.get("VoterIdNo","")
                    display(f"{voter_id_no}")
                    voter_id_issued_date = voter_id_list_item.get("VoterIdIssuedDate","")

                else:
                    voter_id_no = ""
                    voter_id_issued_date = ""
            # pan_count = item["PANDetails"]["PANCount"]
            pan_data = item['PANDetails']
            pan_count = pan_data["PANCount"]
            pan_list_item = pan_data.get('PAN',[])
            if isinstance(pan_list_item,list):
                if pan_list_item:
                    for items in pan_list_item:
                        pan_number = items.get('PAN','')
                        pan_issued_date = items.get('PANIssuedDate','')
                        pan_issued_district = items.get('PANIssuedDistrict','')
                else:
                    pan_number = ""
                    pan_issued_date = ""
                    pan_issued_district = ""
            if isinstance(pan_list_item,dict):
                if pan_list_item:
                    pan_number = pan_list_item.get('PAN','')
                    pan_issued_date = pan_list_item.get('PANIssuedDate','')
                    pan_issued_district = pan_list_item.get('PANIssuedDistrict','')
                else:
                    pan_number = ""
                    pan_issued_date = ""
                    pan_issued_district = ""

            indian_embassy_data = item["IndianEmbassyDetails"]
            indian_embassy_count = indian_embassy_data["IndianEmbassyCount"]
            indian_embassy_detail = indian_embassy_data.get("IndianEmbassyDetail",[])
            if isinstance(indian_embassy_detail,list):
                if indian_embassy_detail:
                    for items in indian_embassy_detail:
                        indian_embassy_number = items.get("IndianEmbassyNumber","")
                        indian_embassy_regdate = items.get("IndianEmbassyRegDate","")

                else:
                    indian_embassy_number = ""
                    indian_embassy_regdate = ""
            if isinstance(indian_embassy_detail,dict):
                if indian_embassy_detail:
                    indian_embassy_number = indian_embassy_detail.get("IndianEmbassyNumber","")
                    indian_embassy_regdate = indian_embassy_detail.get("IndianEmbassyRegDate","")
                else:
                    indian_embassy_number = ""
                    indian_embassy_regdate = ""

            citizenship_data = item["CitizenshipDetails"]
            citizenship_count = citizenship_data['CitizenshipCount']
            citizenship_list_items = citizenship_data.get("Citizenship", [])
            if isinstance(citizenship_list_items, list):
                if citizenship_list_items:
                    for items in citizenship_list_items:
                        citizenship_number = items.get("CitizenshipNumber", "")
                        citizenship_issued_date = items.get("CitizenshipIssuedDate", "")
                        citizenship_issued_district = items.get("CitizenshipIssuedDistrict", "")
                else:
                    citizenship_number = ""
                    citizenship_issued_date = ""
                    citizenship_issued_district = ""
            if isinstance(citizenship_list_items, dict):
                if citizenship_list_items:
                    citizenship_number = citizenship_list_items.get("CitizenshipNumber", "")
                    citizenship_issued_date = citizenship_list_items.get("CitizenshipIssuedDate", "")
                    citizenship_issued_district = citizenship_list_items.get("CitizenshipIssuedDistrict", "")
                else:
                    citizenship_number = ""
                    citizenship_issued_date = ""
                    citizenship_issued_district = ""
            
            
            black_lists_data = item["BlackLists"]
            black_list_count = black_lists_data["BlackListCount"]
            display(f"Black lIst Cout is : {black_list_count}")
            black_list_items = black_lists_data.get("BlackList", [])
            if isinstance(black_list_items, list):
                for items in black_list_items:
                    black_list_sector = items.get("Sector", "")
                    display(f"{black_list_sector}")
                    # if black_list_number:
                    # else:
                    if items['BlacklistNumber']:
                        
                        black_list_number = items.get("BlacklistNumber", "")
                        print(f"---{citizenship_number}----{black_list_number}")
                    else:
                        black_list_number = ""
                    black_list_date = items.get("BlacklistedDate", "")
                    black_list_type = items.get("BlacklistType", "")
                    black_list_relation = items.get("NatureOfRelation", "")
                    detail_data = {
                        "Name":name,
                        'DOB': dob,
                        'Gender':gender,
                        'FatherName':father_name,

                        'CitizenshipCount':citizenship_count,
                        'CitizenshipNumber':citizenship_number,
                        'CitizenshipIssuedDate':citizenship_issued_date,
                        'CitizenshipIssuedDistrict':citizenship_issued_district,

                        'PassportCount':passport_count,
                        "PassportNumber":passport_number,
                        "PassportExpiryDate":passport_expiry_date,

                        'DrivingLicenseCount':driving_license_count,
                        "DrivingLicenseNo":driving_license_no,
                        "DrivingLicenseIssuedDate":driving_license_issuedate,

                        'VoterIdCount':voter_id_count,
                        "VoterIdNo":voter_id_no,
                        "VoterIdIssuedDate":voter_id_issued_date,

                        'PANCount':pan_count,
                        'PAN':pan_number,
                        "PANIssuedDate":pan_issued_date,
                        "PANIssuedDistrict": pan_issued_district,

                        'IndianEmbassyCount':indian_embassy_count,
                        "IndianEmbassyNumber":indian_embassy_number,
                        "IndianEmbassyRegDate":indian_embassy_regdate,

                        'BlackListCount':black_list_count,
                        'Sector':black_list_sector,
                        'BlacklistNumber':black_list_number,
                        'BlacklistedDate':black_list_date,
                        'BlacklistType':black_list_type,
                        'NatureOfRelation':black_list_relation,

                        "CompanyCount": "",
                        "CompanyRegNumber": "",
                        "CompanyRegDate" : "",
                        "CompanyRegAuth": "",

                        "Status":""
                    }
                    # display(f"data details is :{detail_data}")
                    self.detail_data_list.append(detail_data)

            if isinstance(black_list_items, dict):
                black_list_sector = black_list_items.get("Sector", "")
                black_list_number = black_list_items.get("BlacklistNumber", "")
                black_list_date = black_list_items.get("BlacklistedDate", "")
                black_list_type = black_list_items.get("BlacklistType", "")
                black_list_relation = black_list_items.get("NatureOfRelation", "")

                detail_data = {
                    "Name":name,
                    'DOB': dob,
                    'Gender':gender,
                    'FatherName':father_name,

                    'CitizenshipCount':citizenship_count,
                    'CitizenshipNumber':citizenship_number,
                    'CitizenshipIssuedDate':citizenship_issued_date,
                    'CitizenshipIssuedDistrict':citizenship_issued_district,

                    'PassportCount':passport_count,
                    "PassportNumber":passport_number,
                    "PassportExpiryDate":passport_expiry_date,

                    'DrivingLicenseCount':driving_license_count,
                    "DrivingLicenseNo":driving_license_no,
                    "DrivingLicenseIssuedDate":driving_license_issuedate,

                    'VoterIdCount':voter_id_count,
                    "VoterIdNo":voter_id_no,
                    "VoterIdIssuedDate":voter_id_issued_date,

                    'PANCount':pan_count,
                    'PAN':pan_number,
                    "PANIssuedDate":pan_issued_date,
                    "PANIssuedDistrict": pan_issued_district,

                    'IndianEmbassyCount':indian_embassy_count,
                    "IndianEmbassyNumber":indian_embassy_number,
                    "IndianEmbassyRegDate":indian_embassy_regdate,

                    'BlackListCount':black_list_count,
                    'Sector':black_list_sector,
                    'BlacklistNumber':black_list_number,
                    'BlacklistedDate':black_list_date,
                    'BlacklistType':black_list_type,
                    'NatureOfRelation':black_list_relation,

                    "CompanyCount": "",
                    "CompanyRegNumber": "",
                    "CompanyRegDate" : "",
                    "CompanyRegAuth": "",

                    "Status":""
                }
                # display(f"data details is :{detail_data}")
                self.detail_data_list.append(detail_data)
                # return detail_data
        # print(self.detail_data_list)
        return self.detail_data_list

    def get_institutional_data(self):
        for item in self.data["BulkOffLoading"]["Institutions"]["Item"]:
            name = item["Name"]
            pan_data = item['PANDetails']
            pan_count = pan_data["PANCount"]
            pan_list_item = pan_data.get('PAN',[])
            if isinstance(pan_list_item,list):
                if pan_list_item:
                    for items in pan_list_item:
                        pan_number = items.get('PAN','')
                        pan_issued_date = items.get('PANIssuedDate','')
                        pan_issued_district = items.get('PANIssuedDistrict','')
                else:
                    pan_number = ""
                    pan_issued_date = ""
                    pan_issued_district = ""
            # indian_embassy_count = item["IndianEmbassyDetails"]["IndianEmbassyCount"]
            if isinstance(pan_list_item,dict):
                if pan_list_item:
                    pan_number = pan_list_item.get('PAN','')
                    pan_issued_date = pan_list_item.get('PANIssuedDate','')
                    pan_issued_district = pan_list_item.get('PANIssuedDistrict','')
                else:
                    pan_number = ""
                    pan_issued_date = ""
                    pan_issued_district = ""

            company_data = item["CompanyDetails"]
            company_count = company_data["CompanyCount"]
            company_list_item = company_data.get("Company",[])
            if isinstance(company_list_item,list):
                if company_list_item:
                    for items in company_list_item:
                        company_reg_number = items.get("CompanyRegNumber","")
                        company_reg_date = items.get("CompanyRegDate","")
                        company_reg_Auth = items.get("CompanyRegAuth","")
                else:
                    company_reg_number = ""
                    company_reg_date = ""
                    company_reg_Auth = ""

            if isinstance(company_list_item,dict):
                if company_list_item:
                    company_reg_number = company_list_item.get("CompanyRegNumber","")
                    company_reg_date = company_list_item.get("CompanyRegDate","")
                    company_reg_Auth = company_list_item.get("CompanyRegAuth","")

                else:
                    company_reg_number = ""
                    company_reg_date = ""
                    company_reg_Auth = "" 




            black_lists_data = item["BlackLists"]
            black_list_count = black_lists_data["BlackListCount"]
            black_list_items = black_lists_data.get("BlackList", [])
            if isinstance(black_list_items, list):
                for items in black_list_items:
                    black_list_sector = items.get("Sector", "")
                    black_list_number = items.get("BlacklistNumber", "")
                    black_list_date = items.get("BlacklistedDate", "")
                    black_list_type = items.get("BlacklistType", "")
                    black_list_relation = items.get("NatureOfRelation", "")

                    detail_data = {
                    "Name":name,
                    "DOB":"",
                    "FatherName":"",
                    "Gender" : "",
                    "CitizenshipCount" : "",
                    "CitizenshipNumber" : "",
                    "CitizenshipIssuedDate" : "",
                    "CitizenshipIssuedDistrict" : "",
                    "PassportCount" : "",
                    "PassportNumber" : "",
                    "PassportExpiryDate" : "",
                    "DrivingLicenseCount" : "",
                    "DrivingLicenseNo" : "",
                    "DrivingLicenseIssuedDate" : "",
                    "VoterIdCount" : "",
                    "VoterIdNo" : "",
                    "VoterIdIssuedDate" : "",
                    "IndianEmbassyCount" : "",
                    "IndianEmbassyNumber" : "",
                    "IndianEmbassyRegDate" : "",
                    "PANCount":pan_count,
                    "PAN":pan_number,
                    "PANIssuedDate":pan_issued_date,
                    "PANIssuedDistrict":pan_issued_district,
                    "CompanyCount":company_count,
                    "CompanyRegNumber":company_reg_number,
                    "CompanyRegDate":company_reg_date,
                    "CompanyRegAuth":company_reg_Auth,
                    "BlackListCount":black_list_count,
                    "Sector":black_list_sector,
                    "BlacklistNumber":black_list_number,
                    "BlacklistedDate":black_list_date,
                    "BlacklistType":black_list_type,
                    "NatureOfRelation":black_list_relation ,
                    "Status":"new_data"
                }

            if isinstance(black_list_items, dict):
                black_list_sector = black_list_items.get("Sector", "")
                black_list_number = black_list_items.get("BlacklistNumber", "")
                black_list_date = black_list_items.get("BlacklistedDate", "")
                black_list_type = black_list_items.get("BlacklistType", "")
                black_list_relation = black_list_items.get("NatureOfRelation", "")

                # data_institutional = [name,pan_count,pan_number,pan_issued_date,pan_issued_district,company_count,company_reg_number,company_reg_date,company_reg_Auth,black_list_count,black_list_date,black_list_number,black_list_type,black_list_relation]
                # print(data_institutional)
                detail_data = {
                    "Name":name,
                    "DOB":"",
                    "FatherName":"",
                    "Gender" : "",
                    "CitizenshipCount" : "",
                    "CitizenshipNumber" : "",
                    "CitizenshipIssuedDate" : "",
                    "CitizenshipIssuedDistrict" : "",
                    "PassportCount" : "",
                    "PassportNumber" : "",
                    "PassportExpiryDate" : "",
                    "DrivingLicenseCount" : "",
                    "DrivingLicenseNo" : "",
                    "DrivingLicenseIssuedDate" : "",
                    "VoterIdCount" : "",
                    "VoterIdNo" : "",
                    "VoterIdIssuedDate" : "",
                    "IndianEmbassyCount" : "",
                    "IndianEmbassyNumber" : "",
                    "IndianEmbassyRegDate" : "",
                    "PANCount":pan_count,
                    "PAN":pan_number,
                    "PANIssuedDate":pan_issued_date,
                    "PANIssuedDistrict":pan_issued_district,
                    "CompanyCount":company_count,
                    "CompanyRegNumber":company_reg_number,
                    "CompanyRegDate":company_reg_date,
                    "CompanyRegAuth":company_reg_Auth,
                    "BlackListCount":black_list_count,
                    "Sector":black_list_sector,
                    "BlacklistNumber":black_list_number,
                    "BlacklistedDate":black_list_date,
                    "BlacklistType":black_list_type,
                    "NatureOfRelation":black_list_relation ,
                    "Status":"new_data"
                }

                self.detail_data_list.append(detail_data)
        print(self.detail_data_list)
        return self.detail_data_list


        # # display(data)

        # # Extract and process "Individuals" data
        # individuals_data = data["BulkOffLoading"]["Individuals"]["Item"]
        # individuals_df = pd.DataFrame(individuals_data)
        # individuals_df = individuals_df.applymap(str) 
        # individuals_df.fillna("", inplace=True)


        # # Extract and process "Institutions" data
        # institutions_data = data["BulkOffLoading"]["Institutions"]["Item"]
        # institutions_df = pd.DataFrame(institutions_data)
        # institutions_df = institutions_df.applymap(str) 
        # institutions_df.fillna("", inplace=True)

        # return individuals_df,institutions_df





