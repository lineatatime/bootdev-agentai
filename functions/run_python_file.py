import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the Python file at the specified file path with the specified arguements, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the Python file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguements to pass into the specified Python file on execution, relative to the working directory. If not provided, attempt to execute the specified Python file without arguements.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(full_path)
        abs_wrk_path = os.path.abspath(working_directory)
        if abs_path.startswith(abs_wrk_path) == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.exists(full_path) == False:
            return f'Error: File "{file_path}" not found.'
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file.'
        args_list = ["uv", "run", full_path]
        args_list.extend(args)
        result = subprocess.run(args_list, timeout=30, capture_output=True)
        if result.returncode == 0:
            return f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        if result.returncode != 0:
            return f"STDOUT: {result.stdout} STDERR: {result.stderr} Process exited with code {result.returncode}"
        if result.stdout == "":
            return f"No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"