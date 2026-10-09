# Filipino 101 Study Quiz - Step 8
# Loads questions from questions.json using json and pathlib.Path.
# Built with beginner-level lists, dictionaries, loops, and functions.

import json
import random
from pathlib import Path

QUESTION_FILE = Path(__file__).parent / "questions.json"
SCORE_FILE = Path(__file__).parent / "scores.txt"
LABELS = "abcd"


def load_questions():
    """Read the question bank from the JSON file."""
    with open(QUESTION_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def choose_category(categories):
    """Let the user choose a category or practice everything."""
    print("\nCategories")
    print("0) All categories")
    for number in range(len(categories)):
        print(str(number + 1) + ") " + categories[number])

    choice = input("Choose a category number: ").strip()
    while not choice.isdigit() or int(choice) < 0 or int(choice) > len(categories):
        choice = input("Enter 0 through " + str(len(categories)) + ": ").strip()

    if int(choice) == 0:
        return "All categories"
    return categories[int(choice) - 1]


def ask_question(item):
    """Display one multiple-choice question and return 1 for correct, 0 otherwise."""
    choices = item["choices"][:]
    random.shuffle(choices)

    answer_choices = {}
    for i in range(len(choices)):
        answer_choices[LABELS[i]] = choices[i]

    print("\nCategory:", item["category"])
    print(item["question"])
    for label, choice in answer_choices.items():
        print(label + ") " + choice)

    answer = input("Choose a, b, c, or d (or h for hint): ").lower().strip()
    while answer == "h":
        print("Hint:", item["hint"])
        answer = input("Your answer (a, b, c, or d): ").lower().strip()

    while answer not in answer_choices:
        answer = input("Please enter a, b, c, or d (or h): ").lower().strip()
        if answer == "h":
            print("Hint:", item["hint"])
            answer = input("Your answer (a, b, c, or d): ").lower().strip()

    selected_answer = answer_choices[answer]
    if selected_answer in item["correct_answers"]:
        print("Correct!")
        print("Explanation:", item["explanation"])
        return 1
    else:
        print("Not quite.")
        print("Correct answer(s):", ", ".join(item["correct_answers"]))
        print("Explanation:", item["explanation"])
        return 0


def save_score(score, total, category):
    """Append a simple score record to scores.txt."""
    with open(SCORE_FILE, "a", encoding="utf-8") as file:
        file.write(category + ": " + str(score) + "/" + str(total) + "\n")


def run_quiz():
    data = load_questions()
    categories = data["categories"]
    category = choose_category(categories)

    selected_questions = []
    for item in data["questions"]:
        if category == "All categories" or item["category"] == category:
            selected_questions.append(item)

    if len(selected_questions) == 0:
        print("No questions found for that category.")
        return

    random.shuffle(selected_questions)
    score = 0

    print("\nFilipino 101 Study Quiz")
    print("Questions:", len(selected_questions))
    for item in selected_questions:
        score += ask_question(item)

    print("\nFinal score:", score, "out of", len(selected_questions))
    percentage = score / len(selected_questions) * 100
    print("Percentage:", round(percentage), "%")
    save_score(score, len(selected_questions), category)
    print("Score saved in scores.txt")


run_quiz()
