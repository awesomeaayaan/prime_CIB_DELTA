import zipfile
import Constants
import os

# zipfile_path = f'{Constants.ACCUITY_PATH}'

# extract_to_path = f'{Constants.ACCUITY_PATH}'

# # file_to_extract = ''
# zip_files = [file for file in zipfile_path if file.endswith('.zip')]
# # for zipfile.ZipFile(zipfile_path,'r') as zip_ref:
    

# download_directory = f'{Constants.ACCUITY_PATH}'
# zip_file = os.listdir(download_directory)
# print(f'File is {zip_file}')
# # zip_files = [file for file in zip_file if file.endswith('.zip')]
# # print(zip_files)
# zip_file_path = f'{Constants.ACCUITY_PATH}'
# for file in zip_file:
#     print(f'File is {file}')
#     with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
#         zip_ref.extractall(file,download_directory)
#         print('successfully extrat the zip file')
# # display(f'zip file list is ==> {zip_file}')
# print(f'zip file list is ==> {zip_file}')
# # for file in zip_files:
# #     print(f'file is {file}')
# zip_file_path = os.path.join(download_directory,zip_files[0])
# extract_directory = download_directory
# print(f'Extract directory is {extract_directory}')
# with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
#     zip_ref.extractall(zip_files[0],extract_directory)
# # display('Successfully extract the zip files in its location')
# print('Successfully extract the zip files in its location')

download_directory = f'{Constants.ACCUITY_PATH}'
zip_file = os.listdir(download_directory)
# zip_files = [file for file in zip_file if file.endswith('.zip')]
print(f'zip file list is ==> {zip_file}')
for file in zip_file:
    zip_file_path = os.path.join(download_directory,file)
    extract_directory = download_directory
    with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
        zip_ref.extractall(extract_directory)
print('Successfully extract the zip files in its location')
