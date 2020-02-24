import sqlite3


def add_event(name_text, soc_text, loc_text, type_text, desc_text, date_text, time_text, url_text):
    conn = sqlite3.connect('/Users/jackgee/Desktop/event-data/borderless_finder.db')
    c = conn.cursor()
    desc_text = desc_text.strip()
    print(url_text)
    # if url not in events table...
    # c.execute("SELECT COUNT(*) FROM events WHERE url = '%s';" % url_text)
    # count = c.fetchall()[0][0]
    # if count > 0:
    #     print('Skip adding this event...')
    # else:
    # c.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
    #           % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,url_text))
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


name = 'Make a Game in 2 Hours'
society = 'Game Developers Society'
location = 'Elizabeth Gidney Room, The Guild'
event_type = 'Society Taster Session'
description = '''
Follow along as we guide you through an interactive experience developing a short, creative, and fun puzzle game in GB Studio! You’ll be able to help decide on key aspects of the game, as well as have the chance to design your own levels! If you want to try following along and developing your own game idea as well, the software is free to download and we’ll be happy to try and help you out too.
'''
date = '2020-02-03'
time = '18:30-20:30'
url = 'https://www.eventbrite.co.uk/e/make-a-game-in-2-hours-tickets-91664046631'
add_event(name, society, location, event_type, description, date, time, url)
