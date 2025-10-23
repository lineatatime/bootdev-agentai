import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_path = os.path.abspath(full_path)
        abs_wrk_path = os.path.abspath(working_directory)
        files_in_dir = os.listdir(full_path)
        dir_details = []
        if abs_path.startswith(abs_wrk_path) == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(full_path) == False:
            return f'Error: "{directory}" is not a directory'
        for item in files_in_dir:
            item_path = os.path.join(full_path, item)
            # print(f"Item: {item}, File Path: {item_path}")
            item_size = os.path.getsize(item_path)
            is_file = os.path.isfile(item_path)
            item_is_dir = os.path.isdir(item_path)
            dir_details.append(f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}")
        return "\n".join(dir_details)
    except Exception as e:
        return f"Error: Exception occurred - {e}"