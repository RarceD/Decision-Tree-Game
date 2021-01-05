import json

class LoadFile():
    def __init__(self, input_file):
        self.icon_child = []
        self.game_name = ""
        self.game_logo = ""
        self.background_login = ""
        self.background_waiting = ""
        self.background_game = ""
        self.background_end = ""
        self.background_ranking = ""
        self.background_logo = ""
        self.background_bad_student = ""
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


            self.background_login = data['color_config_children'][ 'background_login']
            self.background_waiting = data['color_config_children'][ 'background_waiting']
            self.background_game = data['color_config_children'][ 'background_game']
            self.background_end = data['color_config_children'][ 'background_end']
            self.background_bad_student = data['color_config_children']['background_bad_student']
            self.background_ranking = data['color_config_children']['background_ranking']
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

    def parse_data(self, pygame):
        dimensions = (1024, 768)
        self.background_login = pygame.image.load(
            'images/' + self.background_login)
        self.background_login = pygame.transform.scale(
            self.background_login, dimensions)
        self.background_waiting = pygame.image.load(
            'images/' + self.background_waiting)
        self.background_waiting = pygame.transform.scale(
            self.background_waiting, dimensions)
        self.background_game = pygame.image.load(
            'images/' + self.background_game)
        self.background_game = pygame.transform.scale(
            self.background_game, dimensions)
        self.background_end = pygame.image.load(
            'images/' + self.background_end)
        self.background_end = pygame.transform.scale(
            self.background_end, dimensions)
        self.background_bad_student = pygame.image.load(
            'images/' + self.background_bad_student)
        self.background_bad_student = pygame.transform.scale(
            self.background_bad_student, dimensions)
        self.background_ranking = pygame.image.load(
            'images/' + self.background_ranking)
        self.background_ranking = pygame.transform.scale(
            self.background_ranking, dimensions)
        self.font_primary = pygame.font.Font(self.font_primary, 52)
        self.font_secundary = pygame.font.Font(self.font_secundary, 52)
        # The global game logo:
        self.game_logo  = pygame.image.load('images/' + self.game_logo)
        self.game_logo = pygame.transform.scale(self.game_logo, (100, 100))
