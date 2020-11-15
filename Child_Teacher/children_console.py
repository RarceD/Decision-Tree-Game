import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode, Children, LoadFile
import time
import random


PUBLISH_TOPIC = 'TFG_B/children'
LISTEN_TOPIC = 'TFG_B/teacher'
WINDOWS = {
    'LOGIN': 0,
    'WAITING_TEACHER': 1,
    'ON_GAME': 2,
    'FINISH': 3,
}
current_window = 1111

# I create the mode that hold the max questions number and the solutions/images
# received from the teacher
mode = Mode()
# The current status of the children, time, question, etc..
children = Children()
children.print_itself()
parser = LoadFile('input.json')
modes=[]
 
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

    for m in modes:
        m.print_itself()

        

def connect_mqtt():
    broker_address = "broker.mqttdashboard.com"
    client = mqtt.Client("asdadf324wsd4asdf")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    print("Subscribing to topic", LISTEN_TOPIC)
    client.subscribe(LISTEN_TOPIC)
    print("Publishing message to topic", "master_beacon_ack")
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
    print (parsed_json)
    if (parsed_json['start']):
        current_window = WINDOWS['ON_GAME']
        max_question_number = parsed_json['mode']
        print (max_question_number)
        if (max_question_number == 4):
            mode = modes[0]
        elif (max_question_number ==  6):
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
    # mode.print_itself()

    
def load_page_login(win, image, font, events, client):
    global current_window, WINDOWS, children
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(450, 600, 140, 50)
    game_name = pygame.Rect(200, 100, 600, 300)

    win.fill((30, 30, 30))
    # Render the current text.
    txt_surface = font.render(children.name, True, (123,123,3))
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    win.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(win, (2,234,34), input_box, 2)
    pygame.draw.rect(win, (123, 0, 0), input_enter)

    pygame.draw.rect(win, (255, 255, 255), game_name)
    txt_game_name = font.render("Nombre to guapo", True, (0, 0, 0))
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

    win.fill((30, 30, 30))
    # Render the current text.
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (150, 200, 700, 200), 2)
    color_letters = (163, 227, 255)
    txt_surface = font.render(
        "Espera un momento a que todos", True, color_letters)
    win.blit(txt_surface, (200, 233))
    txt_surface = font.render(
        "tus compañeros entren al juego", True, color_letters)
    win.blit(txt_surface, (200, 333))
    txt_surface = font.render(str(children.name), True, color_letters)
    win.blit(txt_surface, (400, 500))
    win.blit(image, (340, 490))
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False


def load_page_game(win, font, image_children,  image_game_logo, events, client, word_image):
    global children, mode, current_window
    win.fill((30, 30, 30))
    win.blit(image_game_logo, (870, 30))
    # Render the current text.
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (200, 50, 600, 150), 2)
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (250, 300, 250, 100), 2)
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (550, 300, 200, 150), 2)

    color_letters = (163, 227, 255)
    txt_surface = font.render(
        "¿ Son correctas las palabras ?", True, color_letters)
    win.blit(txt_surface, (250, 120))
    txt_surface = font.render(
        mode.words_right[children.current_question-1], True, color_letters)
    # Each word has a diferent image:
    win.blit(txt_surface, (320, 330))
    win.blit(word_image, (600, 320))

    color_circle = (87, 154, 230)
    radio_cicle = 80
    circle_yes = pygame.draw.circle(win, color_circle, (100, 300), radio_cicle)
    circle_question = pygame.draw.circle(
        win, color_circle, (500, 600), radio_cicle)
    circle_no = pygame.draw.circle(win, color_circle, (900, 300), radio_cicle)

    color_text = (0, 0, 0)
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
                    print("the response is ok")
                else:
                    puntuation = 0
                    print("the response is NOT OK")

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

                # Do I have to finish the game:
                if (children.current_question < mode.name):
                    children.current_question += 1
                else:
                    # Finish if the children have end successfully
                    all_right = True
                    if (all_right):
                        current_window = WINDOWS['FINISH']
                    # If not I return the children to the first fail
                    else:
                        pass


def load_page_end(win, events, font, image_children, image_game_logo):
    global children, mode
    for event in events:
        if event.type == pygame.QUIT:
            children.run = False
    # Add the name of the children
    txt_surface = font.render(children.name, True,  (163, 227, 255))
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    win.blit(image_game_logo, (870, 30))

    # Draw the tree
    if (mode.name == 4):
        pass
    elif (mode.name == 6):
        pass
    elif (mode.name == 8):
        pass


def main():
    global current_window, children, mode

    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 52)
    clock = pygame.time.Clock()
    # Start the game on LOGIN:
    current_window = WINDOWS['LOGIN']
    # The game icon of the children:
    image = pygame.image.load('icon/' + str(parser.icon_child[random.randint(0, len(parser.icon_child)-1)]))
    image = pygame.transform.scale(image, (50, 50))
    # The global game logo
    image_game_logo = pygame.image.load('images/' +parser.game_logo)
    image_game_logo = pygame.transform.scale(image_game_logo, (100, 100))

    timer_update_screen = int(round(time.time()))
    

    while children.run:
        # Game state machine:
        if (current_window == WINDOWS['LOGIN']):
            load_page_login(win,  image, font,pygame.event.get(), client)
        elif (current_window == WINDOWS['WAITING_TEACHER']):
            if (len(children.name) == 0):
                children.name = "Laura Lomez"
            load_page_waiting(win, font, image, pygame.event.get())
        elif (current_window == WINDOWS['ON_GAME']):
            if (len(children.name) == 0):
                children.name = "Laura Lomez"
            image_word = pygame.image.load('images/' +mode.images[children.current_question-1])
            image_word = pygame.transform.scale(image_word, (100, 100))
            load_page_game(win, font, image,
                           image_game_logo, pygame.event.get(), client, image_word)
        elif (current_window == WINDOWS['FINISH']):
            if (len(children.name) == 0):
                children.name = "Laura Lomez"
            load_page_end(win, pygame.event.get(), font, image, image_game_logo)
        i = 0
        while i < 1024:
            pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
            pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
            i += 100
        if (current_window == WINDOWS['ON_GAME'] and int(round(time.time())) - timer_update_screen >= children.refresh_time):
            timer_update_screen = int(round(time.time()))
            children.timer_running += 1
            print(children.timer_running)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    client = connect_mqtt()
    main()
    pygame.quit()
