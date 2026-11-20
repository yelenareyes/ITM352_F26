# Quiz Web App

Name: Yelena Reyes
Course: ITM 352
Date: Nov. 19, 2026

A Flask web version of my console quiz game. Questions are loaded from a JSON file,
shuffled for each session, and graded with feedback after every answer.

## Setup

1. Install Python 3 and Flask:
   `pip install flask`
2. Put all of these in the same folder:
   - `webapp_quiz.py`
   - `questions.json`
   - `test_quiz_app.py`
   - `static/style.css`
   - `templates/index.html`, `quiz.html`, `results.html`

## How to run

From the project folder, run:

`python webapp_quiz.py`

Then open http://127.0.0.1:5000 in a browser.

## How to use

1. Click **Start the Quiz**.
2. Pick an answer and click **Submit Answer**. You will see whether it was right or
   wrong, the correct answer, and a short explanation.
3. Click **Next** to continue.
4. At the end, the results page shows correct and incorrect counts, your score,
   the time taken, and the questions you missed.
5. Click **Play Again** to restart with a new random order.

## How to run the tests

`python test_quiz_app.py`

The tests use a separate `test_scores.json` file, so real scores are not changed.

## Project files

| File | Purpose |
|------|---------|
| `webapp_quiz.py` | Flask app: routes, question loading, shuffling, scoring, score saving, REST APIs |
| `questions.json` | All questions, answer options, correct answers, and explanations |
| `scores.json` | Saved scores (created automatically after the first completed quiz) |
| `templates/` | Jinja HTML pages for the start, question, and results screens |
| `static/style.css` | Styling, including a layout for small phone screens |
| `test_quiz_app.py` | Unit and integration tests |

## REST API

| Route | Method | Description |
|-------|--------|-------------|
| `/api/questions` | GET | Returns the questions and options as JSON (no answers included) |
| `/api/scores` | GET | Returns all saved scores |
| `/api/scores` | POST | Validates and saves a new score. Needs `name`, `score`, `total` |

## Design choices

- **Questions in JSON:** questions can be added or changed without touching the code.
- **Answer stored as text:** the correct answer is saved as text, not a position, so
  shuffling the options never breaks grading.
- **Feedback before moving on:** `/answer` checks the answer and shows the result on
  the same question. `/next` moves to the next one.
- **Time and score saved once:** the time is calculated and the score saved only the
  first time the results page loads, so refreshing does not add duplicates.
- **API leaves out answers:** `/api/questions` does not include the correct answers.
- **Error handling:** a missing or broken question file, an empty answer, and bad API
  data each give a clear message instead of crashing.

## Use of AI

Claude was used for parts of this project. Each AI-assisted function has a comment
in the code saying where it was used and what the prompt was. See the separate
"Use of AI" document for details.