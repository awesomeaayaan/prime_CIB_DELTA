from qrlib.QRComponent import QRComponent
import sqlite3
import Constants
from qrlib.QRUtils import display
import nepali_datetime
from datetime import datetime

class DBComponent(QRComponent):
    def __init__(self) -> None:
        self.con = None
        self.cur = None
        
    def connect(self):
        self.con = sqlite3.connect(Constants.DB_NAME)
        self.cur = self.con.cursor()
        display(f"Successfully connected to the database")
        
    def close_connection(self):
        self.cur.close()
        self.con.close()

    def create_table(self):
        # Create a table with the specified schema
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {Constants.INDIVIDUAL_TABLE_NAME} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        DOB TEXT,
        Gender TEXT,
        FatherName TEXT,
        CitizenshipCount TEXT,
        CitizenshipNumber TEXT,
        CitizenshipIssuedDate TEXT,
        CitizenshipIssuedDistrict TEXT,
        PassportCount TEXT,
        PassportNumber TEXT,
        PassportExpiryDate TEXT,
        DrivingLicenseCount TEXT,
        DrivingLicenseNo TEXT,
        DrivingLicenseIssuedDate TEXT,
        VoterIdCount TEXT,
        VoterIdNo TEXT,
        VoterIdIssuedDate TEXT,
        PANCount TEXT,
        PANIssuedDate TEXT,
        PANIssuedDistrict TEXT,
        IndianEmbassyCount TEXT,
        IndianEmbassyNumber TEXT,
        IndianEmbassyRegDate TEXT,
        BlackListCount TEXT,
        Sector TEXT,
        BlacklistNumber TEXT,
        BlacklistedDate TEXT,
        BlacklistType TEXT,
        NatureOfRelation TEXT,
        CompanyCount TEXT,
        CompanyRegNumber TEXT,
        CompanyRegDate TEXT,
        CompanyRegAuth TEXT,
        Status Text
    )
        """)
        display(f"Successfully created the table")


    def insert_into_the_database(self,detail_data):
        insert_sql = f"""INSERT INTO {Constants.INDIVIDUAL_TABLE_NAME}(
                                Name,
                                DOB,
                                Gender,
                                FatherName,
                                CitizenshipCount,
                                CitizenshipNumber,
                                CitizenshipIssuedDate,
                                CitizenshipIssuedDistrict,
                                PassportCount,
                                PassportNumber,
                                PassportExpiryDate ,
                                DrivingLicenseCount,
                                DrivingLicenseNo,
                                DrivingLicenseIssuedDate,
                                VoterIdCount,
                                VoterIdNo,
                                VoterIdIssuedDate,
                                PANCount,
                                PANIssuedDate,
                                PANIssuedDistrict,
                                IndianEmbassyCount,
                                IndianEmbassyNumber,
                                IndianEmbassyRegDate,
                                BlackListCount,
                                Sector,
                                BlacklistNumber,
                                BlacklistedDate,
                                BlacklistType,
                                NatureOfRelation,
                                CompanyCount,
                                CompanyRegNumber,
                                CompanyRegDate,
                                CompanyRegAuth,
                                Status
                                ) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """
        self.cur.execute(insert_sql, (
                detail_data["Name"],
                detail_data["DOB"],
                detail_data["Gender"],
                detail_data["FatherName"],
                detail_data["CitizenshipCount"],
                detail_data["CitizenshipNumber"],
                detail_data["CitizenshipIssuedDate"],
                detail_data["CitizenshipIssuedDistrict"],
                detail_data["PassportCount"],
                detail_data["PassportNumber"],
                detail_data["PassportExpiryDate"],
                detail_data["DrivingLicenseCount"],
                detail_data["DrivingLicenseNo"],
                detail_data["DrivingLicenseIssuedDate"],
                detail_data["VoterIdCount"],
                detail_data["VoterIdNo"],
                detail_data["VoterIdIssuedDate"],
                detail_data["PANCount"],
                detail_data["PANIssuedDate"],
                detail_data["PANIssuedDistrict"],
                detail_data["IndianEmbassyCount"],
                detail_data["IndianEmbassyNumber"],
                detail_data["IndianEmbassyRegDate"],
                detail_data["BlackListCount"],
                detail_data["Sector"],
                detail_data["BlacklistNumber"],
                detail_data["BlacklistedDate"],
                detail_data["BlacklistType"],
                detail_data["NatureOfRelation"],
                detail_data["CompanyCount"],
                detail_data["CompanyRegNumber"],
                detail_data["CompanyRegDate"],
                detail_data["CompanyRegAuth"],
                detail_data["Status"],
                # detail_data["Name"],
            
        ))
        self.con.commit()
        

    def fetch_latest_blacklisted_date_from_database(self):
        # Query to extract the latest blacklisted date
        self.cur.execute('SELECT BlackLists FROM test_delta_screening;')

        # Fetch the result
        black_lists_tuples = self.cur.fetchall()

        # Extract dates and split them
        black_lists_dates = [black_list[0].split("|")[2] for black_list in black_lists_tuples]
        # Convert date strings to datetime objects, handling invalid dates
        date_objects = []
        for date_str in black_lists_dates:
            try:
                date_object = nepali_datetime.datetime.strptime(date_str, '%Y-%m-%d')
                date_objects.append(date_object)
            except ValueError:
                print(f"Skipping invalid date: {date_str}")

        # If you want to exclude invalid dates from further processing, you can use date_objects list

        # Find the latest date
        if date_objects:
            # print('date-object',date_objects)
            latest_date = max(date_objects)
            parsed_date = datetime.strptime(str(latest_date), "%Y-%m-%d %H:%M:%S%z")
            latest_blacklisted_date = parsed_date.strftime("%Y-%m-%d")
            print("Latest Blacklisted Date:", latest_blacklisted_date)
            return latest_date
        else:
            print("No valid dates found in the database.")

        
        




    # def insert_dataframe_into_database(self,individuals_df,institutions_df):
    #     individuals_df.to_sql(Constants.INDIVIDUAL_TABLE_NAME, self.con, if_exists='replace', index=False)
    #     institutions_df.to_sql(Constants.INSTITUTIONS_TABLE_NAME, self.con, if_exists='replace', index=False)


    # def insert_individual_record(self, item):
    #     name = item["Name"]
    #     display(name)
    #     dob = item["DOB"]
    #     gender = item["Gender"]
    #     father_name = item["FatherName"]
       
    #     citizenship_data = item["CitizenshipDetails"]
    #     citizenship_count = citizenship_data['CitizenshipCount']
    #     citizenship_number = ""  # Initialize the variable here
    #     citizenship_issued_date = ""  # Initialize the variable here
    #     citizenship_issued_district = ""  # Initialize the variable here
        
    #     citizenship_list_items = citizenship_data.get("Citizenship", [])
    #     if isinstance(citizenship_list_items, list):
    #         for items in citizenship_list_items:
    #             citizenship_number = items.get("CitizenshipNumber", "")
    #             citizenship_issued_date = items.get("CitizenshipIssuedDate", "")
    #             citizenship_issued_district = items.get("CitizenshipIssuedDistrict", "")

    #     if isinstance(citizenship_list_items, dict):
    #         citizenship_number = citizenship_list_items.get("CitizenshipNumber", "")
    #         citizenship_issued_date = citizenship_list_items.get("CitizenshipIssuedDate", "")
    #         citizenship_issued_district = citizenship_list_items.get("CitizenshipIssuedDistrict", "")

    #     passport_count = item["PassportDetails"]["PassportCount"]
    #     driving_license_count = item["DrivingLicenseDetails"]["DrivingLicenseCount"]
    #     voter_id_count = item["VoterIDDetails"]["VoterIdCount"]
    #     pan_count = item["PANDetails"]["PANCount"]
    #     indian_embassy_count = item["IndianEmbassyDetails"]["IndianEmbassyCount"]



    #     black_lists_data = item["BlackLists"]
    #     black_list_count = black_lists_data["BlackListCount"]
    #     black_list_sector = ""  # Initialize the variable here
    #     black_list_number = ""  # Initialize the variable here
    #     black_list_date = ""  # Initialize the variable here
    #     black_list_type = ""  # Initialize the variable here
    #     black_list_relation = ""  # Initialize the variable here
        
    #     black_list_items = black_lists_data.get("BlackList", [])
    #     if isinstance(black_list_items, list):
    #         for items in black_list_items:
    #             black_list_sector = items.get("Sector", "")
    #             black_list_number = items.get("BlacklistNumber", "")
    #             black_list_date = items.get("BlacklistedDate", "")
    #             black_list_type = items.get("BlacklistType", "")
    #             black_list_relation = items.get("NatureOfRelation", "")

    #     if isinstance(black_list_items, dict):
    #         black_list_sector = black_list_items.get("Sector", "")
    #         black_list_number = black_list_items.get("BlacklistNumber", "")
    #         black_list_date = black_list_items.get("BlacklistedDate", "")
    #         black_list_type = black_list_items.get("BlacklistType", "")
    #         black_list_relation = black_list_items.get("NatureOfRelation", "")

    #     # Insert data into the table for the current record
    #     self.cur.execute(f"""
    #         INSERT INTO {Constants.INDIVIDUAL_TABLE_NAME} (
    #             Name, DOB, Gender, FatherName,
    #             CitizenshipCount, CitizenshipNumber, CitizenshipIssuedDate, CitizenshipIssuedDistrict,
    #             PassportCount, DrivingLicenseCount, VoterIdCount, PANCount, IndianEmbassyCount,
    #             BlackListCount, BlackListSector, BlackListNumber, BlackListDate, BlackListType, BlackListRelation
    #         )
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     """, (
    #         name, dob, gender, father_name,
    #         citizenship_count, citizenship_number, citizenship_issued_date, citizenship_issued_district,
    #         passport_count, driving_license_count, voter_id_count, pan_count, indian_embassy_count,
    #         black_list_count, black_list_sector, black_list_number, black_list_date, black_list_type, black_list_relation
    #     ))
    #         # self.con.commit()
    #         # self.con.close()












        