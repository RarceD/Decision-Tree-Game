import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode
import time

WINDOWS = {
    'LOGIN': 0,
    'WAITING_TEACHER': 1,
    'ON_GAME': 2,
    'FINISH': 3,
}
current_window = 1111
PUBLISH_TOPIC = 'TFG_B/children'
LISTEN_TOPIC = 'TFG_B/teacher'
mode = Mode("unknown")
run = True
child_name = ""
current_question = 1
timer_running = 0


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
    global current_window, WINDOWS, mode
    msg = str(message.payload.decode("utf-8"))
    print("message received: ", msg)
    parsed_json = json.loads(msg)
    # I received the questions and save them:
    if (parsed_json['start']):
        current_window = WINDOWS['ON_GAME']
        m = Mode("")
        m.name = parsed_json['mode']
        m.images = parsed_json['images']
        m.words_right = parsed_json['words_right']
        m.words_wrong = parsed_json['words_wrong']
        mode = m
    mode.print_itself()


def load_page_login(win, image, font, input_box, color, game_name, input_enter, events, client, color_active, color_inactive, active):
    global current_window, WINDOWS, run, child_name
    win.fill((30, 30, 30))
    # Render the current text.
    txt_surface = font.render(child_name, True, color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    win.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(win, color, input_box, 2)
    pygame.draw.rect(win, (123, 0, 0), input_enter)

    pygame.draw.rect(win, (255, 255, 255), game_name)
    txt_game_name = font.render("Nombre to guapo", True, (0, 0, 0))
    win.blit(txt_game_name, (350, 220))
    txt_game_name = font.render("Enter", True, (0xFF, 0xFF, 0xFF))
    win.blit(txt_game_name, (460, 610))
    win.blit(image, (280, 500))
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse button down")
            # If the user clicked on the input_box rect.

            # else:
            #     active = False
            # color = color_active if not active else color_inactive
            if input_enter.collidepoint(event.pos):
                if (len(child_name) != 0):
                    current_window = WINDOWS['WAITING_TEACHER']
                    msg = "{\"uuid\":\""+child_name+"\",\"question\":0}"
                    client.publish(PUBLISH_TOPIC, msg)
                    print("Enter Press")
            # Change the current color of the input box.
        if event.type == pygame.KEYDOWN:
            if True:
                if event.key == pygame.K_RETURN:
                    print(child_name)
                    child_name = ''
                elif event.key == pygame.K_BACKSPACE:
                    child_name = child_name[:-1]
                else:
                    child_name += event.unicode


def load_page_waiting(win, font, image, events):
    global run, child_name

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
    txt_surface = font.render(str(child_name), True, color_letters)
    win.blit(txt_surface, (400, 500))
    win.blit(image, (340, 490))
    for event in events:
        if event.type == pygame.QUIT:
            run = False


def load_page_game(win, font, image_children,  image_game_logo, events, client):
    global run, child_name, current_question, mode, timer_running, current_window
    win.fill((30, 30, 30))
    win.blit(image_game_logo, (870, 30))
    # Render the current text.
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (200, 50, 600, 150), 2)
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (300, 300, 400, 100), 2)

    color_letters = (163, 227, 255)
    txt_surface = font.render("Palabra / Frase / Audio", True, color_letters)
    win.blit(txt_surface, (300, 120))
    txt_surface = font.render(
        mode.words_right[current_question-1], True, color_letters)
    win.blit(txt_surface, (400, 333))

    color_circle = (87, 154, 230)
    radio_cicle = 50
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
    txt_surface = font.render(str(current_question), True, color_text)
    win.blit(txt_surface, (500-offset, 600-offset))

    # Child name and picture:
    txt_surface = font.render(child_name, True, color_letters)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))
    for event in events:
        if event.type == pygame.QUIT:
            run = False
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
                if (mode.words_wrong[current_question-1] == response):
                    puntuation = calculate_punctuation(timer_running)
                    print("the response is ok")
                else:
                    puntuation = 0
                    print("the response is NOT OK")

                # I restart the timer for the next question:
                timer_running = 0
                # Publish the results:
                msg = {
                    "uuid": child_name,
                    "question": str(current_question),
                    "punctuation":str(puntuation)
                }
                json_dump = json.dumps(msg)
                client.publish(PUBLISH_TOPIC, json_dump)

                # Do I have to finish the game:
                if (current_question < mode.name):
                    current_question += 1
                else:
                    # Finish if the children have end successfully
                    all_right = True
                    if (all_right):
                        current_window = WINDOWS['FINISH']
                    # If not I return the children to the first fail
                    else:
                        pass


def load_page_end(win, events, font, image_children):
    global child_name, run
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    txt_surface = font.render(child_name, True,  (163, 227, 255))
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))


def calculate_punctuation(time):
    # Start with 10 points and every 5 seconds it start to decrese -1
    punctuation = 10
    if time > 25:
        return 5
    while (time - 5 > 0):
        punctuation -= 1
        time-=5
    return punctuation


def main():
    global current_window, run, child_name, mode, timer_running
    client = connect_mqtt()
    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 52)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(450, 600, 140, 50)
    game_name = pygame.Rect(200, 100, 600, 300)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    child_name = ''
    current_window = WINDOWS['FINISH']
    image = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\duck_icon.jpg')
    image = pygame.transform.scale(image, (50, 50))
    image_game_logo = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\game_logo.png')
    image_game_logo = pygame.transform.scale(image_game_logo, (100, 100))
    timer_update_screen = int(round(time.time()))
    refresh_time = 1
    color_letters = (163, 227, 255)

    while run:
        # Game state machine:
        if (current_window == WINDOWS['LOGIN']):
            load_page_login(win,  image, font,  input_box, color,
                            game_name, input_enter, pygame.event.get(), client, color_active, color_inactive, active)
        elif (current_window == WINDOWS['WAITING_TEACHER']):
            if (len(child_name) == 0):
                child_name = "Laura Lomez"
            load_page_waiting(win, font, image, pygame.event.get())
        elif (current_window == WINDOWS['ON_GAME']):
            if (len(child_name) == 0):
                child_name = "Laura Lomez"
            load_page_game(win, font, image,
                           image_game_logo, pygame.event.get(), client)
        elif (current_window == WINDOWS['FINISH']):
            if (len(child_name) == 0):
                child_name = "Laura Lomez"
            load_page_end(win,pygame.event.get() , font, image)
        # i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0),(i,1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i),(1024,i), 1)
        #     i += 100
        if (current_window == WINDOWS['ON_GAME'] and int(round(time.time())) - timer_update_screen >= refresh_time):
            timer_update_screen = int(round(time.time()))
            timer_running += 1
            print(timer_running)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
