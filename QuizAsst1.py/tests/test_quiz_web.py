import json
import re
import tempfile
import time
import unittest
from pathlib import Path

import quiz_web


class QuizWebsiteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.media_dir = self.root / "media"
        self.media_dir.mkdir()
        (self.media_dir / "sample.png").write_bytes(b"sample image")
        (self.media_dir / "sample.mp4").write_bytes(b"sample video")
        self.question_file = self.root / "questions.json"
        self.question_file.write_text(
            json.dumps(
                {
                    "categories": ["Media"],
                    "questions": [
                        {
                            "id": 1,
                            "category": "Media",
                            "question": "Which is the correct answer?",
                            "choices": ["correct one", "wrong one", "wrong two", "wrong three"],
                            "correct_answers": ["correct one"],
                            "hint": "A hint",
                            "explanation": "Because it is correct.",
                            "media": {
                                "type": "image",
                                "filename": "sample.png",
                                "alt": "Sample image",
                            },
                        },
                        {
                            "id": 2,
                            "category": "Media",
                            "question": "Which video is shown?",
                            "choices": ["right", "incorrect A", "incorrect B", "incorrect C"],
                            "correct_answers": ["right"],
                            "hint": "Watch the clip.",
                            "explanation": "The clip shows the correct choice.",
                            "media": {
                                "type": "video",
                                "filename": "sample.mp4",
                                "alt": "Sample video",
                            },
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        quiz_web.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            DATABASE=str(self.root / "quiz.sqlite3"),
            QUESTION_FILE=str(self.question_file),
            MEDIA_DIR=str(self.media_dir),
        )
        with quiz_web.app.app_context():
            quiz_web.init_db()
        self.client = quiz_web.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def csrf_token(self, path="/login"):
        response = self.client.get(path)
        match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
        self.assertIsNotNone(match)
        return match.group(1).decode()

    def register(self, username):
        token = self.csrf_token("/register")
        return self.client.post(
            "/register",
            data={"csrf_token": token, "username": username, "password": "correct horse"},
        )

    def test_user_can_play_use_lifeline_and_save_high_score(self):
        self.register("Alice")
        token = self.csrf_token("/")
        response = self.client.post(
            "/quiz",
            data={"csrf_token": token, "category": "Media"},
        )
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as browser_session:
            user_id = browser_session["user_id"]
        with quiz_web.app.app_context():
            run = quiz_web.get_db().execute(
                "SELECT id FROM quiz_runs WHERE user_id = ?", (user_id,)
            ).fetchone()
        run_id = run["id"]

        page = self.client.get(f"/quiz/{run_id}")
        self.assertEqual(page.status_code, 200)
        media_markup = page.data
        image_response = self.client.get("/media/sample.png")
        video_response = self.client.get("/media/sample.mp4")
        self.assertEqual(image_response.status_code, 200)
        self.assertEqual(video_response.status_code, 200)
        image_response.close()
        video_response.close()
        token = self.csrf_token(f"/quiz/{run_id}")
        self.client.post(
            f"/quiz/{run_id}",
            data={"csrf_token": token, "action": "fifty_fifty"},
        )
        with quiz_web.app.app_context():
            run = quiz_web.get_db().execute(
                "SELECT * FROM quiz_runs WHERE id = ?", (run_id,)
            ).fetchone()
            self.assertEqual(run["fifty_fifty_used"], 1)
            self.assertEqual(len(json.loads(run["eliminated_json"])), 2)

        response = self.client.post(
            f"/quiz/{run_id}",
            data={"csrf_token": token, "action": "fifty_fifty"},
            follow_redirects=True,
        )
        self.assertIn(b"already been used", response.data)

        with quiz_web.app.app_context():
            run = quiz_web.get_db().execute(
                "SELECT * FROM quiz_runs WHERE id = ?", (run_id,)
            ).fetchone()
            questions = json.loads(run["questions_json"])
            eliminated = json.loads(run["eliminated_json"])
            question = questions[run["current_index"]]
            answer = next(
                choice
                for choice in question["correct_answers"]
                if choice not in eliminated
            )
            quiz_web.get_db().execute(
                "UPDATE quiz_runs SET question_started_at = ? WHERE id = ?",
                (time.time() - 2, run_id),
            )
            quiz_web.get_db().commit()
        self.client.post(
            f"/quiz/{run_id}",
            data={
                "csrf_token": token,
                "action": "answer",
                "answer": answer,
            },
        )
        media_markup += self.client.get(f"/quiz/{run_id}").data
        self.assertIn(b"<img", media_markup)
        self.assertIn(b"<video", media_markup)

        token = self.csrf_token(f"/quiz/{run_id}")
        with quiz_web.app.app_context():
            run = quiz_web.get_db().execute(
                "SELECT * FROM quiz_runs WHERE id = ?", (run_id,)
            ).fetchone()
            questions = json.loads(run["questions_json"])
            question = questions[run["current_index"]]
            answer = question["correct_answers"][0]
            quiz_web.get_db().execute(
                "UPDATE quiz_runs SET question_started_at = ? WHERE id = ?",
                (time.time() - 11, run_id),
            )
            quiz_web.get_db().commit()
        result = self.client.post(
            f"/quiz/{run_id}",
            data={
                "csrf_token": token,
                "action": "answer",
                "answer": answer,
            },
            follow_redirects=True,
        )
        self.assertIn(b"75%", result.data)
        self.assertIn(b"Grand champion: <strong>Alice</strong>", result.data)

        with quiz_web.app.app_context():
            user = quiz_web.get_db().execute(
                "SELECT high_score_percent, high_score_points, high_score_total "
                "FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
            self.assertEqual(user["high_score_percent"], 75.0)
            self.assertEqual(user["high_score_points"], 3)
            self.assertEqual(user["high_score_total"], 4)

        leaderboard = self.client.get("/leaderboard")
        self.assertIn(b"Alice", leaderboard.data)
        self.assertIn(b"75%", leaderboard.data)

    def test_media_validation_prevents_path_traversal(self):
        malicious_question = {
            "media": {"type": "image", "filename": "../secret.txt"}
        }
        with quiz_web.app.test_request_context():
            with self.assertRaises(ValueError):
                quiz_web.validate_question_media(malicious_question)

    def test_post_requires_csrf_token(self):
        response = self.client.post("/register", data={"username": "Alice", "password": "x"})
        self.assertEqual(response.status_code, 400)

    def test_login_requires_valid_credentials(self):
        self.register("Alice")
        self.client.post("/logout", data={"csrf_token": self.csrf_token("/")})
        token = self.csrf_token("/login")
        response = self.client.post(
            "/login",
            data={"csrf_token": token, "username": "Alice", "password": "wrong password"},
            follow_redirects=True,
        )
        self.assertIn(b"Invalid username or password", response.data)
        token = self.csrf_token("/login")
        response = self.client.post(
            "/login",
            data={"csrf_token": token, "username": "alice", "password": "correct horse"},
        )
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
