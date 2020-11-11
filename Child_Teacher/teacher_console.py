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
current_window = 1111
run = True
modes = []


def read_config_file(modes):
    with open('input.json') as json_file:
        data = json.load(json_file)
        for index, p in enumerate(data['modes']):
            modes.append(Mode(p['name']))
            modes[index].words_right.append(p["words_right"])
            modes[index].words_wrong.append(p["words_wrong"])
            modes[index].images.append(p["images"])

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

    #     # print(parsed_json['esp'])
    #     # Get the distance and the uuid of the beacon:
    #     beacon_distance = float(parsed_json['beacon'][index]['distance'])
    #     beacon_uuid = str(parsed_json['beacon'][index]['uuid'])


def load_page_waitting_child(win, font, child_name, input_box, color, game_name, input_enter, events, client, active, color_active, color_inactive):
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
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(child_name)
                    child_name = ''
                elif event.key == pygame.K_BACKSPACE:
                    child_name = child_name[:-1]
                else:
                    child_name += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change the current color of the input box.
            color = color_active if active else color_inactive
            # If the user clicked on the input_box rect.
            if pygame.Rect(700, 100, 200, 100).collidepoint(event.pos):
                current_window = WINDOWS['ON_GAME']
                data = {
                    "start": True,
                    "mode": 4,
                }
                data['words_right'] = modes[0].words_right[0]
                data['words_wrong'] = modes[0].words_wrong[0]

                json_dump = json.dumps(data)
                client.publish(PUBLISH_TOPIC, json_dump)
                print("Mode 5")
            if pygame.Rect(700, 100 + space_box, 200, 100).collidepoint(event.pos):
                current_window = WINDOWS['ON_GAME']
                data = {
                    "start": True,
                    "mode": 6,
                }
                data['words_right'] = modes[1].words_right[0]
                data['words_wrong'] = modes[1].words_wrong[0]
                json_dump = json.dumps(data)
                client.publish(PUBLISH_TOPIC, json_dump)
                print("Mode 8")
            if pygame.Rect(700, 100 + space_box*2, 200, 100).collidepoint(event.pos):
                current_window = WINDOWS['ON_GAME']
                data = {
                    "start": True,
                    "mode": 10,
                }
                data['words_right'] = modes[2].words_right[0]
                data['words_wrong'] = modes[2].words_wrong[0]
                json_dump = json.dumps(data)
                client.publish(PUBLISH_TOPIC, json_dump)
                print("Mode 10")

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
        while (r < progress[index]):
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
    global current_window, run, childrens, progress
    client = connect_mqtt()
    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(700, 100, 200, 100)
    game_name = pygame.Rect(200, 100, 600, 300)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    child_name = ''
    current_window = WINDOWS['WAITING_CHILDRENS']
    image = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\duck_icon.jpg')
    image = pygame.transform.scale(image, (50, 50))

    while run:
        if current_window == WINDOWS['WAITING_CHILDRENS']:
            load_page_waitting_child(win, font, child_name,
                                     input_box, color, game_name, input_enter, pygame.event.get(), client,  active, color_active, color_inactive)
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
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    read_config_file(modes)
    main()
    pygame.quit()
