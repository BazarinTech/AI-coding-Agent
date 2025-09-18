import os
from dotenv import load_dotenv
from google import genai
import sys


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print('I need a prompt!')
        sys.exit(1)

    prompt = sys.argv[1]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=prompt
    )

    print(response.text)

    if response is None or response.usage_metadata is None:
        print('Response is maliformed')
        return

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
