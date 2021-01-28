import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode
import random
import time
import xlsxwriter


PUBLISH_TOPIC = 'TFG_B/teacher'
LISTEN_TOPIC = 'TFG_B/children'
childrens = []
progress = []
children_evaluation = []

WINDOWS = {
    'WAITING_CHILDRENS': 0,
    'ON_GAME': 1,
    'FINISH': 3,
}
parser = {
    "game_name": "",
    "game_logo": "",
    "background": "",
    "mode_buttons": "",
    "children_background": "",
    "letters": "",
    "progress_bar": ""
}
current_window = 1111
run = True
modes = []
global_clock = 0
for i in range(0,20):
    childrens.append('Bea Puente')
    progress.append(random.randint(0,8))
childrens.append('Rubén Arce')
progress.append(1)
childrens.append('Ubu Ventajas')
progress.append(0)


class ChildrenEvaluation:
    def __init__(self, name, words):
        self.words = words
        self.name = name
        self.fails = []
        self.final_time = 0
        self.final_punctuation = 0

    def print_itself(self):
        print('++> ', self.name)
        print('  words:', self.words)
        print('  fails: ', self.fails)
        print('  final_time: ', self.final_time)
        print('  final_punctuation: ', self.final_punctuation)


def read_config_file(modes, parser):
    with open('input.json') as json_file:
        data = json.load(json_file)
        for index, p in enumerate(data['modes']):
            modes.append(Mode())
            modes[index].words_right.append(p["words"])
            modes[index].words_wrong.append(p["correct_word"])
            modes[index].images.append(p["images"])
        parser['game_name'] = data['global_images']['game_name']
        parser['game_logo'] = data['global_images']['game_logo']
        parser['background'] = data['color_config_teacher']['background']
        parser['background'] = tuple(
            map(int, str(parser['background'])[1:-1].split(',')))

        parser['children_background'] = data['color_config_teacher']['children_background']
        parser['children_background'] = tuple(
            map(int, str(parser['children_background'])[1:-1].split(',')))

        parser['mode_buttons'] = data['color_config_teacher']['mode_buttons']
        parser['mode_buttons'] = tuple(
            map(int, str(parser['mode_buttons'])[1:-1].split(',')))

        parser['letters'] = data['color_config_teacher']['letters']
        parser['letters'] = tuple(
            map(int, str(parser['letters'])[1:-1].split(',')))

        parser['progress_bar'] = data['color_config_teacher']['progress_bar']
        parser['progress_bar'] = tuple(
            map(int, str(parser['progress_bar'])[1:-1].split(',')))
    # for m in modes:
    #     m.print_itself()
    # print (parser)


def connect_mqtt():
    broker_address = "broker.mqttdashboard.com"
    # create new instance
    client = mqtt.Client("a"+str(random.randint(121233, 35123234)) + "f")
    client.on_message = on_message  # attach function to callback
    # print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    # print("Subscribing to topic", LISTEN_TOPIC)
    client.subscribe(LISTEN_TOPIC)
    # print("Publishing message to topic", "master_beacon_ack")
    msg = '''{"ok":true}'''
    client.publish("TFG_B/ack", msg)
    client.loop_start()  # start the loop
    return client


def on_message(client, userdata, message):
    global progress, childrens, children_evaluation
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # Example json: {"esp":"A1","beacon":[ {"uuid":5245,"distance":1.23},{"uuid":52345, "distance":1.23 }]}
    msg = str(message.payload.decode("utf-8"))
    # print("message received: ", msg)
    parsed_json = json.loads(msg)
    new_children = parsed_json['uuid']

    if (new_children in childrens):
        # Update the status of the questions
        for index, c in enumerate(childrens):
            if (c == new_children):
                progress[index] = parsed_json['question']

        for index, c in enumerate(children_evaluation):
            if (c.name == new_children):
                points = parsed_json['punctuation']
                children_evaluation[index].final_punctuation += int(points)
                if (int(points) == 0):
                    children_evaluation[index].fails.append("1")
                else:
                    children_evaluation[index].fails.append("0")
                children_evaluation[index].final_time = global_clock

    else:
        if (len(childrens) > 24):
            childrens.append("dijimos 25 guapita ...")
        else:
            question = parsed_json['question']
            childrens.append(new_children)
            progress.append(question)
            # Evaluation part:
            a = ChildrenEvaluation(new_children, [])
            children_evaluation.append(a)

    # print('childrens:',childrens)
    # print('progress:',progress)
    # for c in children_evaluation:
    #     c.print_itself()


def generate_excel(childrens, words, total_words_fails):
    words = childrens[0].words
    children_names = []
    children_punctuations = []
    total_words_times = []

    for c in childrens:
        children_names.append(c.name)
        children_punctuations.append(c.final_punctuation)
        total_words_times.append(c.final_time)

    print('All the child names:', children_names)
    print('All children points :', children_punctuations)
    # I need all the words to be the same.... to check with B
    print('Total fails :', total_words_fails)
    print('Total times of the game :', total_words_times)

    # I create the csv:
    workbook = xlsxwriter.Workbook('B.xlsx')
    worksheet = workbook.add_worksheet()

    # Format the document:
    worksheet.write('B1', 'Names')
    worksheet.write('C1', 'Time(s)')
    worksheet.write('D1', 'Punctuation')

    worksheet.write('G1', 'Words')
    worksheet.write('H1', 'Fails')

    worksheet.write('J1', 'Names')
    worksheet.write('K1', 'Words')
    worksheet.write('L1', 'Fails')

    row = 1
    col = 1
    # Save the data:
    for index, c in enumerate(children_names):
        worksheet.write(row, col, c)
        worksheet.write(row, col+1, total_words_times[index])
        worksheet.write(row, col+2, children_punctuations[index])
        row += 1
    row = 1
    col = 6
    for index, c in enumerate(words):
        worksheet.write(row, col, c)
        worksheet.write(row, col+1, total_words_fails[index])
        row += 1
    row = 1
    col = 9
    for index, c in enumerate(childrens):
        worksheet.write(row, col, c.name+':')
        col += 1
        initial_row = row
        for w in c.words:
            worksheet.write(row, col, w)
            row += 1
        col += 1
        row = initial_row
        for f in c.fails:
            worksheet.write(row, col, f)
            row += 1
        col -= 2
        row += 1
    # Children Time and punctuation:
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({'categories': '=Sheet1!$B$2:$B$26',
                      'values': '=Sheet1!$C$2:$C$26',
                      'name': 'Tiempo (s)'})
    chart.add_series({'values': '=Sheet1!$D$2:$D$26',
                      'name': 'Puntuación (pts)'})
    chart.set_title({'name': 'Puntuación y tiempos de niños'})
    chart.set_legend({'position': 'bottom'})
    worksheet.insert_chart('N1', chart)
    chart.set_plotarea({
        'border': {'color': 'red', 'width': 2, 'dash_type': 'dash'},
        'fill':   {'color': '#FFFFC2'}
    })
    # Words and fails:
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({'categories': '=Sheet1!$G$2:$G$5',
                      'values': '=Sheet1!$H$2:$H$5',
                      'name': 'Fallos por palabra'})
    chart.set_title({'name': 'Palabras más falladas'})
    chart.set_legend({'position': 'bottom'})
    worksheet.insert_chart('N16', chart)
    chart.set_plotarea({
        'border': {'color': 'red', 'width': 2, 'dash_type': 'dash'},
        'fill':   {'color': '#FFFFC2'}
    })
    # Every children:
    row = [2, 5]

    coordenates = []
    values = []
    position = [1]
    max_coordenates = len(childrens)+1
    for i in range(0, max_coordenates):
        coordenates.append("=Sheet1!$K$" + str(row[0]) + ":$K$" + str(row[1]))
        values.append("=Sheet1!$L$" + str(row[0]) + ":$L$" + str(row[1]))
        if i != 0:
            position.append(i*15)
        row[0] += 5
        row[1] += 5
    print(position)

    for index, c in enumerate(childrens):
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({'categories': coordenates[index],
                          'values': values[index],
                          'name': 'Fallos por palabra'})
        chart.set_title({'name': str(c.name)})
        chart.set_legend({'position': 'bottom'})
        pos = 0

        worksheet.insert_chart('V'+str(position[index]), chart)
        chart.set_plotarea({
            'border': {'color': 'red', 'width': 2, 'dash_type': 'dash'},
            'fill':   {'color': '#FFFFC2'}
        })

    workbook.close()


def load_page_waitting_child(win, font, events, client, image):
    global run, current_window, childrens, progress, PUBLISH_TOPIC, modes,  parser

    win.fill(parser['background'])
    pygame.draw.rect(win, parser['children_background'], (100, 100, 500, 600))
    txt_game_name = font.render(parser['game_name'], True,  (240, 240, 240))
    win.blit(txt_game_name, (700, 50))
    win.blit(image, (900, 25))

    space_box = 200
    pygame.draw.rect(win, parser['mode_buttons'], (700, 100, 200, 100))
    txt_game_name = font.render("4 WORDS", True,  parser['letters'])
    win.blit(txt_game_name, (750, 140))

    pygame.draw.rect(win, parser['mode_buttons'],
                     (700, 100 + space_box, 200, 100))
    txt_game_name = font.render("6 WORDS", True,  parser['letters'])
    win.blit(txt_game_name, (750, 140 + space_box))

    pygame.draw.rect(win, parser['mode_buttons'],
                     (700, 100 + space_box*2, 200, 100))
    txt_game_name = font.render("8 WORDS", True,  parser['letters'])
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


def load_page_game(win, font, events, image):
    global run, childrens, progress, current_window
    win.fill(parser['background'])

    # The list of childrens:
    pygame.draw.rect(win, parser['children_background'], (50, 100, 900, 600))
    offset = 0
    spacing = 0
    for index, c in enumerate(childrens):
        a = font.render(c, True, parser['letters'])
        win.blit(a, (100+spacing, 150 + offset))
        r = 0
        while (r < int(progress[index])):
            pygame.draw.rect(win, (0, 0, 0), (320 + r * 20 +
                                              spacing, 150 + offset, 20, 30))
            pygame.draw.rect(win, parser['progress_bar'], (320 + r *
                                                           20+2+spacing, 150+2 + offset, 20-4, 30-4))
            r += 1
        offset += 40
        if (index == 12):
            offset = 0
            spacing = 450
    offset = 0
    for index, p in enumerate(progress):
        while (offset < int(p)):
            pygame.draw.rect(win, (0, 0, 0), (320 + offset * 20, 150, 20, 30))
            pygame.draw.rect(
                win, parser['progress_bar'], (320 + offset * 20+2, 150+2, 20-4, 30-4))
            offset += 1

    rec_close = pygame.Rect(800, 20, 40, 40)
    pygame.draw.rect(win, parser['mode_buttons'], rec_close)
    txt_game_name = font.render("X", True,  parser['letters'])
    win.blit(txt_game_name, (805, 20))
    
    font_new = pygame.font.Font(None, 42)
    txt_game_name = font_new.render(str(global_clock), True, (221, 223, 212))
    win.blit(txt_game_name, (500, 720))
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("press")
            if rec_close.collidepoint(event.pos):
                print("press")
                current_window = WINDOWS['FINISH']


def load_page_end(win, font, events, image):
    global run, childrens, progress
    win.fill(parser['background'])

    for event in events:
        if event.type == pygame.QUIT:
            run = False
            print("generate the excel and close all")
            # Invent the data first:
            commond_words = ["galdiolo", "flor", "palmera", "bloso"]
            # Nor sure how to get the total fails:
            total_words_fails = [12, 4, 16, 3, 5, 2, 0, 2, 3, 5]
            for c in children_evaluation:
                c.words = commond_words
            generate_excel(children_evaluation,
                           commond_words, total_words_fails)


def main():
    global current_window, run, childrens, progress, parser, global_clock

    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    current_window = WINDOWS['WAITING_CHILDRENS']

    image = pygame.image.load('images/' + parser['game_logo'])
    image = pygame.transform.scale(image, (50, 50))
    timer_update_screen = int(round(time.time()))

    while run:
        if current_window == WINDOWS['WAITING_CHILDRENS']:
            load_page_waitting_child(
                win, font, pygame.event.get(), client, image)
        elif current_window == WINDOWS['ON_GAME']:
            load_page_game(win, font, pygame.event.get(), image)
        elif current_window == WINDOWS['FINISH']:
            load_page_end(win, font, pygame.event.get(), image)
        i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
        #     i += 100
        pygame.display.flip()
        clock.tick(100)
        if (current_window == WINDOWS['ON_GAME'] and int(round(time.time())) - timer_update_screen >= 1):
            timer_update_screen = int(round(time.time()))
            global_clock += 1



if __name__ == '__main__':
    pygame.init()
    client = connect_mqtt()
    read_config_file(modes, parser)
    main()
    pygame.quit()
