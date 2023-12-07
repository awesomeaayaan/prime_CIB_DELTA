# import sqlite3

# # Connect to the database (you can change this to your preferred database type)
# conn = sqlite3.connect('example.db')
# cursor = conn.cursor()

# # Create the Individual table
# cursor.execute('''
#     CREATE TABLE Individual (
#         ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         BranchCode TEXT,
#         CBSClientCode TEXT,
#         CBSAccountNumber TEXT,
#         AccountDescription TEXT,
#         CBSAccountStatus TEXT,
#         CBSAccountName TEXT,
#         "Name Match %" TEXT,
#         CBSFatherName TEXT,
#         FatherNamePercentage TEXT,
#         CBSDOB_BS TEXT,
#         DOBMatchPercentage TEXT,
#         CBSCitizenshipNo TEXT,
#         CitizenshipMatchPercentage TEXT,
#         TotalSimilarityPercentage TEXT,
#         ResultOfCIBScreening TEXT,
#         CIBName TEXT,
#         CIBFatherName TEXT,
#         CIBDOB TEXT,
#         CIBCitizenshipNo TEXT,
#         CIBGender TEXT,
#         CIBBlackListedNo TEXT,
#         CIBBlackListedDate TEXT,
#         DrivingLicenceNo TEXT,
#         IndianEmbassyRegNo TEXT,
#         PANNo TEXT,
#         PassportNo TEXT
#     )
# ''')

# # Create the CIBData table
# cursor.execute('''
#     CREATE TABLE CIBData (
#         ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         IndividualID INTEGER,
#         BranchCode TEXT,
#         CBSClientCode TEXT,
#         CBSAccountNumber TEXT,
#         AccountDescription TEXT,
#         CBSAccountStatus TEXT,
#         CBSAccountName TEXT,
#         "Name Match %" TEXT,
#         CBSFatherName TEXT,
#         FatherNamePercentage TEXT,
#         CBSDOB_BS TEXT,
#         DOBMatchPercentage TEXT,
#         PANNo TEXT,
#         PANNumberPercentage TEXT,
#         TotalSimilarityPercentage TEXT,
#         ResultOfCIBScreening TEXT,
#         CIBName TEXT,
#         CIBFatherName TEXT,
#         CIBDOB TEXT,
#         CIBPANNo TEXT,
#         CIBGender TEXT,
#         CIBBlackListedNo TEXT,
#         CIBBlackListedDate TEXT,
#         DrivingLicenceNo TEXT,
#         IndianEmbassyRegNo TEXT,
#         # CIBPANNo TEXT,
#         PassportNo TEXT
#     )
# ''')

# # Commit changes and close connection
# conn.commit()
# conn.close()
# import sqlite3

# # Connect to the SQLite database (replace 'example.db' with your database file)
# conn = sqlite3.connect('example.db')

# # Create a cursor object to execute SQL statements
# cursor = conn.cursor()

# # Create the Email table if it doesn't already exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Email (
#         Email_ID TEXT,
#         Status INTEGER
#     )
# ''')

# # Insert sample data into the Email table
# sample_data = [
#     ('ramgautam@gmail.com', 0)
# ]
# print(sample_data)
# cursor.executemany('INSERT INTO Email (Email_ID, Status) VALUES (?, ?)', sample_data)
# print('successfully insert data to the table email')
# # Commit the changes and close the connection
# conn.commit()
# conn.close()

import sqlite3

# Connect to the SQLite database (replace 'example.db' with your database file)
conn = sqlite3.connect('example.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()
cursor.execute('''
        SELECT * FROM Email where Status == '0'
''')
# Fetch all the rows as a list of tuples
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row[0])

conn.commit()
conn.close()

# import sqlite3

# def update_email_status(email_list):
#     # Connect to the SQLite database (replace 'example.db' with your database file)
#     conn = sqlite3.connect('example.db')

#     # Create a cursor object to execute SQL statements
#     cursor = conn.cursor()

#     # Update the status to 1 for emails in the list
#     for email in email_list:
#         cursor.execute('''
#             UPDATE Email
#             SET Status = 1
#             WHERE Email_ID = ?
#         ''', (email,))

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

# Example usage
# email_list_to_update = ['aayaangautam.com.np', 'another@example.com']

# update_email_status(email_list_to_update)
# print('successfully update the email in database')
