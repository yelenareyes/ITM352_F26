●      Data Structure Justification: What data structure design was used to store the quiz questions and why is the best for the application? Explain the design quality goals for this? E.g. readability by human, easy to read from a file, etc. Do not simply list the goals. Explain them relative to storing quiz questions.

The questions are stored in a JSON file as a list of dictionaries. Each dictionary represents one question and has named fields such as category, question, choices, correct_answers, hint, and explanation. For example, choices is a list of possible answers, while correct_answers is a list of accepted correct answers.
This design separates the question content from the Python program. That makes the question bank easier for a person to read and edit, and JSON lets Python load it directly with json.load(). The list also lets the program loop through questions, filter them by category, and shuffle their order. Keeping each question’s information together in a dictionary makes it clearer which choices, answer, hint, and explanation belong together. The named fields are more readable than relying on positions in a long list.


●      Function Design: Why did you design your non-trivial custom function the way you did, and what specific problem does it solve in the application?


A useful example is ask_question(item, fifty_fifty_used). It handles the steps for one question: shuffling and labeling the choices, displaying the question, processing a hint or 50/50 request, checking the selected answer, and calculating points.

It takes the current question as item so the same function can work with different question dictionaries instead of duplicating that logic for every question. It also takes fifty_fifty_used so the function can enforce the once-per-quiz limit. It returns both the points earned and whether the lifeline has been used, allowing run_quiz() to update the score and pass the lifeline state to the next question.


●      Control Flow: A brief explanation of how the application handles invalid user inputs (e.g., preventing inputs outside of "a-d") and why you chose that validation loop structure. Explain the design quality goals for this? E.g. Do not simply list the goals. Explain them relative to storing quiz questions[RK1] .


Inside ask_question(), a while True loop keeps asking for input until the player enters a valid answer or a recognized command. The code normalizes the response with .lower().strip(), so uppercase letters and extra spaces don’t cause otherwise valid input to be rejected. It checks answer labels against answer_choices, the dictionary of choices currently available. That matters after 50/50 removes two options: the player can select only a label that is still displayed. The loop also handles h for a hint and f for the lifeline.

I used a loop because the player can correct an invalid entry immediately and continue the same question, rather than ending the quiz or accidentally checking an invalid answer. The program also uses a separate validation loop in choose_category() to keep asking until the user enters a category number in range. In both cases, validation is based on the options the program actually presented.


●      Use of AI: You must also include a statement on how you used AI (Copilot or any other tool) in the creation of this assignment.  Be honest: if we ask you to explain your code and you cannot, that will mean that you relied too heavily on AI.

I used GitHub Copilot/AI as a coding assistant and tutor while working on this quiz. It helped me discuss the code structure, add and test features, and prepare explanations. I reviewed the code and tests, but I am responsible for understanding the final program and being able to explain how its data structures, functions, and input validation work.
 
Tip: You can use the design document as guidance to your coding agent or copilot to ensure the code implements the designs explained.
