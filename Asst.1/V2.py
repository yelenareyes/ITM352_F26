# Interactivve quiz system, second version
# Make a list with questions and correct answers

questions =[
    ("What is the capital of France?", "Paris"),
    ("What is the capital of Japan?", "Tokyo"), 
    ("The Last Supper was painted by which artist?", "Leonardo da Vinci"),
]


for question, correct_answer in questions:
    answer = input(f"{question} ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is {correct_answer}, not {answer!r}.")