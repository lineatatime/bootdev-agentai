import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the specified content to a file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, relative to the working directory. If not provided, use default untitled.txt.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file, relative to the working directory. If not provided, use an empty string.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(full_path)
        abs_wrk_path = os.path.abspath(working_directory)
        if abs_path.startswith(abs_wrk_path) == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Exception occurred - {e}"