# Step 4: Select an answer using labels a, b, c, and d

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

for item in questions:
    print("\\n" + item["question"])
    for label, choice in item["choices"].items():
        print(label + ")", choice)

    answer = input("Choose a, b, c, or d: ").lower()

    if answer == item["answer"]:
        print("Correct!")
    else:
        print("Correct answer:", item["answer"], ")", item["choices"][item["answer"]])


