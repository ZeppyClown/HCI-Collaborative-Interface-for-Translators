import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI()
secret_key = os.getenv("OPENAI_API_KEY")


def test_prompt(prompt, model="gpt-4.1"):
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response


def mandarin_to_eng(input, model="gpt-4.1"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"Translate to English: {input}"}],
    )
    return response


def main():
    p = "Hello. Testing OpenAI API"
    response = test_prompt(p)
    print(response.choices[0].message.content)
    return


if __name__ == "__main__":
    main()
