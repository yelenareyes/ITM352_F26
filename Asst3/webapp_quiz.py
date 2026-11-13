# Application to manage the quiz webapp
# Name: Yelena Reyes
# Date: Nov. 13, 2026

from flask import Flask, render_template, request, redirect, url_for

# Global variables
score = 0
question_number = 0
questions = (
    {
        "questions": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"]
    },
    {
        "questions": "What is the largest planet in our solar system?",
        "options": ["Jupiter", "Saturn", "Earth", "Mars"]
    }
)

max_questions = len(questions)

app = Flask(__name__)

@app.route('/')
def index():
    global score, question_number
    score = 0
    question_number = 0
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global score, question_number, max_questions, questions

    if request.method == 'POST':
        # Capture the answer from the form
        answer = request.form.get('answer')

        # Check if the answer is correct
        if answer == questions[question_number]['options'][0]:  # Assuming the first option is correct
            score += 1
        question_number += 1

    if question_number < max_questions:
        # Render the next question
        return render_template('quiz.html', 
                               question=questions[question_number]['questions'], 
                               question_number=question_number + 1,
                               options=questions[question_number]['options'])
    else:
        # Quiz is over, redirect to the result page
        return render_template('results.html', score=score, max_questions=max_questions)

    @app.route
    def results():
        # Display the final score
        global score, max_questions
        return render_template('results.html', score=score, max_questions=max_questions)    

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()