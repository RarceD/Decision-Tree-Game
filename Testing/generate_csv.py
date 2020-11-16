import xlsxwriter


class ChildrenEvaluation:
    def __init__(self, name, words):
        self.words = words
        self.name = name
        self.fails = []
        self.final_time = 0
        self.final_punctuation = 0


# I create the csv:
workbook = xlsxwriter.Workbook('B.xlsx')
worksheet = workbook.add_worksheet()

# Invent the data first:
childrens = []
words = ["galdiolo", "flor", "palmera", "bloso"]
children_names = []
children_punctuations = []

total_words_times = []
total_words_fails = [12, 4, 16, 3, 5, 2, 0, 2, 3, 5]

a = ChildrenEvaluation('Paco', words)
a.final_punctuation = 67
a.final_time = 12
a.fails = [1,0,0,1]
childrens.append(a)
a = ChildrenEvaluation('Pepe', words)
a.final_punctuation = 35
a.final_time = 23
a.fails = [1,0,0,1]
childrens.append(a)
a = ChildrenEvaluation('Bea', words)
a.final_time = 54
a.final_punctuation = 24
a.fails = [1,1,1,1]
childrens.append(a)
a = ChildrenEvaluation('Rubén', words)
a.final_time = 32
a.final_punctuation = 47
a.fails = [0,0,0,1]
childrens.append(a)
a = ChildrenEvaluation('María', words)
a.final_time = 122
a.final_punctuation = 33
a.fails = [0,1,0,1]
childrens.append(a)

for c in childrens:
    children_names.append(c.name)
    children_punctuations.append(c.final_punctuation)
    total_words_times.append(c.final_time)

print('All the child names:', children_names)
print('All children points :', children_punctuations)
# I need all the words to be the same.... to check with B
print('Total fails :', total_words_fails)
print('Total times of the game :', total_words_times)


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
    col+=1
    row = initial_row
    for f in c.fails:
        worksheet.write(row, col, f)
        row += 1
    col -= 2
    row += 1


# Finally, close the Excel file
# via the close() method.
workbook.close()
