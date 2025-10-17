import os

def get_files_info(working_directory, directory="."):
    root_dir = os.path.abspath("../")
    working_directory = os.path.join(root_dir, working_directory)
    full_path = os.path.join(working_directory, directory)
    abs_rel_path = os.path.abspath(directory)
    abs_wrk_path = os.path.abspath(working_directory)
    if full_path.startswith(working_directory) == False:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if os.path.isdir(directory) == False:
        print(f'Error: "{directory}" is not a directory')
    for item in os.listdir(full_path):
        item_size = 0
        if os.path.isdir(item):
            for i in os.listdir(item):
                if os.path.isfile(i):
                    item_size += os.path.getsize(i)
        # else: item_size += os.path.getsize(item)
        item_is_dir = os.path.isdir(item)
        print(f"{item}: file_size={item_size}, is_dir={item_is_dir}")
    print(f"Root directory: {root_dir}")
    print(f"Working directory: {working_directory}")
    print(f"Join working_directory and directory: {full_path}")
    # print(f"Absolute path for relative directory: {abs_rel_path}")
    print(f"Absolute path for working directory: {abs_wrk_path}")
    print(f"List files in joined directory: {os.listdir(full_path)}")

get_files_info("calculator")