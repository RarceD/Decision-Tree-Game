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
        self.background = ""
        self.background_logo = ""
        self.enter_button = ""
        self.enter_button_text_color = ""
        self.circle_button_yes_no_button = ""
        self.circle_question_number = ""
        self.letters_color = ""
        self.border_colors = ""
        self.waiting_children_font_up = ""
        self.waiting_children_font_down = ""
        self.question_text_2 = ""
        self.color_circle_right = ""
        self.color_circle_wrong = ""
        self.radio_circle = 0
        self.font_primary = ""
        self.font_secondary = ""

        with open(input_file) as json_file:
            data = json.load(json_file)
            for index, p in enumerate(data['icon_child_sharable']):
                self.icon_child.append(p)
            self.game_name = data['global_images']["game_name"]
            self.game_logo = data['global_images']["game_logo"]

            self.background = data['color_config_children']['background']
            # self.background = tuple(
            #     map(int, str(self.background)[1:-1].split(',')))

            self.background_logo = data['color_config_children']['background_logo']
            self.background_logo = tuple(
                map(int, str(self.background_logo)[1:-1].split(',')))

            self.enter_button = data['color_config_children']['enter_button']
            self.enter_button = tuple(
                map(int, str(self.enter_button)[1:-1].split(',')))

            self.enter_button_text_color = data['color_config_children']['enter_button_text_color']
            self.enter_button_text_color = tuple(
                map(int, str(self.enter_button_text_color)[1:-1].split(',')))

            self.circle_button_yes_no_button = data['color_config_children']['circle_button_yes_no_button']
            self.circle_button_yes_no_button = tuple(
                map(int, str(self.circle_button_yes_no_button)[1:-1].split(',')))

            self.circle_question_number = data['color_config_children']['circle_question_number']
            self.circle_question_number = tuple(
                map(int, str(self.circle_question_number)[1:-1].split(',')))

            self.letters_color = data['color_config_children']['letters_color']
            self.letters_color = tuple(
                map(int, str(self.letters_color)[1:-1].split(',')))

            self.font_primary = data['color_config_children']['font_primary']
            self.font_secundary = data['color_config_children']['font_secundary']

            self.border_colors = data['color_config_children']['border_colors']
            self.border_colors = tuple(
                map(int, str(self.border_colors)[1:-1].split(',')))

            self.waiting_children_font_up = data['color_config_children']['waiting_children_font_up']
            self.waiting_children_font_down = data['color_config_children']['waiting_children_font_down']
            self.question_text_2 = data['color_config_children']['question_text_2']

            self.color_circle_wrong = data['color_config_children']['color_circle_wrong']
            self.color_circle_wrong = tuple(
                map(int, str(self.color_circle_wrong)[1:-1].split(',')))

            self.color_circle_right = data['color_config_children']['color_circle_right']
            self.color_circle_right = tuple(
                map(int, str(self.color_circle_right)[1:-1].split(',')))

            self.radio_circle = data['color_config_children']['radio_circle']

    def parse_data(self):
        pass
