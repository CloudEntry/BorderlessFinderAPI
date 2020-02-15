from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sqlite3


def main(base_dir):
    conn = sqlite3.connect(f'{base_dir}/borderless_finder.db')
    c = conn.cursor()

    c.execute("SELECT url FROM events WHERE url like '%%%s%%';" % 'liverpoolguild')
    for row in c.fetchall():
        db_url = row[0]
        print(db_url)

        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument("--window-position=0,0")
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=r'/Users/jackgee/Downloads/chromedriver', options=options)
        driver.get(db_url)
        time.sleep(4)

        plain_text = driver.page_source
        soup = BeautifulSoup(plain_text, 'lxml')
        error_404 = soup.find('div', {'class', 'uc-page-not-found'})
        if error_404:
            print('Error 404')
            c.execute("DELETE FROM events WHERE url = '%s';" % db_url)
            conn.commit()

    conn.close()
