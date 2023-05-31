import tkinter as tk
from tkinter import simpledialog
import sqlite3

class QuizApp:
    def __init__(self):
        self.levels = [
            {
                "name": "Level 1",
                "questions": [
                    {
                        "text": "Which country has won the most Copa America titles?",
                        "options": ["Brazil", "Argentina", "Uruguay", "Chile"],
                        "correct": 0
                    },
                    {
                        "text": "Who is the all-time leading goal scorer in the UEFA Champions League?",
                        "options": ["Cristiano Ronaldo", "Lionel Messi", "Robert Lewandowski", "Raul"],
                        "correct": 0
                    },
                    {
                        "text": "Which team has won the most FIFA World Cup titles?",
                        "options": ["Brazil", "Germany", "Italy", "Argentina"],
                        "correct": 0
                    },
                    {
                        "text": "Who is the manager of the Manchester City football club as of 2023?",
                        "options": ["Pep Guardiola", "Jurgen Klopp", "Jose Mourinho", "Carlo Ancelotti"],
                        "correct": 0
                    },
                    {
                        "text": "Who is the all-time leading goal scorer in the history of the UEFA European Championship?",
                        "options": ["Cristiano Ronaldo", "Michel Platini", "Antoine Griezmann", "Thierry Henry"],
                        "correct": 0
                    },
                    {
                        "text": "Who scored the famous Hand of God goal in the 1986 FIFA World Cup quarter-final?",
                        "options": ["Pele", "Lionel Messi", "Diego Maradona", "Zinedine Zidane"],
                        "correct": 2
                    },
                    {
                        "text": "Which city is home to both AC Milan and Inter Milan?",
                        "options": ["Rome", "Milan", "Turin", "Naples"],
                        "correct": 1
                    },
                    # Add more questions for Level 1
                ]
            },
            {
                "name": "Level 2",
                "questions": [
                    {
                        "text": "Which player has won the most Ballon d'Or awards?",
                        "options": ["Lionel Messi", "Cristiano Ronaldo", "Michel Platini", "Johan Cruyff"],
                        "correct": 0
                    },
                    {
                        "text": "Which player has scored the most goals in a single UEFA Champions League season?",
                        "options": ["Lionel Messi", "Cristiano Ronaldo", "Robert Lewandowski", "Raul"],
                        "correct": 2
                    },
                    {
                        "text": "Who is the all-time leading goal scorer for the Brazilian national team?",
                        "options": ["Pele", "Ronaldo", "Romario", "Neymar"],
                        "correct": 0
                    },
                    {
                        "text": "Which club has won the most Serie A titles in Italy?",
                        "options": ["Inter Milan", "AC Milan", "Juventus", "Roma"],
                        "correct": 2
                    },
                    {
                        "text": "Who is the all-time leading goal scorer in the history of the FIFA World Cup?",
                        "options": ["Ronaldo", "Miroslav Klose", "Gerd Muller", "Just Fontaine"],
                        "correct": 1
                    },
                    {
                        "text": "Which country won the first-ever FIFA World Cup in 1930?",
                        "options": ["Brazil", "Germany", "Uruguay", "Italy"],
                        "correct": 2
                    },
                    {
                        "text": "Who is the only player to have won the UEFA Champions League with three different clubs?",
                        "options": ["Cristiano Ronaldo", "Lionel Messi", "Zlatan Ibrahimovic", "Clarence Seedorf"],
                        "correct": 1
                    },
                    # Add more questions for Level 2
                ]
            },
            # Add more levels here...
        ]

        self.current_level = 0
        self.current_question = 0
        self.score = 0

        self.window = tk.Tk()
        self.window.title("Football Quiz Game")

        self.label_question = tk.Label(self.window, text="", wraplength=300)
        self.label_question.pack(pady=20)

        self.option_buttons = []

        self.next_button = tk.Button(self.window, text="Next", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.pack(pady=10)

        self.connection = sqlite3.connect('quiz.db')
        self.cursor = self.connection.cursor()
        self.create_high_scores_table()

        self.show_question()

    def create_high_scores_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                player_name TEXT,
                score INT
            )
        ''')
        self.connection.commit()

    def show_question(self):
        level = self.levels[self.current_level]
        questions = level["questions"]
        question = questions[self.current_question]

        self.label_question.config(text=f"{level['name']}\n\n{question['text']}")

        for button in self.option_buttons:
            button.destroy()

        self.option_buttons = []

        for i, option in enumerate(question["options"]):
            option_button = tk.Button(self.window, text=option, width=30, command=lambda i=i: self.check_answer(i))
            option_button.pack(pady=5)
            self.option_buttons.append(option_button)

        self.next_button.config(state=tk.DISABLED)

    def check_answer(self, selected_option):
        level = self.levels[self.current_level]
        questions = level["questions"]
        question = questions[self.current_question]

        if selected_option == question["correct"]:
            self.score += 1
            tk.messagebox.showinfo("Correct!", "You answered correctly!")

        self.current_question += 1

        if self.current_question == len(questions):
            if self.current_level == len(self.levels) - 1:
                self.save_high_score()
                self.show_high_scores()
                self.window.destroy()
            else:
                self.current_level += 1
                self.current_question = 0
                self.show_question()
        else:
            self.score_label.config(text=f"Score: {self.score}/{self.current_question}")
            self.show_question()

    def save_high_score(self):
        player_name = simpledialog.askstring("Congratulations!", "Enter your name:")
        self.cursor.execute('INSERT INTO high_scores VALUES (?, ?)', (player_name, self.score))
        self.connection.commit()

    def show_high_scores(self):
        self.cursor.execute('SELECT * FROM high_scores ORDER BY score DESC')
        high_scores = self.cursor.fetchall()

        high_scores_str = "High Scores:\n\n"
        for i, row in enumerate(high_scores):
            high_scores_str += f"{i+1}. {row[0]} - {row[1]}\n"

        tk.messagebox.showinfo("High Scores", high_scores_str)

    def next_question(self):
        self.show_question()

    def start(self):
        self.window.mainloop()

# Create the QuizApp and start the game
app = QuizApp()
app.start()





