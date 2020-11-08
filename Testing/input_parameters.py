import json

with open('input.json') as json_file:
    data = json.load(json_file)
    for p in data['modes']:
        print('Name: ' + p['name'])
        print('Website: ' + p['from'])
        print('From: ' + p['clear'])
        print('')
    print(data['hola'])