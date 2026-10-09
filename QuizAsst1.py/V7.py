# Step 7: Use functions to organize repeated tasks

import random

questions = [
    {
        "question": "What does masaya mean?",
        "choices": ["sad", "happy", "tired", "angry"],
        "answer": "happy"
    },
    {
        "question": "What does pagod mean?",
        "choices": ["thirsty", "excited", "tired", "hungry"],
        "answer": "tired"
    }
]

def ask_question(item):
    labels = "abcd"
    choices = item["choices"][:]
    random.shuffle(choices)

    answer_choices = {}
    for i in range(len(choices)):
        answer_choices[labels[i]] = choices[i]

    print("\n" + item["question"])
    for label, choice in answer_choices.items():
        print(label + ")", choice)

    answer = input("Choose a, b, c, or d: ").lower().strip()
    while answer not in answer_choices:
        answer = input("Please choose a, b, c, or d: ").lower().strip()

    if answer_choices[answer] == item["answer"]:
        print("Correct!")
        return 1
    else:
        print("Correct answer:", item["answer"])
        return 0

def run_quiz():
    random.shuffle(questions)
    score = 0

    for item in questions:
        score += ask_question(item)

    print("\n"+"Final score:", score, "out of", len(questions))
    return score

final_score = run_quiz()
print("Score:", final_score, "out of", len(questions))

