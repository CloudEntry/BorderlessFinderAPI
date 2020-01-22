import sqlite3


def add_event(name_text, soc_text, loc_text, type_text, desc_text, date_text, time_text, url_text):
    conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c = conn.cursor()
    desc_text = desc_text.strip()
    print(url_text)
    # if url not in events table...
    c.execute("SELECT COUNT(*) FROM events WHERE url = '%s';" % url_text)
    count = c.fetchall()[0][0]
    if count > 0:
        print('Skip adding this event...')
    else:
        c.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
                  % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,url_text))
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


name = ''
society = ''
location = ''
event_type = ''
description = ''
date = ''
time = ''
url = ''
add_event(name, society, location, event_type, description, date, time, url)
