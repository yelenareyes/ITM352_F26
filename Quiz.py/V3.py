# Step 3: Each question is a dictionary with answer choices

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

score = 0

for item in questions:
    print(item["question"])
    for choice in item["choices"]:
        print("-", choice)

    answer = input("Your answer: ").lower()

    if answer == item["answer"]:
        print("Correct!")
        score += 1
    else:
        print("Correct answer:", item["answer"])

print("Score:", score, "out of", len(questions))

