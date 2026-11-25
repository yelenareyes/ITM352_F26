import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent / ".env")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API_KEY"]
)
MODEL = "openrouter/free" # You may need to deliberately select a model that supports structured https://openrouter.ai/models?variant=free

user_message = "My name is Yelena"
my_messages = [
    {"role": "user", "content": user_message},
]
response = client.chat.completions.create(
    model=MODEL,
    messages=my_messages
)
saved_response = response.choices[0].message.content
print("First response:")
print(first_message := response.choices[0].message.content)

second_message = [
    {"role": "user", "content": "What is my name?"}
]

response = client.chat.completions.create(
    model=MODEL,
    messages=second_message
)

print("\nSecond response:")
print(response.choices[0].message.content)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": "What is my name?"},
        {"role": "assistant", "content": saved_response}
    ]
)
