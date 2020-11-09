import json
from ModeClass import Mode

modes = []
with open('input.json') as json_file:
    data = json.load(json_file)
    for index, p in enumerate(data['modes']):
        modes.append(Mode(p['name']))
        modes[index].words_right.append( p["words_right"])
        modes[index].words_wrong.append(p["words_wrong"])
        modes[index].images.append(p["images"])

for m in modes:
    m.print_itself()