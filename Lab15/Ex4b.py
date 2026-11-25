import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from mycontent import MENU, INFO, MODEL, build_system_prompt

load_dotenv(Path(__file__).resolve().parent / ".env")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API_KEY"]
)
MODEL = "openrouter/free"

system_context = input("Enter system context (or leave blank for default): ")
if not system_context.strip():
    system_context = build_system_prompt(MENU, INFO)
messages = [{"role": "system", "content": system_context}]

print("Welcome to the Aloha Bikes assistant! Type your message below. Type 'exit', 'quit', or 'bye' to end the conversation.")

while True:
    user_text = input("You: ")
    if user_text.lower() in ("exit", "quit", "bye"):
        break
    if not user_text.strip():
        print("Please enter a message.")
        continue
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content
    print(f"Assistant: {reply}")
    messages.append({"role": "assistant", "content": reply})

    # 1. Exit if the user types quit
    # 2. Append the user's message to messages
    # 3. Call client.chat.completions.create() with the full messages list
    # 4. Print the reply
    # 5. Append the reply as an assistant message