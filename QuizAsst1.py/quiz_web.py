"""Flask website for the Filipino 101 quiz."""

import json
import os
import random
import re
import secrets
import sqlite3
import time
from functools import wraps
from pathlib import Path, PurePosixPath

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
SPEED_BONUS_SECONDS = 10

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("QUIZ_SECRET_KEY") or secrets.token_hex(32),
    DATABASE=os.environ.get("QUIZ_DATABASE", str(BASE_DIR / "quiz_users.sqlite3")),
    QUESTION_FILE=os.environ.get("QUIZ_QUESTION_FILE", str(BASE_DIR / "questions.json")),
    MEDIA_DIR=os.environ.get("QUIZ_MEDIA_DIR", str(BASE_DIR / "static" / "media")),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("QUIZ_HTTPS", "").lower() in {"1", "true"},
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    high_score_percent REAL,
    high_score_points INTEGER,
    high_score_total INTEGER
);

CREATE TABLE IF NOT EXISTS quiz_runs (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    category TEXT NOT NULL,
    questions_json TEXT NOT NULL,
    current_index INTEGER NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 0,
    fifty_fifty_used INTEGER NOT NULL DEFAULT 0,
    eliminated_json TEXT NOT NULL DEFAULT '[]',
    choices_json TEXT NOT NULL,
    question_started_at REAL NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0
);
"""


def get_db():
    """Return this request's SQLite connection."""
    if "db" not in g:
        database_path = Path(app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path, timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db():
    """Create the account and quiz-run tables if they do not exist."""
    database = get_db()
    database.executescript(SCHEMA)
    database.commit()


def load_question_bank():
    with open(app.config["QUESTION_FILE"], "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


@app.before_request
def protect_post_requests():
    if request.method == "POST":
        supplied_token = request.form.get("csrf_token", "")
        expected_token = session.get("csrf_token", "")
        if not expected_token or not secrets.compare_digest(
            supplied_token, expected_token
        ):
            abort(400, description="Invalid or missing form security token.")


@app.context_processor
def inject_template_values():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["csrf_token"]}


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = get_db().execute(
        "SELECT username, high_score_percent, high_score_points, high_score_total "
        "FROM users WHERE id = ?",
        (session["user_id"],),
    ).fetchone()
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    categories = load_question_bank()["categories"]
    return render_template("index.html", user=user, categories=categories)


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        error = None

        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,24}", username):
            error = "Username must be 3-24 characters: letters, numbers, _, ., or -."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        if error is None:
            database = get_db()
            try:
                cursor = database.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                database.commit()
            except sqlite3.IntegrityError:
                database.rollback()
                error = "That username is already registered."
            else:
                session.clear()
                session["user_id"] = cursor.lastrowid
                return redirect(url_for("index"))

        flash(error, "error")

    return render_template("register.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT id, password_hash FROM users WHERE username = ? COLLATE NOCASE",
            (username,),
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout", methods=("POST",))
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/leaderboard")
def leaderboard():
    champion = get_db().execute(
        "SELECT username, high_score_percent, high_score_points, high_score_total "
        "FROM users WHERE high_score_percent IS NOT NULL "
        "ORDER BY high_score_percent DESC, high_score_points DESC, username COLLATE NOCASE "
        "LIMIT 1"
    ).fetchone()
    users = get_db().execute(
        "SELECT username, high_score_percent, high_score_points, high_score_total "
        "FROM users WHERE high_score_percent IS NOT NULL "
        "ORDER BY high_score_percent DESC, high_score_points DESC, username COLLATE NOCASE"
    ).fetchall()
    return render_template("leaderboard.html", champion=champion, users=users)


def validate_question_media(question):
    media = question.get("media")
    if media is None:
        return None
    if not isinstance(media, dict) or media.get("type") not in {"image", "video"}:
        raise ValueError("Question media must have type 'image' or 'video'.")

    filename = media.get("filename")
    if not isinstance(filename, str) or "\\" in filename:
        raise ValueError("Media filename must be a relative path under static/media.")
    relative_path = PurePosixPath(filename)
    if (
        not filename
        or relative_path.is_absolute()
        or any(part in {"", ".", ".."} for part in relative_path.parts)
    ):
        raise ValueError("Media filename must be a safe relative path under static/media.")

    media_path = Path(app.config["MEDIA_DIR"]).joinpath(*relative_path.parts)
    if not media_path.is_file():
        raise FileNotFoundError(f"Question media file was not found: {media_path}")

    return {
        "type": media["type"],
        "url": url_for("media_file", filename=relative_path.as_posix()),
        "alt": str(media.get("alt", "Question media")),
    }


@app.route("/media/<path:filename>")
def media_file(filename):
    return send_from_directory(app.config["MEDIA_DIR"], filename)


@app.route("/quiz", methods=("POST",))
@login_required
def start_quiz():
    bank = load_question_bank()
    category = request.form.get("category", "")
    categories = bank["categories"]
    if category != "All categories" and category not in categories:
        abort(400, description="Select a valid quiz category.")

    questions = [
        question
        for question in bank["questions"]
        if category == "All categories" or question["category"] == category
    ]
    if not questions:
        flash("No questions are available for that category.", "error")
        return redirect(url_for("index"))

    for question in questions:
        choices = question.get("choices", [])
        correct_answers = question.get("correct_answers", [])
        if (
            len(choices) != 4
            or len(correct_answers) < 1
            or not set(correct_answers).issubset(choices)
            or len([choice for choice in choices if choice not in correct_answers]) < 2
        ):
            raise ValueError(
                f"Question {question.get('id')} must have four choices, "
                "at least one correct answer, and at least two incorrect answers."
            )
        validate_question_media(question)

    random.shuffle(questions)
    first_choices = questions[0]["choices"][:]
    random.shuffle(first_choices)
    run_id = secrets.token_urlsafe(24)
    database = get_db()
    database.execute(
        "INSERT INTO quiz_runs "
        "(id, user_id, category, questions_json, choices_json, question_started_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            run_id,
            session["user_id"],
            category,
            json.dumps(questions),
            json.dumps(first_choices),
            time.time(),
        ),
    )
    database.commit()
    return redirect(url_for("play_quiz", run_id=run_id))


def get_quiz_run(run_id):
    run = get_db().execute(
        "SELECT * FROM quiz_runs WHERE id = ? AND user_id = ?",
        (run_id, session["user_id"]),
    ).fetchone()
    if run is None:
        abort(404)
    return run


@app.route("/quiz/<run_id>", methods=("GET", "POST"))
@login_required
def play_quiz(run_id):
    database = get_db()
    run = get_quiz_run(run_id)
    if run["completed"]:
        return redirect(url_for("quiz_result", run_id=run_id))

    questions = json.loads(run["questions_json"])
    index = run["current_index"]
    question = questions[index]
    choices = json.loads(run["choices_json"])
    eliminated = json.loads(run["eliminated_json"])

    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "hint":
            flash(question["hint"], "hint")
        elif action == "fifty_fifty":
            if run["fifty_fifty_used"]:
                flash("The 50/50 feature has already been used this quiz.", "error")
            else:
                wrong_choices = [
                    choice
                    for choice in choices
                    if choice not in question["correct_answers"]
                    and choice not in eliminated
                ]
                if len(wrong_choices) < 2:
                    flash("50/50 is unavailable for this question.", "error")
                else:
                    eliminated.extend(random.sample(wrong_choices, k=2))
                    database.execute(
                        "UPDATE quiz_runs SET fifty_fifty_used = 1, eliminated_json = ? "
                        "WHERE id = ?",
                        (json.dumps(eliminated), run_id),
                    )
                    database.commit()
                    flash("50/50 used: two incorrect choices were removed.", "success")
        elif action == "answer":
            selected_answer = request.form.get("answer", "")
            visible_choices = [choice for choice in choices if choice not in eliminated]
            if selected_answer not in visible_choices:
                flash("Choose one of the available answers.", "error")
                return redirect(url_for("play_quiz", run_id=run_id))

            elapsed = max(0.0, time.time() - run["question_started_at"])
            points_earned = 0
            correct = selected_answer in question["correct_answers"]
            if correct:
                points_earned = 1
                if elapsed <= SPEED_BONUS_SECONDS:
                    points_earned += 1

            next_index = index + 1
            score = run["score"] + points_earned
            completed = next_index >= len(questions)
            if completed:
                total_possible = len(questions) * 2
                percentage = score / total_possible * 100
                database.execute(
                    "UPDATE users SET high_score_percent = ?, high_score_points = ?, "
                    "high_score_total = ? WHERE id = ? AND "
                    "(high_score_percent IS NULL OR high_score_percent < ? OR "
                    "(high_score_percent = ? AND high_score_points < ?))",
                    (
                        percentage,
                        score,
                        total_possible,
                        session["user_id"],
                        percentage,
                        percentage,
                        score,
                    ),
                )
            else:
                next_choices = questions[next_index]["choices"][:]
                random.shuffle(next_choices)
                database.execute(
                    "UPDATE quiz_runs SET current_index = ?, score = ?, eliminated_json = '[]', "
                    "choices_json = ?, question_started_at = ? WHERE id = ?",
                    (
                        next_index,
                        score,
                        json.dumps(next_choices),
                        time.time(),
                        run_id,
                    ),
                )

            if completed:
                database.execute(
                    "UPDATE quiz_runs SET current_index = ?, score = ?, completed = 1 "
                    "WHERE id = ?",
                    (next_index, score, run_id),
                )
            database.commit()
            if correct:
                message = f"Correct! You earned {points_earned} point(s)."
                if points_earned == 2:
                    message += " That includes the 10-second speed bonus."
                flash(message, "success")
            else:
                flash("Not quite. " + question["explanation"], "error")
            if completed:
                return redirect(url_for("quiz_result", run_id=run_id))
            return redirect(url_for("play_quiz", run_id=run_id))
        else:
            abort(400, description="Invalid quiz action.")

        return redirect(url_for("play_quiz", run_id=run_id))

    media = validate_question_media(question)
    return render_template(
        "question.html",
        run=run,
        question=question,
        choices=choices,
        eliminated=eliminated,
        media=media,
        question_number=index + 1,
        total_questions=len(questions),
        elapsed_seconds=max(0.0, time.time() - run["question_started_at"]),
        speed_bonus_seconds=SPEED_BONUS_SECONDS,
    )


@app.route("/quiz/<run_id>/result")
@login_required
def quiz_result(run_id):
    run = get_quiz_run(run_id)
    if not run["completed"]:
        return redirect(url_for("play_quiz", run_id=run_id))
    total_questions = len(json.loads(run["questions_json"]))
    total_possible = total_questions * 2
    percentage = round(run["score"] / total_possible * 100)
    champion = get_db().execute(
        "SELECT username FROM users WHERE high_score_percent IS NOT NULL "
        "ORDER BY high_score_percent DESC, high_score_points DESC, username COLLATE NOCASE "
        "LIMIT 1"
    ).fetchone()
    return render_template(
        "result.html",
        run=run,
        total_questions=total_questions,
        total_possible=total_possible,
        percentage=percentage,
        champion=champion,
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run()
