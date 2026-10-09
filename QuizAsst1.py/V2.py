# Step 2: Store several questions in a list of tuples

questions = [
    ("What does masaya mean?", "happy"),
    ("What does pagod mean?", "tired"),
    ("What does gutom mean?", "hungry")
]

score = 0

for question, correct_answer in questions:
    print(question)
    answer = input("Your answer: ")

    if answer.lower() == correct_answer:
        print("Correct!")
        score = score + 1
    else:
        print("The answer is", correct_answer)

print("Final score:", score, "out of", len(questions))

