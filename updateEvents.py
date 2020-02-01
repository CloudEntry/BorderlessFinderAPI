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

    # url_location
    url_location = soup.find('span', {'class': 'eventVenue'}).getText().strip().replace('\'', '’')

    dateTimeStr = soup.find('span', {'class': 'eventDateTime'}).getText().strip()
    dtarr = dateTimeStr.split()
    datearr = dtarr[1].split('-')

    # url_date
    url_date = f'{datearr[2]}-{datearr[1]}-{datearr[0]}'

    # url_time
    url_time = dtarr[3]+'-'+dtarr[-1]

    # if url not in events table...
    c.execute("SELECT time, date, location FROM events WHERE url = '%s';" % eventUrl)
    for row in c.fetchall():
        db_time = row[0]
        db_date = row[1]
        db_location = row[2]

    if db_location != url_location:
        print(f'db_location = {db_location}, url_location = {url_location},')
        c.execute("UPDATE events SET location = '%s' where url = '%s';" % (url_location, eventUrl))
        conn.commit()

    if db_date != url_date:
        print(f'db_date = {db_date}, url_date = {url_date},')
        c.execute("UPDATE events SET date = date('%s') where url = '%s';" % (url_date, eventUrl))
        conn.commit()

    if db_time != url_time:
        print(f'db_time = {db_time}, url_time = {url_time},')
        c.execute("UPDATE events SET time = '%s' where url = '%s';" % (url_time, eventUrl))
        conn.commit()


conn.close()
