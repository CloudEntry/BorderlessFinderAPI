import sqlite3
from time import strptime


def convertDate(ds):
    print(ds)
    month = ds.split()[2][:3]
    month = strptime(month, '%b').tm_mon
    date = ds.split()[1][:-2]
    year = ds.split()[-1]
    print(str(date) + '/' + str(month) + '/' + str(year))


conn = sqlite3.connect('/Users/jackgee/Desktop/events.db')
c = conn.cursor()
c.execute("SELECT date FROM event;")
for date in c.fetchall():
    convertDate(date[0])
