# Step 5: Add score tracking and basic input validation

questions = [
    {
        "question": "What does masaya mean?",
        "choices": {"a": "sad", "b": "happy", "c": "tired", "d": "angry"},
        "answer": "b"
    },
    {
        "question": "What does pagod mean?",
        "choices": {"a": "thirsty", "b": "excited", "c": "tired", "d": "hungry"},
        "answer": "c"
    }
]

score = 0

for item in questions:
    print("\n" + item["question"])
    for label, choice in item["choices"].items():
        print(label + ")", choice)

    answer = input("Choose a, b, c, or d: ").lower().strip()
    while answer not in item["choices"]:
        print("Please enter a, b, c, or d.")
        answer = input("Your answer: ").lower().strip()

    if answer == item["answer"]:
        print("Correct!")
        score += 1
    else:
        print("Not quite. The answer is", item["answer"] + ")",
              item["choices"][item["answer"]])

print("\nYou scored", score, "out of", len(questions))

