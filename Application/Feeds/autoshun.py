import Database.dbmanagment as database
import urllib.request
import csv


description = """
    autoshun feeds,
    it gets all Intelligent from autoshon list,then insert database
    ->CSV is a simple file format used to store tabular data, such as a spreadsheet or database.
    Files in the CSV format can be imported to and exported from programs that store data in tables,
    such as Microsoft Excel or OpenOffice Calc.

    ->CSV stands for "comma-separated values". Its data fields are most often separated, or delimited, by a comma.

req = urllib.request.urlopen('https://www.autoshun.org/download/?api_key=d4066260862da9118d84717e17c0fc&format=csv')
data = req.read()
print(data)
# Write data to file
filename = "autoshun.csv"
file_ = open(filename, 'w')
file_.write(data)
file_.close()
"""




with open('report.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    result=[]
    for index,item in enumerate(readCSV):
        if item[0][0] =="#":
            print("Pass ")
        else:
            print(item[0],item[1],item[2])
            result.append(item)


    print(result)





