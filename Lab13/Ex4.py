"""A navigable Flask mock-up for a future quiz game."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('quiz_home.html')


@app.route('/instructions')
def instructions():
    return render_template('quiz_instructions.html')


@app.route('/question')
def question():
    return render_template('quiz_question.html')


@app.route('/results')
def results():
    return render_template('quiz_results.html')


if __name__ == '__main__':
    app.run(debug=True)
