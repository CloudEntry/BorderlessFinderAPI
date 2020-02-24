import scrapeSocEvents as soc
import scrapeDepartmentEvents as dep
import scrapeUniEvents as uni
import updateEvents as update
import removeDeadLinks as remDL
import sqlite3
import os
import shutil
from datetime import datetime

base_dir = '/Users/jackgee/Desktop'

# perform backup
today = datetime.today().strftime('%Y-%m-%d')
os.mkdir(f'{base_dir}/backup-{today}')
shutil.copy2(f'{base_dir}/borderless_finder.db', f'{base_dir}/backup-{today}')
if os.path.exists(f'{base_dir}/events.txt'):
    shutil.copy2(f'{base_dir}/events.txt', f'{base_dir}/backup-{today}')

# remove old txt and excel files
if os.path.exists(f'{base_dir}/events.txt'):
    os.remove(f'{base_dir}/events.txt')

# fetch new events, remove dead links and update detail changes in db
soc.main(base_dir)
dep.main(base_dir)
uni.main(base_dir)
try:
    remDL.main(base_dir)
except:
    pass
try:
    update.main(base_dir)
except:
    pass

# output new text file
conn = sqlite3.connect(f'{base_dir}/borderless_finder.db')
c = conn.cursor()
c.execute("select name, society, date, time, location, type, replace(description,X'0A',' '), url from events order by date;")
f = open(f"{base_dir}/events.txt", "w")
f.write("name|society|date|time|location|type|description|url\n")
for row in c.fetchall():
    f.write(f'{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}\n')
f.close()
