import pygame
import json
import paho.mqtt.client as mqtt
from ModeClass import Mode, ChildrenEvaluation
import random
import time
import xlsxwriter
import copy

PUBLISH_TOPIC = 'TFG_B/teacher'
LISTEN_TOPIC = 'TFG_B/children'
childrens = []
progress = []
progress_colors = []
children_evaluation = []
max_number_questions = 0
WINDOWS = {
    'WAITING_CHILDRENS': 0,
    'ON_GAME': 1,
    'FINISH': 3,
}
parser = {
    "waiting_children_background": "",
    "waiting_children_name_container": "",
    "waiting_children_buttons_back": "",
    "waiting_children_letter": "",
    "on_game_background": "",
    "on_game_name_container": "",
    "on_game_letter": "",
    "on_game_progress_bar_ok": "",
    "on_game_progress_bar_wrong": "",
    "end_game_background": "",
    "end_game_letter": "",
}
current_window = 1111
run = True
modes = []
global_clock = 0


def read_config_file(modes, parser, pygame):
    with open('input.json') as json_file:
        data = json.load(json_file)
        for index, p in enumerate(data['modes']):
            modes.append(Mode())
            modes[index].words_right.append(p["words"])
            modes[index].words_wrong.append(p["correct_word"])
            modes[index].images.append(p["images"])
        dimensions = (1024, 768)
        # First get the shared data:
        parser['game_name'] = data['global_images']['game_name']
        parser['game_logo'] = data['global_images']['game_logo']
        # Waiting data load:
        parser['waiting_children_background'] = data['color_config_teacher']['waiting_children_background']
        parser['waiting_children_background'] = pygame.image.load(
            'images/' + parser['waiting_children_background'])
        parser['waiting_children_background'] = pygame.transform.scale(
            parser['waiting_children_background'], dimensions)

        parser['waiting_children_name_container'] = data['color_config_teacher']['waiting_children_name_container']
        parser['waiting_children_name_container'] = tuple(
            map(int, str(parser['waiting_children_name_container'])[1:-1].split(',')))

        parser['waiting_children_buttons_back'] = data['color_config_teacher']['waiting_children_buttons_back']
        parser['waiting_children_buttons_back'] = tuple(
            map(int, str(parser['waiting_children_buttons_back'])[1:-1].split(',')))

        parser['waiting_children_letter'] = data['color_config_teacher']['waiting_children_letter']
        parser['waiting_children_letter'] = tuple(
            map(int, str(parser['waiting_children_letter'])[1:-1].split(',')))

        # Waiting data load:
        parser['on_game_background'] = data['color_config_teacher']['on_game_background']
        parser['on_game_background'] = pygame.image.load(
            'images/' + parser['on_game_background'])
        parser['on_game_background'] = pygame.transform.scale(
            parser['on_game_background'], dimensions)

        parser['on_game_name_container'] = data['color_config_teacher']['on_game_name_container']
        parser['on_game_name_container'] = tuple(
            map(int, str(parser['on_game_name_container'])[1:-1].split(',')))

        parser['on_game_letter'] = data['color_config_teacher']['on_game_letter']
        parser['on_game_letter'] = tuple(
            map(int, str(parser['on_game_letter'])[1:-1].split(',')))

        # Waiting data load:
        parser['end_game_background'] = data['color_config_teacher']['end_game_background']
        parser['end_game_background'] = pygame.image.load(
            'images/' + parser['end_game_background'])
        parser['end_game_background'] = pygame.transform.scale(
            parser['end_game_background'], dimensions)

        parser['end_game_letter'] = data['color_config_teacher']['end_game_letter']
        parser['end_game_letter'] = tuple(
            map(int, str(parser['end_game_letter'])[1:-1].split(',')))
        parser['on_game_progress_bar_ok'] = data['color_config_teacher']['on_game_progress_bar_ok']
        parser['on_game_progress_bar_ok'] = tuple(
            map(int, str(parser['on_game_progress_bar_ok'])[1:-1].split(',')))
        parser['on_game_progress_bar_wrong'] = data['color_config_teacher']['on_game_progress_bar_wrong']
        parser['on_game_progress_bar_wrong'] = tuple(
            map(int, str(parser['on_game_progress_bar_wrong'])[1:-1].split(',')))

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
    global progress, childrens, children_evaluation, progress_colors
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
                children_evaluation[index].final_time = global_clock
                children_evaluation[index].words.append(parsed_json['words'])
                # Save in progress bar colors the 0 and 1 of the correct or incorrect responses
                if (len(children_evaluation[index].progress_bar_colors) <= max_number_questions):
                    if (int(points) == 0):
                        children_evaluation[index].fails.append("1")
                        children_evaluation[index].progress_bar_colors.append(
                            0)
                    else:
                        children_evaluation[index].fails.append("0")
                        children_evaluation[index].progress_bar_colors.append(
                            1)
                else:
                    # print("yes")
                    for find_0 in children_evaluation[index].progress_bar_colors:
                        if find_0 == 0:
                            find_0 = 1
                            # print("remake", children_evaluation[index].progress_bar_colors)
                            break

    else:
        if (len(childrens) > 24):
            childrens.append("dijimos 25 guapita ...")
        else:
            question = parsed_json['question']
            childrens.append(new_children)
            progress.append(question)
            progress_colors.append("2")
            # Evaluation part:
            a = ChildrenEvaluation(new_children, [])
            a.progress_bar_colors.append(2)
            children_evaluation.append(a)

    for i in children_evaluation:
        i.print_itself()

def generate_excel(childrens):
    children_names = []
    children_punctuations = []
    total_words_times = []
    # I get the most failed words:
    total_words = childrens[0].words
    total_failed = list()
    for _ in total_words:
        total_failed.append(0)
    index = 0
    for c in childrens:
        children_names.append(c.name)
        children_punctuations.append(c.final_punctuation)
        total_words_times.append(c.final_time)
        for w in c.words:
            for i, t in enumerate(total_words):
                if w == t:
                    if c.fails[i] == 1:
                        total_failed[i] += 1

    print('All the child names:', children_names)
    print('Words to match:', total_words)
    print('Total failed:', total_failed)
    print('All children points :', children_punctuations)
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
    for index, c in enumerate(total_words):
        worksheet.write(row, col, c)
        worksheet.write(row, col+1, total_failed[index])
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
    chart.add_series({'categories': '=Sheet1!$B$2:$B$'+str(len(childrens)+1),
                      'values': '=Sheet1!$C$2:$C$'+str(len(childrens)+1),
                      'name': 'Tiempo (s)'})
    chart.add_series({'values': '=Sheet1!$D$2:$D$'+str(len(childrens)+1),
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
    # print(position)

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
    global run, current_window, childrens, progress, PUBLISH_TOPIC, modes,  parser, max_number_questions

    # win.fill(0, 0, 0)
    win.blit(parser['waiting_children_background'], (0, 0))
    pygame.draw.rect(
        win, parser['waiting_children_name_container'], (100, 100, 500, 600))
    txt_game_name = font.render(parser['game_name'], True,  (0, 0, 0))
    win.blit(txt_game_name, (700, 50))
    win.blit(image, (900, 25))

    space_box = 200
    pygame.draw.rect(
        win, parser['waiting_children_buttons_back'], (700, 100, 200, 100))
    txt_game_name = font.render(
        "6 WORDS", True,  parser['waiting_children_letter'])
    win.blit(txt_game_name, (750, 140))

    pygame.draw.rect(win, parser['waiting_children_buttons_back'],
                     (700, 100 + space_box, 200, 100))
    txt_game_name = font.render(
        "8 WORDS", True,  parser['waiting_children_letter'])
    win.blit(txt_game_name, (750, 140 + space_box))

    pygame.draw.rect(win, parser['waiting_children_buttons_back'],
                     (700, 100 + space_box*2, 200, 100))
    txt_game_name = font.render(
        "12 WORDS", True,  parser['waiting_children_letter'])
    win.blit(txt_game_name, (750, 140 + space_box*2))

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the  rect.
            send_to_app = [False, 0, 0]
            if pygame.Rect(700, 100, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 6, 0]
                max_number_questions = 6
            if pygame.Rect(700, 100 + space_box, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 8, 1]
                max_number_questions = 8
            if pygame.Rect(700, 100 + space_box*2, 200, 100).collidepoint(event.pos):
                send_to_app = [True, 12, 2]
                max_number_questions = 12
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
        a = font.render(c, True, parser['waiting_children_letter'])
        win.blit(a, (150+spacing, 150 + offset))
        offset += 40
        if (index == 12):
            offset = 0
            spacing = 250

    # txt_game_name = font.in("Enter", True, (0xFF,0xFF,0xFF))
    # win.blit(txt_game_name, (350, 220))


def load_page_game(win, font, events, image):
    global run, childrens, progress, current_window, progress_colors

    win.blit(parser['on_game_background'], (0, 0))

    txt_game_name = font.render(parser['game_name'], True,  (0, 0, 0))
    win.blit(txt_game_name, (700, 50))
    win.blit(image, (900, 25))

    # The list of childrens:
    pygame.draw.rect(
        win, parser['on_game_name_container'], (50, 100, 900, 600))
    offset = 0
    spacing = 0
    r = 0
    for index, c in enumerate(children_evaluation):
        a = font.render(str(childrens[index]), True, parser['on_game_letter'])
        win.blit(a, (100+spacing, 150 + offset))
        data_to_print = ""
        data_to_print += str(childrens[index])
        for color in c.progress_bar_colors:
            if (color == 0):
                pygame.draw.rect(win, (0, 0, 0), (320 + r * 20 +
                                                  spacing, 150 + offset, 20, 30))
                data_to_print += " [ 0 ]"
                pygame.draw.rect(win, parser['on_game_progress_bar_wrong'], (320 + r *
                                                                             20+2+spacing, 150+2 + offset, 20-4, 30-4))
            elif (color == 1):
                pygame.draw.rect(win, (0, 0, 0), (320 + r * 20 +
                                                  spacing, 150 + offset, 20, 30))
                data_to_print += " [ 1 ]"
                pygame.draw.rect(win, parser['on_game_progress_bar_ok'], (320 + r *
                                                                          20+2+spacing, 150+2 + offset, 20-4, 30-4))
            r += 1

        offset += 40
        r = 0
        if (index == 12):
            offset = 0
            spacing = 450

    rec_close = pygame.Rect(900, 100, 40, 40)
    pygame.draw.rect(win, (200,200,200), rec_close)
    txt_game_name = font.render("X", True,  (0,0,0))
    win.blit(txt_game_name, (910, 110))

    font_new = pygame.font.Font(None, 42)
    txt_game_name = font_new.render(str(global_clock), True, (0, 0, 0))
    win.blit(txt_game_name, (500, 720))
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("press")
            if rec_close.collidepoint(event.pos):
                print("press")
                current_window = WINDOWS['FINISH']


def get_ranking(children_evaluation):
    _children_evaluation = copy.copy(children_evaluation)
    ranking = dict()
    max_punctuation = 0
    for _ in range(0, len(_children_evaluation)):
        for c in _children_evaluation:
            if c.final_punctuation >= max_punctuation:
                max_punctuation = c.final_punctuation

        for c in _children_evaluation:
            if c.final_punctuation == max_punctuation:
                ranking[c.name] = c.final_punctuation
                _children_evaluation.remove(c)
        max_punctuation = 0
    return ranking


def load_page_end(win, font, events, image):
    global run, childrens, progress, children_evaluation
    win.blit(parser['end_game_background'], (0, 0))
    ranking = get_ranking(children_evaluation)
    offset = 0
    for keys, values in ranking.items():
        txt_game_name = font.render(
            str(values)+" - "+str(keys), True, parser['end_game_letter'])
        win.blit(txt_game_name, (360, 225 + offset))
        offset += 50
        # Get the most point chi ldren and print it:
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            ranking = get_ranking(children_evaluation)
            generate_excel(children_evaluation)


def main():
    global current_window, run, childrens, progress, parser, global_clock

    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    current_window = WINDOWS['WAITING_CHILDRENS']

    image_logo = pygame.image.load('images/' + parser['game_logo'])
    image_logo = pygame.transform.scale(image_logo, (50, 50))
    timer_update_screen = int(round(time.time()))
    time_send_ranking = int(round(time.time()))
    while run:
        if current_window == WINDOWS['WAITING_CHILDRENS']:
            load_page_waitting_child(
                win, font, pygame.event.get(), client, image_logo)
        elif current_window == WINDOWS['ON_GAME']:
            load_page_game(win, font, pygame.event.get(), image_logo)
        elif current_window == WINDOWS['FINISH']:
            load_page_end(win, font, pygame.event.get(), image_logo)
        # i = 0
        # while i < 1024:
        #     pygame.draw.line(win, (133, 128, 123), (i, 0), (i, 1024), 1)
        #     pygame.draw.line(win, (133, 128, 123), (0, i), (1024, i), 1)
        #     i += 100
        pygame.display.flip()
        clock.tick(100)
        if (current_window == WINDOWS['ON_GAME'] and int(round(time.time())) - timer_update_screen >= 1):
            timer_update_screen = int(round(time.time()))
            global_clock += 1
        if (current_window != WINDOWS['WAITING_CHILDRENS']and int(round(time.time())) - time_send_ranking >= 5):
            time_send_ranking = int(round(time.time()))
            rank = get_ranking(children_evaluation)
            update_rank = {
                'names':  [],
                'points': []
            }
            for keys, values in rank.items():
                update_rank['points'].append(values)
                update_rank['names'].append(keys)
            client.publish(PUBLISH_TOPIC,json.dumps(update_rank))


if __name__ == '__main__':
    pygame.init()
    client = connect_mqtt()
    read_config_file(modes, parser, pygame)
    main()
    pygame.quit()
