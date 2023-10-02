import os

DB_PATH = os.path.join(os.getcwd(), 'output')
# DB_NAME = os.path.join(DB_PATH,'cib_delta_screening.db')
DB_NAME = os.path.join(DB_PATH,'test.db')
INDIVIDUAL_TABLE_NAME = 'Individuals'
INSTITUTIONS_TABLE_NAME = 'Institutions'
FLAG_FILE_PATH = os.path.join(os.getcwd(), 'output','first_run_flag.txt')