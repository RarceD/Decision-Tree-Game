import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode, Children, BadChildren
from LoadFile import LoadFile
import time
import random


PUBLISH_TOPIC = 'TFG_B/children'
LISTEN_TOPIC = 'TFG_B/teacher'
WINDOWS = {
    'LOGIN': 0,
    'WAITING_TEACHER': 1,
    'ON_GAME': 2,
    'FINISH': 3,
    'BAD_STUDENT': 4,
    'RANKING':5
}
current_window = 1111

def connect_mqtt():
    broker_address = "broker.mqttdashboard.com"
    # client = mqtt.Client("asdadf31wsd4asdffwefw")  # create new instance
    client = mqtt.Client("a"+str(random.randint(121233, 35123234)) + "f")
    client.on_message = on_message  # attach function to callback
    # print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    # print("Subscribing to topic", LISTEN_TOPIC)
    client.subscribe(LISTEN_TOPIC)
    # print("Publishing message to topic", "master_beacon_ack")
    msg = '''{"ok":true}'''
    client.publish(PUBLISH_TOPIC, msg)
    client.loop_start()  # start the loop
    return client


def on_message(client, userdata, message):
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # Example json: {"esp":"A1","beacon":[ {"uuid":5245,"distance":1.23},{"uuid":52345, "distance":1.23 }]}
    global current_window, WINDOWS, mode, modes
    msg = str(message.payload.decode("utf-8"))
    # print("message received: ", msg)
    parsed_json = json.loads(msg)
    # I received the questions and save them:
    # print(parsed_json)
    if (parsed_json['start']):
        current_window = WINDOWS['ON_GAME']
        max_question_number = parsed_json['mode']
        print(max_question_number)
        if (max_question_number == 4):
            mode = modes[0]
        elif (max_question_number == 6):
            mode = modes[1]
        else:
            mode = modes[2]
    # print("The selected mode is:" )
    # mode.print_itself()
    # I untidy the words in order to not repeat between childs:
    ran_int_seed = random.randint(0, 25)
    random.seed(ran_int_seed)
    random.shuffle(mode.words_right)
    random.seed(ran_int_seed)
    random.shuffle(mode.words_wrong)
    random.seed(ran_int_seed)
    random.shuffle(mode.images)
    # mode.print_itself()


def load_page_login(win, image, font, events, client):
    global current_window, WINDOWS, children, parser
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(450, 600, 140, 50)
    game_name = pygame.Rect(200, 100, 600, 300)

    win.blit(parser.background_login, (0, 0))
    # Render the current text.
    txt_surface = font.render(
        children.name, True, parser.enter_button_text_color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    win.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(win, parser.enter_button_text_color, input_box, 5)
    pygame.draw.rect(win, parser.enter_button, input_enter)

    pygame.draw.rect(win, parser.background_logo, game_name)
    txt_game_name = font.render(parser.game_name, True, parser.letters_color)
    win.blit(txt_game_name, (350, 220))
    txt_game_name = font.render("Enter", True, (0xFF, 0xFF, 0xFF))
    win.blit(txt_game_name, (460, 610))
    win.blit(image, (280, 500))
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_enter.collidepoint(event.pos):
                if (len(children.name) != 0):
                    current_window = WINDOWS['WAITING_TEACHER']
                    msg = "{\"uuid\":\""+children.name+"\",\"question\":0}"
                    client.publish(PUBLISH_TOPIC, msg)
                    print("Enter Press")
        if event.type == pygame.KEYDOWN:
            if True:
                if event.key == pygame.K_RETURN:
                    print(children.name)
                    children.name = ''
                elif event.key == pygame.K_BACKSPACE:
                    children.name = children.name[:-1]
                else:
                    children.name += event.unicode


def load_page_waiting(win, font, image, events):
    global children

    win.blit(parser.background_waiting, (0, 0))
    # Render the current text.
    pygame.draw.rect(win, parser.background_logo, (150, 200, 700, 200), 2)
    color_letters = parser.letters_color
    txt_surface = font.render(
        parser.waiting_children_font_up, True, color_letters)
    win.blit(txt_surface, (200, 233))
    txt_surface = font.render(
        parser.waiting_children_font_down, True, color_letters)
    win.blit(txt_surface, (200, 333))
    txt_surface = font.render(str(children.name), True, color_letters)
    win.blit(txt_surface, (400, 500))
    win.blit(image, (340, 490))
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False


def load_page_game(win, font, image_children,  image_game_logo, events, client):
    global children, mode, current_window, parser, bad_children
    win.blit(parser.background_game, (0, 0))
    win.blit(image_game_logo, (870, 30))
    # Render the current text.
    pygame.draw.rect(win, parser.border_colors, (200, 50, 600, 150), 2)
    pygame.draw.rect(win, parser.border_colors, (170, 300, 330, 100), 2)
    pygame.draw.rect(win, parser.border_colors, (550, 300, 250, 220), 2)
    color_letters = parser.letters_color
    txt_surface = font.render(
        parser.question_text_2, True, color_letters)
    win.blit(txt_surface, (250, 120))
    txt_surface = font.render(
        mode.words_right[children.current_question-1], True, color_letters)
    # Each word has a diferent image:
    win.blit(txt_surface, (220, 330))
    word_image = pygame.image.load(
        'images/' + mode.images[children.current_question-1])
    word_image = pygame.transform.scale(word_image, (170, 170))
    win.blit(word_image, (580, 320))

    color_circle = parser.circle_button_yes_no_button
    radio_circle = parser.radio_circle
    circle_yes = pygame.draw.circle(
        win, color_circle, (100, 300), radio_circle)
    circle_question = pygame.draw.circle(
        win, parser.circle_question_number, (500, 600), radio_circle)
    circle_no = pygame.draw.circle(win, color_circle, (900, 300), radio_circle)

    color_text = parser.letters_color
    offset = 17
    txt_surface = font.render("SI", True, color_text)
    win.blit(txt_surface, (100-offset, 300-offset))
    txt_surface = font.render("NO", True, color_text)
    win.blit(txt_surface, (900-offset, 300-offset))
    txt_surface = font.render(str(children.current_question), True, color_text)
    win.blit(txt_surface, (500-offset, 600-offset))

    # Child name and picture:
    txt_surface = font.render(children.name, True, color_letters)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = 0  # I get the child response
            children_solution_ok = False  # The real child response to compare
            response = False
            if circle_yes.collidepoint(event.pos):
                response = True
                action = 1
            if circle_no.collidepoint(event.pos):
                response = False
                action = 2
            if action > 0:
                # Check if is ok or not
                puntuation = 10
                # Calculate the punctiation: given current time to response and an unknown protocol
                if (mode.words_wrong[children.current_question-1] == response):
                    puntuation = children.calculate_punctuation(
                        children.timer_running)
                    pygame.mixer.music.load('audio/si.wav')
                    pygame.mixer.music.play(0)
                    print("the response is ok")
                else:
                    puntuation = 0
                    print("the response is NOT OK")
                    pygame.mixer.music.load('audio/no.wav')
                    pygame.mixer.music.play(0)
                    # I save to previously repeat this little asshole the question:
                    bad_children.questions.append(
                        mode.words_right[children.current_question-1])
                    bad_children.answers.append(
                        mode.words_wrong[children.current_question-1])
                    bad_children.images.append(
                        mode.images[children.current_question-1])
                    bad_children.print_itself()

                # I restart the timer for the next question:
                children.timer_running = 0
                # Publish the results:
                msg = {
                    "uuid": children.name,
                    "question": str(children.current_question),
                    "punctuation": str(puntuation)
                }
                json_dump = json.dumps(msg)
                client.publish(PUBLISH_TOPIC, json_dump)

                # Do I have to finish the game?:
                if (children.current_question < mode.name):
                    children.current_question += 1
                    print("increase the current question")

                else:
                    print("I finish the game")
                    # Finish if the children have end successfully
                    current_window = WINDOWS['FINISH']


def load_page_end(win, events, font, image_children, image_game_logo, image_tree):
    global children, mode, bad_children, WINDOWS, current_window
    win.blit(parser.background_end, (0, 0))
    input_enter = pygame.Rect(750, 600, 140, 50)
    # Add the name of the children
    txt_surface = font.render(children.name, True,  parser.letters_color)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    win.blit(image_game_logo, (870, 30))
    win.blit(image_tree, (150, 100))
    pygame.draw.rect(win, parser.enter_button, input_enter)

    txt_game_name = font.render("Enter", True, (0xFF, 0xFF, 0xFF))
    win.blit(txt_game_name, (780, 590))

    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_enter.collidepoint(event.pos):
                print('move to final or repeat')
                if len(bad_children.questions) > 0:
                    current_window = WINDOWS['BAD_STUDENT']
                else:
                    current_window = WINDOWS['RANKING']

    #Print the branch:
    txt_game_name = font.render("Camino elegido:", True, (0x00, 0x00, 0x00))
    win.blit(txt_game_name, (740, 310))
    win.blit(image_children, (860, 410))
    #Print the balls:
    color_circle_wrong = parser.color_circle_wrong
    color_circle_right = parser.color_circle_right
    radio_circle = 20
    # Draw the tree
    offset = 0
    color = color_circle_wrong

    max_number_balls = int(mode.name)
    failed_words = len(bad_children.questions)

    
    if (failed_words > 0):
        color = color_circle_wrong
        failed_words -= 1
    else:
        color = color_circle_right
    x_space = 80
    if (max_number_balls >= 4):
        for i in range(0, 4):
            if i<3:
                circle_yes = pygame.draw.circle(
                    win, color, (350 + x_space*i, 200), radio_circle)
                if (failed_words > 0):
                    color = color_circle_wrong
                    failed_words-=1
                else:
                    color = color_circle_right
            else:                
                circle_yes = pygame.draw.circle(
                    win, color, (350 + x_space , 350), radio_circle)
                if (failed_words > 0):
                    color = color_circle_wrong
                    failed_words-=1
                else:
                    color = color_circle_right


    if (max_number_balls >= 6):
        for i in range(0, 2):
            circle_yes = pygame.draw.circle(
                win, color, (400 + x_space*i, 275), radio_circle)
            if (failed_words > 0):
                color = color_circle_wrong
                failed_words-=1
            else:
                color = color_circle_right
    if (max_number_balls == 8):
        for i in range(0, 2):
            circle_yes = pygame.draw.circle(
                win, color, (350 + x_space*2*i, 350), radio_circle)
            if (failed_words > 0):
                color = color_circle_wrong
                failed_words-=1
            else:
                color = color_circle_right


def load_page_bad_student(win, events, font, image_children, image_game_logo, image_tree):
    global children, mode, current_window, parser, bad_children
    win.fill((4, 4, 4))
    win.blit(parser.background_bad_student, (0, 0))

    win.blit(image_game_logo, (870, 30))
    # Render the current text.
    pygame.draw.rect(win, parser.border_colors, (200, 50, 600, 150), 2)
    pygame.draw.rect(win, parser.border_colors, (170, 300, 330, 100), 2)
    pygame.draw.rect(win, parser.border_colors, (550, 300, 250, 220), 2)
    color_letters = parser.letters_color
    txt_surface = font.render(
        parser.question_text_2, True, color_letters)
    win.blit(txt_surface, (250, 120))
    txt_surface = font.render(
        bad_children.questions[bad_children.index], True, color_letters)
    # Each word has a diferent image:
    win.blit(txt_surface, (220, 330))
    word_image = pygame.image.load(
        'images/' + bad_children.images[bad_children.index])
    word_image = pygame.transform.scale(word_image, (170, 170))
    win.blit(word_image, (580, 320))

    color_circle = parser.circle_button_yes_no_button
    radio_circle = parser.radio_circle
    circle_yes = pygame.draw.circle(
        win, color_circle, (100, 300), radio_circle)
    circle_question = pygame.draw.circle(
        win, parser.circle_question_number, (500, 600), radio_circle)
    circle_no = pygame.draw.circle(win, color_circle, (900, 300), radio_circle)

    color_text = parser.letters_color
    offset = 17
    txt_surface = font.render("SI", True, color_text)
    win.blit(txt_surface, (100-offset, 300-offset))
    txt_surface = font.render("NO", True, color_text)
    win.blit(txt_surface, (900-offset, 300-offset))
    txt_surface = font.render(str(bad_children.index + 1), True, color_text)
    win.blit(txt_surface, (500-offset, 600-offset))

    # Child name and picture:
    txt_surface = font.render(children.name, True, color_letters)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = 0  # I get the child response
            children_solution_ok = False  # The real child response to compare
            response = False
            if circle_yes.collidepoint(event.pos):
                response = True
                action = 1
            if circle_no.collidepoint(event.pos):
                response = False
                action = 2
            if action > 0:
                # Remove the bad_children and continue the game:
                if (bad_children.answers[bad_children.index]== response):
                    bad_children.answers.pop(bad_children.index)
                    bad_children.questions.pop(bad_children.index)
                    bad_children.images.pop(bad_children.index)
                    if (bad_children.index!=0):
                        bad_children.index-=1
                else:
                    if (len(bad_children.answers) > bad_children.index + 1):
                        bad_children.index += 1
                    else:
                        current_window = WINDOWS['FINISH']

                # Do I have to finish the game?:
                if (len(bad_children.answers) == 0):
                    print("I finish the game")
                    current_window = WINDOWS['FINISH']
                else:
                    print("increase the current question")


def load_page_ranking(win, events, font, image_children, image_game_logo, image_tree):
    global children, mode, bad_children, WINDOWS, current_window
    win.blit(parser.background_ranking, (0, 0))
    input_enter = pygame.Rect(750, 600, 140, 50)
    # Add the name of the children
    txt_surface = font.render(children.name, True,  parser.letters_color)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    win.blit(image_game_logo, (870, 30))
  
    pygame.draw.rect(win, parser.enter_button, input_enter)

    txt_game_name = font.render("Enter", True, (0xFF, 0xFF, 0xFF))
    win.blit(txt_game_name, (780, 590))
    txt_game_name = font.render("RANKING ALUMNOS:", True, parser.letters_color)
    win.blit(txt_game_name, (310, 110))
    names = ['Bea', 'Ruben', 'Luís', 'Francisco ', 'Paquito']
    offset = 0
    for i in range(0, 5):
        txt_game_name = font.render(names[i], True, parser.letters_color)
        win.blit(txt_game_name, (360, 225 + offset))
        offset += 50
    

    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_enter.collidepoint(event.pos):
                if len(bad_children.questions) > 0:
                    current_window = WINDOWS['BAD_STUDENT']
                else:
                    current_window = WINDOWS['RANKING']

def main():
    global current_window, children, mode
    clock = pygame.time.Clock()
    # Start the game on LOGIN:
    win = pygame.display.set_mode((1024, 768))
    current_window = WINDOWS['LOGIN']
    # The game icon of the children:
    image = pygame.image.load(
        'icon/' + str(parser.icon_child[random.randint(0, len(parser.icon_child)-1)]))
    image = pygame.transform.scale(image, (50, 50))
    # The tree final image:
    image_tree = pygame.image.load('images/' + 'tree.png')
    image_tree = pygame.transform.scale(image_tree, (600, 600))
    # Parse all the images and fonts:
    parser.parse_data(pygame)
    # Periodic task made with this timer:
    timer_update_screen = int(round(time.time()))
    while children.run:
        # Game state machine:
        if (current_window == WINDOWS['LOGIN']):
            load_page_login(win,  image, parser.font_primary, pygame.event.get(), client)
        elif (current_window == WINDOWS['WAITING_TEACHER']):
            load_page_waiting(win, parser.font_primary, image, pygame.event.get())
        elif (current_window == WINDOWS['ON_GAME']):
            load_page_game(win, parser.font_secundary, image,
                           parser.game_logo, pygame.event.get(), client)
        elif (current_window == WINDOWS['FINISH']):
            load_page_end(win, pygame.event.get(),
                          parser.font_primary, image, parser.game_logo, image_tree)
        elif (current_window == WINDOWS['BAD_STUDENT']):
            load_page_bad_student(win, pygame.event.get(),
                                  parser.font_primary, image, parser.game_logo, image_tree)
        elif (current_window == WINDOWS['RANKING']):
            load_page_ranking(win, pygame.event.get(),
                                  parser.font_primary, image, parser.game_logo, image_tree)
        # i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
        #     i += 100

        # I count the time on game for calculate children points
        if (current_window == WINDOWS['ON_GAME'] and int(round(time.time())) - timer_update_screen >= children.refresh_time):
            timer_update_screen = int(round(time.time()))
            children.timer_running += 1
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    # I create the mode that hold the max questions number and the solutions/images
    # received from the teacher
    mode = Mode()
    # The current status of the children, time, question, etc..
    children = Children()
    parser = LoadFile('input.json')
    bad_children = BadChildren()
    modes = []
    with open('input.json') as json_file:
        data = json.load(json_file)
        for i in range(0, 3):
            modes.append(Mode())
            modes[i].name = data['modes'][i]["name"]
            for w in data['modes'][i]["words"]:
                modes[i].words_right.append(w)
            for w in data['modes'][i]["correct_word"]:
                modes[i].words_wrong.append(w)
            for w in data['modes'][i]["images"]:
                modes[i].images.append(w)

    pygame.init()
    client = connect_mqtt()
    main()
    pygame.quit()
