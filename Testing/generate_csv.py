import random
import xlsxwriter


class ChildrenEvaluation:
    def __init__(self, name, words):
        self.words = words
        self.name = name
        self.fails = []
        self.final_time = 0
        self.final_punctuation = 0

    def __repr__(self):
        data = ""
        data += "Name: " + self.name + "\n"
        data += " - Words: "
        for w in self.words:
            data += str(w) + ", "
        data += "\n"

        return data


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


# Invent the data first:
childrens = []
words = ["cholcolate", "esto es", "una prueba", "la verdad"]


a = ChildrenEvaluation('Paco', words)
a.final_punctuation = 67
a.final_time = 12
a.fails = [1, 0, 0, 1]
childrens.append(a)
a = ChildrenEvaluation('Pepe', words)
a.final_punctuation = 35
a.final_time = 23
a.fails = [1, 0, 0, 1]
childrens.append(a)
words = ["una prueba", "la verdad", "cholcolate", "esto es"]
random.seed(4)
random.shuffle(words)
a = ChildrenEvaluation('Bea', words)
a.final_time = 54
a.final_punctuation = 24
a.fails = [1, 1, 1, 1]
childrens.append(a)
random.seed(3)
random.shuffle(words)
words = ["una prueba", "cholcolate", "la verdad" "esto es"]
a = ChildrenEvaluation('Rubén', words)
a.final_time = 32
a.final_punctuation = 47
a.fails = [0, 0, 0, 1]
childrens.append(a)

generate_excel(childrens)

