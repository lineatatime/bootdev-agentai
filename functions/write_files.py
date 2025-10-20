import os

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