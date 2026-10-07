# Interactive quiz system, fifth version
# make a dictionary with the questions and correct answers
# Allow the user to choose the option by its label 
# Improve the look and usabiloty. Keep track of correct answers.

from string import ascii_lowercase

questions = {
    "What is the capital of France?": ["Paris", "Nice", "Avignon"],
    "What is the capital of Japan?": ["Tokyo", "Shinjuku", "Kyoto"],
    "What is the sirspeed of an unladen swallow?": ["10 m/s", "20 m/s", "30 m/s"],
    "The Last Supper was painted by which artist?": ["Leonardo da Vinci", "Arvaggio", "Michelangelo"]
}
num_correct = 0


for num,(question, answers) in enumerate(questions.items(), start=1):
    correct_answer = answers[0]
    print(f"\nQuestion {num}: {question}")

sorted_answers = sorted(answers)
labeled_answers = dict(zip(ascii_lowercase, sorted_answers))


for label, answer in labeled_answers.items():
    print(f"{label}. {answer}")

answer_label = input("Choice?").lower()
answer = labeled_answers.get(answer_label)

if answer == correct_answer:
    print("Correct!")
    num_correct += 1
else:
    print(f"The answer is {correct_answer!r}, not {answer!r}.")

print(f"\nYou got {num_correct} out of {num_questions} correct.")