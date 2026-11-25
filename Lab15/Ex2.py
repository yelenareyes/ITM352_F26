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


messages = [
    {"role": "system", "content": "You are a pirate-themed assistant for Aloha Bikes, a bike rental shop in Waikiki. Answer in 2 sentences or less."},
    {"role": "user", "content": "What should I bring on a bike ride to Diamond Head?"}
]
response = client.chat.completions.create(
    model=MODEL,
    messages=messages
)

print(response.choices[0].message.content)

