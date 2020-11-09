import pygame
import json
import paho.mqtt.client as mqtt

PUBLISH_TOPIC = 'TFG_B/teacher'
LISTEN_TOPIC = 'TFG_B/children'
childrens = []

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
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # Example json: {"esp":"A1","beacon":[ {"uuid":5245,"distance":1.23},{"uuid":52345, "distance":1.23 }]}
    msg = str(message.payload.decode("utf-8"))
    print("message received: ", msg)
    parsed_json = (json.loads(msg))
    print('_________________')
    new_children = parsed_json['uuid']
    print(new_children)
    # if (new_children in childrens):
    #     pass
    # else:
    #     childrens.append(new_children)
    childrens.append(new_children)

    print(childrens)
    
    #     # print(parsed_json['esp'])
    #     # Get the distance and the uuid of the beacon:
    #     beacon_distance = float(parsed_json['beacon'][index]['distance'])
    #     beacon_uuid = str(parsed_json['beacon'][index]['uuid'])


def load_page_waitting_child(win, font, child_name, input_box, color, game_name, input_enter):
    win.fill((30, 30, 30))

    pygame.draw.rect(win, (255, 255, 255), (700, 100, 200,100))
    txt_game_name = font.render("5 WORDS", True,  (0x00,0x00,0x00))
    win.blit(txt_game_name, (750, 140))
    
    pygame.draw.rect(win, (181, 255, 255), (100, 100, 500, 600))
    index = 0
    for c in childrens:
        a = font.render(c, True, (0x00, 0x00, 0x00))
        win.blit(a, (200, 200 + index))
        index += 50

    # txt_game_name = font.render("Enter", True, (0xFF,0xFF,0xFF))
    # win.blit(txt_game_name, (350, 220))

    i = 0
    while i < 1024:
        # pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
        # pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
        i += 100


def main():
    client = connect_mqtt()
    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(450, 600, 140, 50)
    game_name = pygame.Rect(200, 100, 600, 300)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    child_name = ''
    run = True
    image = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\duck_icon.jpg')
    image = pygame.transform.scale(image, (50, 50))
    remove_window = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                if input_enter.collidepoint(event.pos):
                    if (len(child_name) != 0):
                        remove_window = True
                        msg = "{\"uuid\":\""+child_name+"\"}"
                        client.publish(PUBLISH_TOPIC, msg)
                        print("Enter Press")
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(child_name)
                        child_name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        child_name = child_name[:-1]
                    else:
                        child_name += event.unicode
        if not remove_window:
            load_page_waitting_child(win, font, child_name,
                                     input_box, color, game_name, input_enter)
        else:
            win.fill((30, 30, 30))
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
