import pygame
import json
import paho.mqtt.client as mqtt

WINDOWS = {
    'LOGIN': 0,
    'WAITING_TEACHER': 1,
    'ON_GAME': 2,
    'FINISH': 3,
}
current_window = 1111
PUBLISH_TOPIC = 'TFG_B/children'
LISTEN_TOPIC = 'TFG_B/teacher'

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
    client.publish("master_beacon/ack", msg)
    client.loop_start()  # start the loop
    return client


def on_message(client, userdata, message):
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # Example json: {"esp":"A1","beacon":[ {"uuid":5245,"distance":1.23},{"uuid":52345, "distance":1.23 }]}
    global current_window, WINDOWS
    msg = str(message.payload.decode("utf-8"))
    # print("message received: ", msg)
    parsed_json = json.loads(msg)
    print(current_window)
    # print(parsed_json['start'])
    if (parsed_json['start']):
        current_window = WINDOWS['ON_GAME']
        print(current_window)
        # print(parsed_json['mode'])ç

    #     # print(parsed_json['esp'])
    #     # Get the distance and the uuid of the beacon:
    #     beacon_distance = float(parsed_json['beacon'][index]['distance'])
    #     beacon_uuid = str(parsed_json['beacon'][index]['uuid'])


def load_page_login(win, image, font, child_name, input_box, color, game_name, input_enter):
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


def load_page_waiting(win, font, image, child_name):
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


def load_page_game(win, font, image_children, child_name, image_game_logo):
    win.fill((30, 30, 30))
    win.blit(image_game_logo, (870, 30)) 
    # Render the current text.
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (200, 50, 600, 150), 2)
    pygame.draw.rect(win, (0xFF, 0xFF, 0xFF), (300, 300, 400, 100), 2)

    color_letters = (163, 227, 255)
    txt_surface = font.render("Palabra / Frase / Audio", True, color_letters)
    win.blit(txt_surface, (300, 120))
    txt_surface = font.render("PREGUNTA", True, color_letters)
    win.blit(txt_surface, (400, 333))


    color_circle = (87, 154, 230)
    radio_cicle = 50
    pygame.draw.circle(win, color_circle, (100, 300), radio_cicle)
    pygame.draw.circle(win, color_circle, (500, 600), radio_cicle)
    pygame.draw.circle(win, color_circle, (900, 300), radio_cicle)

    color_text = (0, 0, 0)
    offset = 17
    txt_surface = font.render("SI", True, color_text)
    win.blit(txt_surface, (100-offset, 300-offset))
    txt_surface = font.render("NO", True, color_text)
    win.blit(txt_surface, (900-offset, 300-offset))
    txt_surface = font.render("01", True, color_text)
    win.blit(txt_surface, (500-offset, 600-offset))

    #Child name and picture:
    txt_surface = font.render(child_name, True, color_letters)
    win.blit(txt_surface, (100, 700))
    win.blit(image_children, (40, 700))



def load_page_end(win):
    pass


def main():
    global current_window
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
    active = False
    child_name = ''
    run = True
    current_window =  WINDOWS['LOGIN']
    image = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\duck_icon.jpg')
    image = pygame.transform.scale(image, (50, 50))
    image_game_logo = pygame.image.load(
        r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Child_Teacher\images\game_logo.png')
    image_game_logo = pygame.transform.scale(image_game_logo, (100, 100))

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
                    if (current_window== WINDOWS['LOGIN']):
                        if (len(child_name) != 0):
                            current_window = WINDOWS['WAITING_TEACHER']
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

        # Game state machine:
        if (current_window == WINDOWS['LOGIN']):
            load_page_login(win, image, font, child_name,
                            input_box, color, game_name, input_enter)
        elif (current_window == WINDOWS['WAITING_TEACHER']):
            if (len(child_name) == 0):
                child_name = "Laura Lomez"
            load_page_waiting(win, font, image, child_name)
            
        elif (current_window == WINDOWS['ON_GAME']):
            if (len(child_name) == 0):
                child_name = "Laura Lomez"
            load_page_game(win, font, image, child_name, image_game_logo)
        elif (current_window == WINDOWS['FINISH']):
            win.fill((110, 220, 30))
        # i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0),(i,1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i),(1024,i), 1)
        #     i += 100
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
