# Interactivve quiz system, second version
# make a dictionary with the questions and correct answers

questions = {
    "What is the capital of France?": ["Paris", "Nice", "Avignon"],
    "What is the capital of Japan?": ["Tokyo", "Shinjuku", "Kyoto"],
    "The Last Supper was painted by which artist?": ["Leonardo da Vinci", "Arvaggio", "Michelangelo"]
}

for question, answers in questions.items():
    correct_answer = answers[0]
    sorted_answers = sorted(answers)

for label, answer in enumerate(sorted_answers, start=1):
    print(f"{label}. {answer}")

answer_label = int(input(f"{question}"))
answer = sorted_answers[answer_label - 1]

if answer == correct_answer:
    print("Correct!")
else:
        print(f"The answer is {correct_answer}, not {answer!r}.")