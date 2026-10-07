First version of the quiz game
# Name: Rick Kazman
# Date: October 2, 2026

answer = input("What is the capital of France? ")
if answer == "Paris":
    print("Correct!")
else:
    print(f"The answer is Paris, not {answer!r}.")

answer = input("What is the capital of Japan? ")
if answer == "Tokyo":
    print("Correct!")
else:
    print(f"The answer is Tokyo, not {answer!r}.")