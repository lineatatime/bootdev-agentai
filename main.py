import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

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

        response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt))
        print(response.text)

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
