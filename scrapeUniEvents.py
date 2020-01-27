import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import *


def format_date(date_str):
    date_arr = date_str.split()
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month = str(months.index(date_arr[2]) + 1)
    day = date_arr[1][:-2]
    if len(month) < 2: month = f'0{month}'
    if len(day) < 2: day = f'0{day}'
    return f'{date_arr[3]}-{month}-{day}'


def format_time(time_str):
    t_arr = time_str.split('-')
    t1 = datetime.strptime(t_arr[0], '%I:%M%p')
    t2 = datetime.strptime(t_arr[1], '%I:%M%p')
    t1 = datetime.strftime(t1, '%H:%M')
    t2 = datetime.strftime(t2, '%H:%M')
    return f'{t1}-{t2}'


conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
c = conn.cursor()

base_url = 'https://www.liverpool.ac.uk/events'
response = requests.get(base_url+'/listing/?id=all')
soup = BeautifulSoup(response.text, 'html.parser')
main_content = soup.find('section', {'id': 'main-content'})
for link in main_content.findAll('a'):
    link_url = base_url+link['href'].strip('..')
    print(link_url)
    response = requests.get(link_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1', {'class': 'n'})
    date = soup.find('span', {'class': 'date'})
    timeFrom = soup.find('span', {'class': 'time-from'})
    timeTo = soup.find('span', {'class': 'time-to'})
    evtype = soup.find('span', {'class': 'event-type'})
    series = soup.find('span', {'class': 'event-series'})
    desc = soup.find('div', {'class': 'biography-information content'})

    name_text = ''
    soc_text = ''
    loc_text = ''
    type_text = ''
    desc_text = ''
    date_text = ''
    time_text = ''

    name_text = name.getText().strip().replace('\'', '’')
    if series is not None:
        soc_text = series.getText().strip()
    loc_text = 'University of liverpool'
    type_text = evtype.getText().strip()
    if desc is not None:
        desc_text = desc.getText().strip().replace('\'', '’')
    date_text = format_date(date.getText().strip())
    time_text = format_time(timeFrom.getText().strip()+'-'+timeTo.getText().strip())

    # if url not in events table...
    c.execute("SELECT COUNT(*) FROM events WHERE url = '%s';" % link_url)
    count = c.fetchall()[0][0]
    if count > 0:
        print('Skip adding this event...')
    else:
        print('Adding this event...')
        # c.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
        #           % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,link_url))
        # conn.commit()

        print('name: ' + name_text)
        print('society: ' + soc_text)
        print('location: ' + loc_text)
        print('type: ' + type_text)
        print('description: ' + desc_text)
        print('date: ' + date_text)
        print('time: ' + time_text)
        print('==========================================')
        print()

conn.close()


