import os
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content from the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get file content from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(full_path)
        abs_wrk_path = os.path.abspath(working_directory)
        if abs_path.startswith(abs_wrk_path) == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        item_size = os.path.getsize(full_path)
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if item_size > MAX_CHARS:
            file_content_string = f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: Exception occurred - {e}"