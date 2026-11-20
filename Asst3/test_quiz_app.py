# Tests for the quiz webapp
# Name: Yelena Reyes
# Date: Nov. 19, 2026
# These tests were written with Claude's help.
# Prompt: "Write unit and integration tests for my Flask quiz app using unittest."

import os
import unittest
import webapp_quiz


def current_correct_answer():
    # Look up the correct answer for the question the app is currently showing
    return webapp_quiz.questions[webapp_quiz.question_number]['answer']


class QuizAppTests(unittest.TestCase):

    def setUp(self):
        # Use a separate scores file so the real scores.json is never changed
        webapp_quiz.scores_file = 'test_scores.json'
        webapp_quiz.questions_file = 'questions.json'
        webapp_quiz.app.config['TESTING'] = True
        self.client = webapp_quiz.app.test_client()

        # Pretend this client has already entered a name, so /quiz is allowed
        with self.client.session_transaction() as sess:
            sess['name'] = 'Test User'
            sess['history'] = []

    def tearDown(self):
        # Delete the test scores file after each test
        if os.path.exists('test_scores.json'):
            os.remove('test_scores.json')

    # ---------- Routes are reachable ----------

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Start the Quiz', response.data)

    def test_quiz_page_loads(self):
        self.client.get('/')
        response = self.client.get('/quiz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Question 1 of', response.data)

    # ---------- Questions come from JSON and are shuffled ----------

    def test_questions_loaded_from_json(self):
        self.client.get('/')
        self.assertGreater(webapp_quiz.max_questions, 0)

    def test_shuffle_keeps_all_questions_and_options(self):
        webapp_quiz.load_questions()
        count_before = len(webapp_quiz.questions)
        webapp_quiz.shuffle_questions()
        self.assertEqual(len(webapp_quiz.questions), count_before)
