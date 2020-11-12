class Mode:
    def __init__(self, name):
        self.name = name
        self.images = []
        self.words_right = []
        self.words_wrong = []
    def random_word(self):
        pass
    def print_itself(self):
        print("Mode: "+ str(self.name))
        print(" -> Images: ", self.images)
        print(" -> Correct words: ", self.words_right)
        print(" -> Incorrect words: ", self.words_wrong)



