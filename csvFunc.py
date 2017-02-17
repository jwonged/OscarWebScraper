import csv

outputFile = open('output.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
outputWriter.writerow(['row1','row2','row3'])
outputFile.close()
