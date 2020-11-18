import xlsxwriter


class ChildrenEvaluation:
    def __init__(self, name, words):
        self.words = words
        self.name = name
        self.fails = []
        self.final_time = 0
        self.final_punctuation = 0


def generate_excel(childrens, words, total_words_fails):
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
    worksheet.write('B1', 'Children Names')
    worksheet.write('C1', 'Compleat Time(s)')
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

    chart = workbook.add_chart({'type': 'column'})

    # chart.add_series({'values': '=Sheet1!$B$2:$B$6'})
    chart.add_series({'values': '=Sheet1!$C$2:$C$6'})
    chart.add_series({'values': '=Sheet1!$D$2:$D$6'})
    chart.set_title({'name': 'Puntuación y tiempos de niños'})
    chart.set_legend({'position': 'bottom'})
    worksheet.insert_chart('N1', chart)
    chart.set_plotarea({
        'border': {'color': 'red', 'width': 2, 'dash_type': 'dash'},
        'fill':   {'color': '#FFFFC2'}
    })

    workbook.close()


# Invent the data first:
childrens = []
commond_words = ["galdiolo", "flor", "palmera", "bloso"]
# Nor sure how to get the total fails:
total_words_fails = [12, 4, 16, 3, 5, 2, 0, 2, 3, 5]

a = ChildrenEvaluation('Paco', commond_words)
a.final_punctuation = 67
a.final_time = 12
a.fails = [1, 0, 0, 1]
childrens.append(a)
a = ChildrenEvaluation('Pepe', commond_words)
a.final_punctuation = 35
a.final_time = 23
a.fails = [1, 0, 0, 1]
childrens.append(a)
a = ChildrenEvaluation('Bea', commond_words)
a.final_time = 54
a.final_punctuation = 24
a.fails = [1, 1, 1, 1]
childrens.append(a)
a = ChildrenEvaluation('Rubén', commond_words)
a.final_time = 32
a.final_punctuation = 47
a.fails = [0, 0, 0, 1]
childrens.append(a)
a = ChildrenEvaluation('María', commond_words)
a.final_time = 122
a.final_punctuation = 33
a.fails = [0, 1, 0, 1]
childrens.append(a)

generate_excel(childrens, commond_words, total_words_fails)
