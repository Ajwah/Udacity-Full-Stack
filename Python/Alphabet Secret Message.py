import os
from random import randrange
os.chdir(r"/Users/Coder/Documents/Python/alphabet")

def scramble():
    file_list = os.listdir(r"/Users/Coder/Documents/Python/alphabet")
    file_list.pop(0)
    for file_name in file_list:
        i = randrange(0, 1000)
        print(str(i) + file_name)
        os.rename(file_name, str(i) + file_name)

def create_message():
    file_list = os.listdir(r"/Users/Coder/Documents/Python/alphabet")
    file_list.pop(0)
    for file_name in file_list:
        new_name = file_name.translate(None, "0123456789")
        os.rename(file_name, new_name)

scramble()
raw_input("Press Enter to continue...")       
create_message()

