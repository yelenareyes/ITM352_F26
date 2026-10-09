
# Step 6: Randomize the question order and answer choices

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

random.shuffle(questions)
score = 0
labels = "abcd"

for item in questions:
    choices = item["choices"][:]
    random.shuffle(choices)

    # Make a label-to-answer dictionary after shuffling.
    answer_choices = {}
    for i in range(len(choices)):
        answer_choices[labels[i]] = choices[i]

    print("\n" + item["question"])
    for label, choice in answer_choices.items():
        print(label + ")", choice)

    answer = input("Choose a, b, c, or d: ").lower().strip()
    while answer not in answer_choices:
        answer = input("Please choose a, b, c, or d: ").lower().strip()

    if answer == item["answer"]:
        print("Correct!")
        score += 1
    else:
        print("Correct answer:", item["answer"])
        

