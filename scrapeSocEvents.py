from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
c = conn.cursor()

url = 'https://www.liverpoolguild.org/events?event_type=&search='

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--window-position=0,0")
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'/Users/jackgee/Downloads/chromedriver', options=options)
driver.get(url)
time.sleep(5)

while True:
    try:
        loadMoreButton = driver.find_element_by_xpath("//div[contains(@id,'load-more-events')]")
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        break

plain_text = driver.page_source
soup = BeautifulSoup(plain_text, 'lxml')
for event in soup.findAll('a', {'class': 'event-box'}):
    eventUrl = 'https://www.liverpoolguild.org'+event['href']
    print(eventUrl)
    driver.get(eventUrl)
    time.sleep(5)
    plain_text = driver.page_source
    soup = BeautifulSoup(plain_text, 'lxml')

    name_text = soup.find('h2').getText().strip().replace('\'', '’')
    soc_text = soup.find('div', {'class': 'title'}).find('h1').getText().strip().replace('\'', '’')
    loc_text = soup.find('span', {'class': 'eventVenue'}).getText().strip().replace('\'', '’')
    type_text = 'Society event'
    desc_text = ''
    for p in soup.find('div', {'class': 'contentBoxes'}).findAll('p'):
        desc_text += p.getText().strip().replace('\'', '’')

    dateTimeStr = soup.find('span', {'class': 'eventDateTime'}).getText().strip()
    dtarr = dateTimeStr.split()
    datearr = dtarr[1].split('-')
    date_text = f'{datearr[2]}-{datearr[1]}-{datearr[0]}'
    time_text = dtarr[3]+'-'+dtarr[-1]

    # if url not in events table...
    c.execute("SELECT COUNT(*) FROM events WHERE url = '%s';" % eventUrl)
    count = c.fetchall()[0][0]
    if count > 0:
        print('Skip adding this event...')
    else:
        print('Adding this event...')
        # c.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
        #           % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,eventUrl))
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





    # day = dtarr[0]
    # date = int(dtarr[1].split('-')[0])
    # if date < 10:
    #     dateStr = str(date).strip('0')
    # else:
    #     dateStr = str(date)
    # if date == 1:
    #     letters = 'st'
    # elif date == 2:
    #     letters = 'nd'
    # else:
    #     letters = 'th'
    # months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    # monthNum = int(dtarr[1].split('-')[1])
    # month = months[monthNum - 1]
    # year = dtarr[1].split('-')[2]
    # date_text = day + ' ' + dateStr + letters + ' ' + month + ' ' + year
