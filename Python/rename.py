import os

def rename_files():
    file_list = os.listdir(r"/Users/Coder/Documents/Python/prank")
    os.chdir(r"/Users/Coder/Documents/Python/prank")
    for file_name in file_list:
        new_name = file_name.translate(None, "0123456789")
        os.rename(file_name, new_name)
        
rename_files()

