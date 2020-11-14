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


class LoadFile():
    def __init__(self, input_file):
        self.icon_child = []
        self.game_name = ""
        self.game_logo = ""
        self.background_color = ""
        self.enter_button = ""
        self.circle_button_yes_no_button = ""
        self.circle_question_number = ""
        self.letters = ""
        with open(input_file) as json_file:
            data = json.load(json_file)
            for index, p in enumerate(data['icon_child_sharable']):
                self.icon_child.append(p)
            self.game_name = data['global_images']["game_name"]
            self.game_logo = data['global_images']["game_logo"]

            self.background_color = data['color_config_children']['background']
            self.enter_button = data['color_config_children']['enter_button']
            self.circle_button_yes_no_button = data['color_config_children']['circle_button_yes_no_button']
            self.circle_question_number = data['color_config_children']['circle_question_number']
            self.letters = data['color_config_children']['letters']
            self.font_primary = data['color_config_children']['font_primary']
            self.font_secundary = data['color_config_children']['font_secundary']

        print(self.icon_child)
        print(self.game_name)
        print(self.background_color)
        print(self.background_color)
        print(self.enter_button)
        print(self.circle_button_yes_no_button)
        print(self.circle_question_number)
        print(self.letters)

    def parse_data(self):
        pass
