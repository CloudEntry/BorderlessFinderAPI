import requests
from bs4 import BeautifulSoup
import sqlite3


def format_date(date_str):
    date_arr = date_str.split()
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month = str(months.index(date_arr[2]) + 1)
    day = date_arr[1]
    if len(month) < 2: month = f'0{month}'
    if len(day) < 2: day = f'0{day}'
    return f'{date_arr[3]}-{month}-{day}'


def format_time(time_str):
    t_arr = time_str.split()
    t1 = t_arr[0]
    t2 = t_arr[2]
    return f'{t1}-{t2}'


def get_all_links(isoup, div_class):
    all_links = []
    base_url = 'https://www.liverpool.ac.uk'
    for section in isoup.findAll('section', {'class': div_class}):
        link_url = base_url + section.find('a')['href']
        iresponse = requests.get(link_url)
        soup2 = BeautifulSoup(iresponse.text, 'html.parser')
        sublinks = []
        for subsection in soup2.findAll('section', {'class': 'generic-promo clearfix'}):
            linkurl = subsection.find('a')['href']
            sublinks.append(linkurl)
        if len(sublinks) < 1:
            all_links.append(link_url)
        else:
            for link in sublinks:
                all_links.append(link)
    return all_links


def main(base_dir):
    conn = sqlite3.connect(f'{base_dir}/borderless_finder.db')
    c = conn.cursor()

    base_url = 'https://www.liverpool.ac.uk'
    arts_url = base_url + '/arts/events/'
    response = requests.get(arts_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links_list = []
    first_links = get_all_links(soup, 'generic-promo clearfix')
    second_links = get_all_links(soup, 'generic-promo extra-emphasis department-cent-promo department-right-promo department-extra-cent-promo department-extra-right-promo color-base clearfix')
    for l1 in first_links:
        links_list.append(l1)
    for l2 in second_links:
        links_list.append(l2)

    for linko in links_list:

        name_text = ''
        soc_text = ''
        loc_text = ''
        type_text = ''
        desc_text = ''
        date_text = ''
        time_text = ''
        url_text = linko

        print(linko)
        lresponse = requests.get(linko)
        lsoup = BeautifulSoup(lresponse.text, 'html.parser')

        if linko.split('.')[1] == 'eventbrite':
            name_text = lsoup.find('h1', {'class': 'listing-hero-title'}).getText().strip().replace('\'', '’')
            soc_text = lsoup.find('a', {'class': 'js-d-scroll-to listing-organizer-name text-default'}).getText().strip().strip('by ')
            loc_text = lsoup.findAll('div', {'class': 'event-details__data'})[1].findAll('p')[0].getText().strip()
            # postcode = lsoup.findAll('div', {'class': 'event-details__data'})[1].findAll('p')[4].getText()
            type_text = 'Eventbrite'
            desc = lsoup.find('div', {'class': 'structured-content-rich-text structured-content__module l-align-left l-mar-vert-6 l-sm-mar-vert-4 text-body-medium'}).findAll('p')
            for d in desc:
                desc_text += f'{d.text.strip()}\n'
            desc_text = desc_text.strip().replace('\'', '’')
            dateStr = lsoup.findAll('div', {'class': 'event-details__data'})[0].findAll('p')[0].getText().strip()
            date_text = format_date(dateStr)
            timeStr = lsoup.findAll('div', {'class': 'event-details__data'})[0].findAll('p')[1].getText().strip()
            time_text = format_time(timeStr)

            # if url not in events table...
            c.execute("SELECT COUNT(*) FROM events WHERE url = '%s';" % linko)
            count = c.fetchall()[0][0]
            if count > 0:
                print('Skip adding this event...')
            else:
                print('Adding this event...')
                c.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
                          % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,linko))
                conn.commit()

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


