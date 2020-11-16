import xlsxwriter

# I create the csv:
workbook = xlsxwriter.Workbook('B.xlsx')
worksheet = workbook.add_worksheet()

# Invent the data first:
children_names = ['Paco', 'Pepe', 'Bea', 'Rubén', 'María']
words = ["galdiolo", "flor", "palmera", "bloso", "adrono", "furta", "tractor",
         "parque", "abarzar", "tornillo", "aporbar", "falda", "plamera"]
children_fails = [12, 4, 16, 3, 5, 2, 0, 2, 3, 5, 6, 8, 12]
children_times = [12, 34, 54, 63, 12, 34, 66, 21, 65, 56, 32, 23]

#Format the document:
worksheet.write('B1', 'Children Names') 
worksheet.write('C1', 'Max Time on respons ') 
row = 1
col = 1
# Save the data:
for index, c in enumerate(children_names):
    worksheet.write(row, col, c)
    worksheet.write(row, col+1, children_times[index])
    row+=1
    
for index, c in enumerate(children_names):
    worksheet.write(row, col, c)
    worksheet.write(row, col+1, children_times[index])
    row+=1
# Finally, close the Excel file
# via the close() method.
workbook.close()
