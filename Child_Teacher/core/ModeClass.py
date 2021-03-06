import json


class Mode:
    def __init__(self):
        self.name = ""
        self.images = []
        self.words_right = []
        self.words_wrong = []

    def random_word(self):
        pass

    def print_itself(self):
        print("Mode: " + str(self.name))
        print(" -> Images: ", self.images)
        print(" -> Correct words: ", self.words_right)
        print(" -> Incorrect words: ", self.words_wrong)

class BadChildren:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.images = []
        self.index = 0

    def print_itself(self):
        print(" -> Incorrect to repeat: ", self.questions)
        print("Answers: ", self.answers)
        print("Images: ", self.images)


class Children:
    def __init__(self):
        self.name = "Paco"
        self.current_question = 1
        self.run = True
        self.timer_running = 0
        self.total_punctuation = 0
        self.refresh_time = 1

    def print_itself(self):
        print(self.name, self.current_question, self.run)

    def calculate_punctuation(self, time):
        # Start with 10 points and every 5 seconds it start to decrese -1
        punctuation = 10
        if time > 25:
            self.total_punctuation += 5
            return 5
        while (time - 5 > 0):
            punctuation -= 1
            time -= 5
        self.total_punctuation += punctuation
        return punctuation


class ChildrenEvaluation:
    def __init__(self, name, words):
        self.words = words
        self.name = name
        self.fails = []
        self.final_time = 0
        self.final_punctuation = 0
        self.progress_bar_colors = []

    def print_itself(self):
        print('++> ', self.name)
        print('  words:', self.words)
        print('  fails: ', self.fails)
        print('  final_time: ', self.final_time)
        print('  final_punctuation: ', self.final_punctuation)
