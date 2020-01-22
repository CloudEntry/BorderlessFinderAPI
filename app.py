#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import sqlite3
from time import strptime

app = Flask(__name__)


@app.route('/api/v1.0/events', methods=['GET'])
def get_events():
    events = []
    conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT name, society, location, type, date, time FROM events;")
    # select name, society, date, time, location, type, replace(description,X'0A',' '), url from events
    id_num = 0
    for row in c.fetchall():
        id_num += 1
        events.append({'id': id_num,
                       'name': row[0],
                       'society': row[1],
                       'location': row[2],
                       'type': row[3],
                       'date': row[4],
                       'time': row[5]})
    return jsonify({'events': events})


@app.route('/api/v1.0/events/info/<int:event_id>', methods=['GET'])
def get_event_detail(event_id):
    event_detail = []
    conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT url, description FROM events where rowid = %s;" % str(event_id))
    # select name, society, date, time, location, type, replace(description,X'0A',' '), url from events
    row = c.fetchone()
    event_detail.append({'url': row[0], 'lat': u'53.406566', 'lon': u'-2.966531', 'description': row[1]})
    conn.close()
    return jsonify({'event': event_detail[0]})


@app.route('/api/v1.0/events', methods=['POST'])
def create_event():
    if not request.json:    # or not 'name' in request.json:
        abort(400)
    # insert into database
    conn2 = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c2 = conn2.cursor()
    name_text = request.json['name']
    soc_text = request.json.get('society', "")
    loc_text = request.json.get('location', "")
    type_text = request.json.get('type', "")
    desc_text = request.json.get('description', "")
    date_text = request.json.get('date', "")
    time_text = request.json.get('time', "")
    link_url = "test123"
    c2.execute("INSERT INTO events(name,society,location,type,description,date,time,url) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s');" \
               % (name_text, soc_text, loc_text, type_text, desc_text, date_text, time_text, link_url))
    conn2.commit()
    conn2.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    users = []
    conn = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users;")
    id_num = 0
    for row in c.fetchall():
        id_num += 1
        users.append({'id': id_num,
                      'email': row[0],
                      'password': row[1],
                      'first_name': row[2],
                      'surname': row[3],
                      'society_admin': row[4]})
    conn.close()
    return jsonify({'users': users})


@app.route('/api/v1.0/users', methods=['POST'])
def create_users():
    conn2 = sqlite3.connect('/Users/jackgee/Desktop/borderless_finder.db')
    c2 = conn2.cursor()
    email_text = request.json['email']
    password_text = request.json['password']
    first_name_text = request.json['first_name']
    surname_text = request.json['surname']
    soc_admin_text = ''
    if email_text.endswith('@society.liverpoolguild.org'):
        soc_admin_text = email_text.split('@')[0]
    c2.execute("INSERT INTO user(email,password,first_name,surname,society_admin) VALUES ('%s','%s','%s','%s','%s');" \
               % (email_text, password_text, first_name_text, surname_text, soc_admin_text))
    conn2.commit()
    conn2.close()
    return jsonify({'successful': "yes"}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
