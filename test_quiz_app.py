import unittest
import sqlite3
from unittest.mock import patch
from main import QuizApp

class QuizAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QuizApp()
        cls.app.connection = sqlite3.connect(':memory:')
        cls.app.cursor = cls.app.connection.cursor()

    def test_show_question(self):
        self.app.current_level = 0
        self.app.current_question = 0

        self.app.show_question()

        # Verify that the question is displayed correctly
        expected_question = "Which country has won the most Copa America titles?"
        self.assertIn(expected_question, self.app.label_question["text"])

    @patch('tkinter.messagebox.showinfo')
    def test_check_answer_correct(self, mock_showinfo):
        self.app.current_level = 0
        self.app.current_question = 0
        self.app.score = 0

        self.app.check_answer(0)  # Select the correct answer

        # Verify that the score is updated and the message box is not shown
        self.assertEqual(self.app.score, 1)
        mock_showinfo.assert_called_once_with("Correct!", "You answered correctly!")

    @patch('tkinter.messagebox.showinfo')
    def test_check_answer_incorrect(self, mock_showinfo):
        self.app.current_level = 0
        self.app.current_question = 0
        self.app.score = 0

        self.app.check_answer(1)  # Select an incorrect answer

        # Verify that the score remains unchanged and the message box is not shown
        self.assertEqual(self.app.score, 0)
        mock_showinfo.assert_not_called()

    @patch('tkinter.simpledialog.askstring', return_value="John Doe")
    def test_save_high_score(self, mock_askstring):
        self.app.score = 5

        self.app.save_high_score()

        # Retrieve the saved high scores from the database
        self.app.cursor.execute('SELECT * FROM high_scores')
        high_scores = self.app.cursor.fetchall()

        # Verify that the high score is saved correctly in the database
        self.assertEqual(len(high_scores), 1)
        self.assertEqual(high_scores[0][0], 'John Doe')
        self.assertEqual(high_scores[0][1], 5)

    @patch('tkinter.messagebox.showinfo')
    def test_show_high_scores(self, mock_showinfo):
        # Insert some sample high scores into the database
        high_scores_data = [('John Doe', 10), ('Jane Smith', 8)]
        self.app.cursor.executemany('INSERT INTO high_scores VALUES (?, ?)', high_scores_data)

        self.app.show_high_scores()

        # Verify that the message box is shown with the expected high scores
        expected_high_scores = "High Scores:\n\n1. John Doe - 10\n2. Jane Smith - 8\n"
        mock_showinfo.assert_called_once_with("High Scores", expected_high_scores)

    def test_next_question(self):
        self.app.current_question = 0

        self.app.next_question()

        # Verify that the current question is incremented
        self.assertEqual(self.app.current_question, 1)

    @classmethod
    def tearDownClass(cls):
        cls.app.connection.close()

if __name__ == '__main__':
    unittest.main()
