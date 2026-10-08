
# Filipino 101 Study Quiz - Step 8
# Loads questions from questions.json using json and pathlib.Path.
# Built with beginner-level lists, dictionaries, loops, and functions.

import json
import random

QUESTION_FILE = "questions.json" 
SCORE_FILE = "scores.txt"
LABELS = "abcd"


def choose_category(categories):
    """Let the user choose a category or practice everything."""
    print("\nCategories")
    print("0) All categories")

    for number in range(len(categories)):
        print(str(number + 1) + ") " + categories[number])

    choice = input("Choose a category number: ").strip()

    while (
        not choice.isdigit()
        or int(choice) < 0
        or int(choice) > len(categories)
    ):
        choice = input("Enter 0 through " + str(len(categories)) + ": ").strip()

    if int(choice) == 0:
        return "All categories"

    return categories[int(choice) - 1]


def ask_question(item):
    """Display a question and return 1 if correct, otherwise 0."""
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

    while answer not in answer_choices:
        if answer == "h":
            print("Hint:", item["hint"])
        else:
            print("Please enter a, b, c, d, or h.")

        answer = input("Your answer: ").lower().strip()

    selected_answer = answer_choices[answer]

    if selected_answer in item["correct_answers"]:
        print("Correct!")
        print("Explanation:", item["explanation"])
        return 1

    print("Not quite.")
    print("Correct answer(s):", ", ".join(item["correct_answers"]))
    print("Explanation:", item["explanation"])
    return 0


def save_score(score, total, category):
    """Append a simple score record to scores.txt."""
    with open(SCORE_FILE, "a", encoding="utf-8") as file:
        file.write(category + ": " + str(score) + "/" + str(total) + "\n")


def run_quiz():
    """Run the quiz and return the score, total, and category."""
    with open(QUESTION_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = data["categories"]
    selected_category = choose_category(categories)

    selected_questions = []

    for item in data["questions"]:
        if (
            selected_category == "All categories"
            or item["category"] == selected_category
        ):
            selected_questions.append(item)

    if len(selected_questions) == 0:
        print("No questions found for that category.")
        return 0, 0, selected_category

    random.shuffle(selected_questions)
    score = 0
    total_questions = len(selected_questions)

    print("\nFilipino 101 Study Quiz")
    print("Questions:", total_questions)

    for item in selected_questions:
        score += ask_question(item)

    save_score(score, total_questions, selected_category)
    print("Score saved in scores.txt")

    return score, total_questions, selected_category


if __name__ == "__main__":
    final_score, total_questions, selected_category = run_quiz()
    print("\nCategory:", selected_category)
    print("Score:", final_score, "out of", total_questions)

    if total_questions > 0:
        percentage = final_score / total_questions * 100
        print("Percentage:", round(percentage), "%")