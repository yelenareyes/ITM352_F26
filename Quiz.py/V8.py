
# Filipino 101 Study Quiz - Step 8
# Loads questions from questions.json using json and pathlib.Path.
# Built with beginner-level lists, dictionaries, loops, and functions.

import json
import random
import time

QUESTION_FILE = "questions.json" 
SCORE_FILE = "scores.txt"
LABELS = "abcd"
SPEED_BONUS_SECONDS = 10


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


def ask_question(item, fifty_fifty_used):
    """Ask one question and return points earned and lifeline usage."""
    choices = item["choices"][:]
    random.shuffle(choices)

    answer_choices = {}

    for i in range(len(choices)):
        answer_choices[LABELS[i]] = choices[i]

    print("\nCategory:", item["category"])
    print(item["question"])

    for label, choice in answer_choices.items():
        print(label + ") " + choice)

    question_start = time.perf_counter()
    while True:
        answer = input(
            "Choose a, b, c, or d (h for hint, f for 50/50): "
        ).lower().strip()

        if answer == "h":
            print("Hint:", item["hint"])
        elif answer == "f":
            if fifty_fifty_used:
                print("The 50/50 feature has already been used.")
            else:
                wrong_labels = []
                for label, choice in answer_choices.items():
                    if choice not in item["correct_answers"]:
                        wrong_labels.append(label)

                if len(wrong_labels) < 2:
                    print("The 50/50 feature is not available for this question.")
                else:
                    labels_to_remove = random.sample(wrong_labels, k=2)
                    for label in labels_to_remove:
                        del answer_choices[label]
                    fifty_fifty_used = True
                    print("50/50 used. Two incorrect choices were removed.")
                    for label, choice in answer_choices.items():
                        print(label + ") " + choice)
        elif answer in answer_choices:
            break
        else:
            print("Please enter an available answer label, h, or f.")

    elapsed_time = time.perf_counter() - question_start
    print("Time:", round(elapsed_time, 1), "seconds")
    selected_answer = answer_choices[answer]

    if selected_answer in item["correct_answers"]:
        print("Correct!")
        print("Explanation:", item["explanation"])
        if elapsed_time <= SPEED_BONUS_SECONDS:
            print("Speed bonus: +1 point for answering within 10 seconds!")
            return 2, fifty_fifty_used
        print("No speed bonus this time.")
        return 1, fifty_fifty_used

    print("Not quite.")
    print("Correct answer(s):", ", ".join(item["correct_answers"]))
    print("Explanation:", item["explanation"])
    return 0, fifty_fifty_used


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
    fifty_fifty_used = False

    print("\nFilipino 101 Study Quiz")
    print("Questions:", total_questions)
    print("Each correct answer is worth 1 point, with a +1 speed bonus")
    print("for answers submitted within", SPEED_BONUS_SECONDS, "seconds.")

    for item in selected_questions:
        question_score, fifty_fifty_used = ask_question(item, fifty_fifty_used)
        score += question_score

    max_score = total_questions * 2
    save_score(score, max_score, selected_category)
    print("Score saved in scores.txt")

    return score, max_score, selected_category


if __name__ == "__main__":
    final_score, max_score, selected_category = run_quiz()
    print("\nCategory:", selected_category)
    print("Score:", final_score, "out of", max_score, "possible points")

    if max_score > 0:
        percentage = final_score / max_score * 100
        print("Percentage:", round(percentage), "%")