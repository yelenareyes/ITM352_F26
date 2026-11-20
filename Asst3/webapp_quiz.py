# Application to manage the quiz webapp
# Name: Yelena Reyes
# Date: Nov. 19, 2026

import json
import random
import time
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

# Global variables
score = 0
question_number = 0
questions = []
max_questions = 0
error_message = ""
start_time = None
time_taken = None
score_saved = False
missed_questions = []
questions_file = 'questions.json'
scores_file = 'scores.json'

app = Flask(__name__)

# A secret key lets Flask sign the session cookie so users cannot change it.
# permanent_session_lifetime keeps the cookie for a year, so returning users are remembered.
app.secret_key = 'quiz-app-secret-key'
app.permanent_session_lifetime = timedelta(days=365)


def load_questions():
    # Load the questions from the JSON file instead of hard-coding them.
    # If the file is missing or broken, save a friendly message to show the user.
    global questions, max_questions, error_message
    error_message = ""
    try:
        with open(questions_file, 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        questions = []
        error_message = "Sorry, the question file could not be found."
    except json.JSONDecodeError:
        questions = []
        error_message = "Sorry, the question file is not formatted correctly."

    max_questions = len(questions)


def shuffle_questions():
    # Randomize the question order and the answer options for each new session
    random.shuffle(questions)
    for q in questions:
        random.shuffle(q['options'])


# The read_scores() and write_scores() functions were written with Claude's help.
# Prompt: "Store user score data in a JSON file using server-side Python."
def read_scores():
    # Get the saved scores from the scores file (an empty list if there are none yet)
    try:
        with open(scores_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_scores(scores):
    # Save the full list of scores back to the scores file
    with open(scores_file, 'w') as file:
        json.dump(scores, file, indent=4)


# The session (cookie) code below was written with Claude's help.
# Prompt: "Use sessions to remember a user's name and quiz score history between visits."
@app.route('/')
def index():
    global score, question_number, start_time, time_taken, score_saved, missed_questions
    score = 0
    question_number = 0
    start_time = None
    time_taken = None
    score_saved = False
    missed_questions = []
    load_questions()
    shuffle_questions()
    # name is None on a first visit, so the page will ask for a name instead
    return render_template('index.html', error=error_message,
                           name=session.get('name'),
                           history=session.get('history', []))


@app.route('/setname', methods=['POST'])
def set_name():
    # Save the first-time visitor's name in the session cookie
    name = request.form.get('name', '').strip()

    # Validation: the name cannot be empty or too long
    if name == "" or len(name) > 20:
        return render_template('index.html', error=error_message, name=None, history=[],
                               name_error="Please enter a name (1 to 20 characters).")

    session.permanent = True
    session['name'] = name
    session['history'] = []
    return redirect(url_for('index'))


@app.route('/switch')
def switch_user():
    # Forget the saved name and history so a different person can use the quiz
    session.pop('name', None)
    session.pop('history', None)
    return redirect(url_for('index'))


@app.route('/quiz')
def quiz():
    # Show the current question, or go to the results page if the quiz is over
    global start_time

    if 'name' not in session:
        # Visitors must enter their name on the start page first
        return redirect(url_for('index'))

    if max_questions == 0:
        return redirect(url_for('index'))

    if start_time is None:
        # Start the timer when the first question is displayed
        start_time = time.time()

    if question_number < max_questions:
        return render_template('quiz.html',
                               question=questions[question_number]['question'],
                               question_number=question_number + 1,
                               max_questions=max_questions,
                               score=score,
                               options=questions[question_number]['options'],
                               answered=False)
    else:
        return redirect(url_for('results'))


# The answer() and next_question() functions were written with Claude's help.
# Prompt: "Show right/wrong feedback after each answer before moving to the next question."
@app.route('/answer', methods=['POST'])
def answer():
    # Check the submitted answer and show feedback on the same question
    global score

    if max_questions == 0 or question_number >= max_questions:
        # Validation: no quiz is in progress, so send the user back to the start page
        return redirect(url_for('index'))

    selected = request.form.get('answer')
    current = questions[question_number]

    if selected is None:
        # Validation: the user clicked Submit without choosing an option
        return render_template('quiz.html',
                               question=current['question'],
                               question_number=question_number + 1,
                               max_questions=max_questions,
                               score=score,
                               options=current['options'],
                               answered=False,
                               error="Please choose an answer before submitting.")

    is_correct = (selected == current['answer'])
    if is_correct:
        score += 1
    else:
        # Keep track of the missed question so it can be reviewed on the results page
        missed_questions.append({"question": current['question'],
                                 "your_answer": selected,
                                 "correct_answer": current['answer'],
                                 "explanation": current['explanation']})

    return render_template('quiz.html',
                           question=current['question'],
                           question_number=question_number + 1,
                           max_questions=max_questions,
                           score=score,
                           options=current['options'],
                           answered=True,
                           selected=selected,
                           is_correct=is_correct,
                           correct_answer=current['answer'],
                           explanation=current['explanation'])


@app.route('/next')
def next_question():
    # Move on to the next question after the user has seen the feedback
    global question_number
    question_number += 1
    return redirect(url_for('quiz'))


@app.route('/results')
def results():
    # Display the final score, the time taken, and save the score once
    global time_taken, score_saved

    if max_questions == 0 or start_time is None:
        return redirect(url_for('index'))

    if time_taken is None:
        # Calculate the time only once so refreshing the page does not change it
        time_taken = round(time.time() - start_time)

    if not score_saved:
        # Save this attempt to the scores file under the user's name
        scores = read_scores()
        scores.append({"name": session.get('name', 'Player'), "score": score,
                       "total": max_questions, "time_taken": time_taken})
        write_scores(scores)

        # Add this attempt to the user's score history in the session cookie
        # (only the last 10 are kept so the cookie stays small)
        history = session.get('history', [])
        history.append({"date": time.strftime('%b %d, %Y'), "score": score,
                        "total": max_questions, "time_taken": time_taken})
        session['history'] = history[-10:]

        score_saved = True

    return render_template('results.html', score=score,
                           max_questions=max_questions, time_taken=time_taken,
                           missed=missed_questions)


# The two API routes below were written with Claude's help.
# Prompt: "Add RESTful API routes to get the questions and to store/retrieve user scores."
@app.route('/api/questions', methods=['GET'])
def api_questions():
    # Return the questions and options as JSON (the correct answers are not included)
    if max_questions == 0:
        return jsonify({"error": "Questions are not loaded. Visit the home page first."}), 404

    safe_questions = []
    for q in questions:
        safe_questions.append({"question": q['question'], "options": q['options']})
    return jsonify(safe_questions)


@app.route('/api/scores', methods=['GET', 'POST'])
def api_scores():
    # GET returns all saved scores, POST validates and saves a new score
    if request.method == 'POST':
        data = request.get_json(silent=True)

        # Validation: make sure the data is there and has the right types
        if data is None:
            return jsonify({"error": "Please send the score as JSON."}), 400
        if not isinstance(data.get('name'), str) or data['name'].strip() == "":
            return jsonify({"error": "A name is required."}), 400
        if not isinstance(data.get('score'), int) or not isinstance(data.get('total'), int):
            return jsonify({"error": "Score and total must be whole numbers."}), 400

        scores = read_scores()
        scores.append({"name": data['name'].strip(), "score": data['score'],
                       "total": data['total'], "time_taken": data.get('time_taken', 0)})
        write_scores(scores)
        return jsonify({"message": "Score saved."}), 201

    return jsonify(read_scores())


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()