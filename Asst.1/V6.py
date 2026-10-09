# Interactive quiz system, sixth version
# Make a dictionary with the questions and correct answers
# Allow the user to choose the option by its label
# Improve the look and usability. Keep track of correct answers.
# Randomize the order of the questions and the order of the answers for each question.

from string import ascii_lowercase
import random

questions ={
    "What is the capital of France?": ["Paris", "Nice", "Avignon"],
    "What is the capital of Japan?": ["Tokyo", "Shinjuku", "Kyoto"],
    "The Last Supper was painted by which artist?": ["Leonardo da Vinci", "Arvaggio", "Michelangelo"],
    "What is the capital of Italy?": ["Rome", "Milan", "Naples"],
    "The Mona Lisa was painted by which artist?": ["Leonardo da Vinci", "Raphael", "Michelangelo"],
    "What is the capital of Spain?": ["Madrid", "Barcelona", "Seville"],
    }
    
NUM_QUESTIONS_PER_QUIZ = 5

num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(questions))
selected_questions = random.sample(list(questions.items()), k=num_questions)

num_correct = 0

for num, (question, answers) in enumerate(selected_questions, start=1):
    correct_answer = answers[0]
    print(f"\nQuestion {num}: {question}")

    sorted_answers = sorted(answers)
    labeled_answers = dict(zip(ascii_lowercase, random.sample(sorted_answers, k=len(sorted_answers))))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")
        
    while (answer_label := input("Choice? ").lower()) not in labeled_answers:
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

    answer = labeled_answers.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer!r}', not {answer!r}.")

print(f"\nYou got {num_correct} out of {len(questions)} correct.")

from string import ascii_lowercase
import json
import random
from pathlib import Path

with Path(__file__).with_name("questions.json").open(encoding="utf-8") as questions_file:
    questions = json.load(questions_file)