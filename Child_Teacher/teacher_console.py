import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode

PUBLISH_TOPIC = 'TFG_B/teacher'
LISTEN_TOPIC = 'TFG_B/children'
childrens = []
progress = []

WINDOWS = {
    'WAITING_CHILDRENS': 0,
    'ON_GAME': 1,
    'FINISH': 3,
}
parser = {
    "game_name": "Nombre to guapo",
    "game_logo": "game_logo.png",
    "background": "",
    "mode_buttons": "",
    "children_background": "",
    "letters": "",
    "progress_bar": ""
}
current_window = 1111
run = True
modes = []


def read_config_file(modes, parser):
    with open('input.json') as json_file:
        data = json.load(json_file)
        for index, p in enumerate(data['modes']):
            modes.append(Mode())
            
            modes[index].words_wrong.append(p["correct_word"])
            modes[index].images.append(p["images"])
            parser['game_name'] = data['global_images']['game_name']
        parser['game_logo'] = data['global_images']['game_logo']
        parser['background'] = data['color_config_teacher']['background']
        parser['mode_buttons'] = data['color_config_teacher']['mode_buttons']
        parser['children_background'] = data['color_config_teacher']['children_background']
        parser['letters'] = data['color_config_teacher']['letters']
        parser['progress_bar'] = data['color_config_teacher']['progress_bar']
    for m in modes:
        m.print_itself()


def connect_mqtt():
    broker_address = "broker.mqttdashboard.com"
    client = mqtt.Client("asdf123bea34asdf")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    print("Subscribing to topic", LISTEN_TOPIC)
    client.subscribe(LISTEN_TOPIC)
    print("Publishing message to topic", "master_beacon_ack")
    msg = '''{"ok":true}'''
    client.publish("master_beacon/ack", msg)
    client.loop_start()  # start the loop
    return client


def on_message(client, userdata, message):
    global progress, childrens
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # Example json: {"esp":"A1","beacon":[ {"uuid":5245,"distance":1.23},{"uuid":52345, "distance":1.23 }]}
    msg = str(message.payload.decode("utf-8"))
    # print("message received: ", msg)
    parsed_json = (json.loads(msg))
    new_children = parsed_json['uuid']
    print(new_children)
    if (new_children in childrens):
        # Update the status of the questions
        for index, c in enumerate(childrens):
            if (c == new_children):
                progress[index] = parsed_json['question']
    else:
        if (len(childrens) > 24):
            childrens.append("dijimos 25 guapita ...")
        else:
            question = parsed_json['question']
            childrens.append(new_children)
            progress.append(question)

    print(childrens)
    print(progress)


def load_page_waitting_child(win, font, events, client):
    global run, current_window, childrens, progress, PUBLISH_TOPIC, modes

    win.fill((30, 30, 30))
    space_box = 200
    pygame.draw.rect(win, (255, 255, 255), (700, 100, 200, 100))
    txt_game_name = font.render("4 WORDS", True,  (0x00, 0x00, 0x00))
    win.blit(txt_game_name, (750, 140))

    pygame.draw.rect(win, (255, 255, 255), (700, 100 + space_box, 200, 100))
    txt_game_name = font.render("6 WORDS", True,  (0x00, 0x00, 0x00))
    win.blit(txt_game_name, (750, 140 + space_box))

    pygame.draw.rect(win, (255, 255, 255), (700, 100 + space_box*2, 200, 100))
    txt_game_name = font.render("8 WORDS", True,  (0x00, 0x00, 0x00))
    win.blit(txt_game_name, (750, 140 + space_box*2))

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the  rect.
            send_to_app = [False, 0, 0]
            if pygame.Rect(700, 100, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 4, 0]
                print("Mode 5")
            if pygame.Rect(700, 100 + space_box, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 6, 1]
                print("Mode 8")
            if pygame.Rect(700, 100 + space_box*2, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 8, 2]
                print("Mode 10")
            if send_to_app[0]:
                current_window = WINDOWS['ON_GAME']
                data = {
                    "start": True,
                    "mode": send_to_app[1],
                }
                data['words_right'] = modes[send_to_app[2]].words_right[0]
                data['words_wrong'] = modes[send_to_app[2]].words_wrong[0]
                data['images'] = modes[send_to_app[2]].images[0]

                json_dump = json.dumps(data)
                client.publish(PUBLISH_TOPIC, json_dump)

    pygame.draw.rect(win, (181, 255, 255), (100, 100, 500, 600))
    offset = 0
    spacing = 0
    for index, c in enumerate(childrens):
        a = font.render(c, True, (0x00, 0x00, 0x00))
        win.blit(a, (150+spacing, 150 + offset))
        offset += 40
        if (index == 12):
            offset = 0
            spacing = 250

    # txt_game_name = font.in("Enter", True, (0xFF,0xFF,0xFF))
    # win.blit(txt_game_name, (350, 220))


def load_page_game(win, font, events):
    global run, childrens, progress
    win.fill((30, 30, 30))

    # THe list of children
    pygame.draw.rect(win, (181, 255, 255), (100, 100, 700, 600))
    offset = 0
    spacing = 0
    for index, c in enumerate(childrens):
        a = font.render(c, True, (0x00, 0x00, 0x00))
        win.blit(a, (150+spacing, 150 + offset))
        r = 0
        while (r < int(progress[index])):
            pygame.draw.rect(win, (0, 0, 0), (320 + r * 20 +
                                              spacing, 150 + offset, 20, 30))
            pygame.draw.rect(win, (217, 0, 30), (320 + r *
                                                 20+2+spacing, 150+2 + offset, 20-4, 30-4))
            r += 1
        offset += 40
        if (index == 12):
            offset = 0
            spacing = 250
    offset = 0
    # for index, p in enumerate(progress):
    #     while (offset < p):
    #         pygame.draw.rect(win, (0, 0, 0), (320 + offset *20, 150, 20, 30))
    #         pygame.draw.rect(win, (217, 0, 30), (320 + offset *20+2, 150+2, 20-4, 30-4))
    #         offset += 1

    for event in events:
        if event.type == pygame.QUIT:
            run = False


def main():
    global current_window, run, childrens, progress, parser

    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    current_window = WINDOWS['WAITING_CHILDRENS']

    image = pygame.image.load('images/' + parser['game_logo'])
    image = pygame.transform.scale(image, (50, 50))

    while run:
        if current_window == WINDOWS['WAITING_CHILDRENS']:
            load_page_waitting_child(win, font, pygame.event.get(), client)
        elif current_window == WINDOWS['ON_GAME']:
            load_page_game(win, font, pygame.event.get())
        elif current_window == WINDOWS['FINISH']:
            load_page_game(win, font)
        # i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
        #     i += 100
        pygame.display.flip()
        clock.tick(100)


if __name__ == '__main__':
    pygame.init()
    client = connect_mqtt()
    read_config_file(modes, parser)
    main()
    pygame.quit()
