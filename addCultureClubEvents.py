import sqlite3

conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
c = conn.cursor()

thursdays = ['2020-01-30','2020-02-06','2020-02-13','2020-02-20','2020-02-27','2020-03-05','2020-03-12','2020-03-19', \
             '2020-03-26','2020-04-23','2020-04-30','2020-05-07']
for t in thursdays:
    name_text = 'Culture Club Session'
    soc_text = 'The Culture Club'
    loc_text = 'The Language Lounge, Abercromby Square'
    type_text = 'Language and Culture'
    desc_text = '''
    Sessions are facilitated by trained leaders and are open to Home/EU and international students.
    Come and join us to:
    • improve your English
    • learn more about different interesting subjects that will help with your studies
    • familiarise yourself with the British culture
    • make new international friends. 
    Sessions will take place every Thursday 5-6 pm during term time in the Language Lounge, Abercromby Square
    For info please contact artssa@liverpool.ac.uk or franco.zappettini@liverpool.ac.uk specifying if you are interested in attending or leading a class.
    '''
    desc_text = desc_text.strip()
    date_text = t
    time_text = '17:00-18:00'
    url_text = 'https://www.liverpool.ac.uk/arts/events/culture-club/'

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
