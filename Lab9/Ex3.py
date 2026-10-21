import json
from pathlib import Path

questions = {
    "What is the capital of France?": ["Paris", "Nice", "Avignon"],
    "What is the capital of Japan?": ["Tokyo", "Shinjuku", "Kyoto"],
    "The Last Supper was painted by which artist?": [
        "Leonardo da Vinci",
        "Arvaggio",
        "Michelangelo",
    ],
    "What is the capital of Italy?": ["Rome", "Milan", "Naples"],
    "The Mona Lisa was painted by which artist?": [
        "Leonardo da Vinci",
        "Raphael",
        "Michelangelo",
    ],
    "What is the capital of Spain?": ["Madrid", "Barcelona", "Seville"],
}

json_path = Path(__file__).with_name("questions.json")
with json_path.open("w", encoding="utf-8") as json_file:
    json.dump(questions, json_file, indent=2, ensure_ascii=False)

print(f"Saved quiz questions to {json_path.name}")
