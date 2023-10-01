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
