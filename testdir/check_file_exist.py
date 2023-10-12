import os

def check_file_exist(file_path):
    """
    Check if a file exists and print the result.

    Args:
        file_path (str): The path to the file to be checked.
    """
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
    else:
        print(f"The file '{file_path}' does not exist.")

# Example usage:
fname=rootpath+"file_name1"
fname2=root_path+"file_name2"
#or list of files:
file_lists=[fname1, fname2]
for f in file_lists:
    check_file_exist(f)
