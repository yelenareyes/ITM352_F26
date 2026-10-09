# Step 4: Select an answer using labels a, b, c, and d

questions = [
    {
        "question": "What does masaya mean?",
        "choices": {"a": "sad", "b": "happy", "c": "joyful", "d": "angry"},
        "answers": ["b", "c"]
    },
    {
        "question": "What does pagod mean?",
        "choices": {"a": "thirsty", "b": "excited", "c": "tired", "d": "exhausted"},
        "answers": ["c", "d"]
    }
]

for item in questions:
    print("\n" + item["question"])
    for label, choice in item["choices"].items():
        print(label + ")", choice)

    answer = input("Choose all correct answers, separated by commas (e.g. a, c): ")
    answers = {label.strip().lower() for label in answer.split(",")}

    while not answers.issubset(item["choices"]):
        answer = input("Enter valid labels separated by commas: ")
        answers = {label.strip().lower() for label in answer.split(",")}

    correct_answers = set(item["answers"])
    if answers == correct_answers:
        print("Correct!")
    else:
        print("Correct answers:")
        for label in sorted(correct_answers):
            print(label + ")", item["choices"][label])
