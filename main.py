import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_files import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

functions_dict = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_call_part.args["working_directory"] = "./calculator"
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: print(f" - Calling function: {function_call_part.name}")
    if function_call_part.name in functions_dict:
        function_result = functions_dict[function_call_part.name](**function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

def main():
    if len(sys.argv) < 2:
        print('Usage: uv run main.py <"prompt">')
        sys.exit(1)
    else:
        model = "gemini-2.0-flash-001"

        user_prompt = sys.argv[1]

        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]

        response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

        if response.function_calls == None:
            print(response.text)
        else:
            for f in response.function_calls:
                if len(sys.argv) > 2:
                    flag = sys.argv[2]
                    if flag == "--verbose":
                        function_call_result = call_function(f, verbose=True)
                else: function_call_result = call_function(f)
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception
                else:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        if len(sys.argv) > 2:
            flag = sys.argv[2]
            if flag == "--verbose":
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
