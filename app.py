#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
from datetime import datetime
import sqlite3


app = Flask(__name__)
CORS(app)


@app.route('/api/v1.0/events', methods=['GET'])
def get_events():
    events = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')  # /home/borderlessfinder/borderless_finder.db
    c = conn.cursor()
    c.execute("SELECT * FROM events order by date, time;")
    # select name, society, date, time, location, type, replace(description,X'0A',' '), url from events
    for row in c.fetchall():
        events.append({'id': row[0],
                       'name': row[1],
                       'society': row[2],
                       'location': row[3],
                       'type': row[4],
                       'description': row[5],
                       'date': row[6],
                       'time': row[7],
                       'url': row[8],
                       'creator': row[9],
                       'tickets_remaining': row[10]})
    return jsonify({'events': events})


@app.route('/api/v1.0/searchevents/<search_text>', methods=['GET'])
def search_events(search_text):
    events = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    query = "SELECT * FROM events where name like '%%%s%%' or society like '%%%s%%' or description like '%%%s%%' order by date, time;" % (search_text, search_text, search_text)
    c.execute(query)
    for row in c.fetchall():
        event = {'id': row[0],
                 'name': row[1],
                 'society': row[2],
                 'location': row[3],
                 'type': row[4],
                 'description': row[5],
                 'date': row[6],
                 'time': row[7],
                 'url': row[8],
                 'creator': row[9]}
        events.append(event)
    return jsonify({'events': events})


@app.route('/api/v1.0/eventscount', methods=['GET'])
def get_events_count():
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    c.execute("select count(id) from events where date >= date('%s');" % today)
    count = c.fetchone()[0]
    return jsonify({'count': count})


@app.route('/api/v1.0/events/info/<int:event_id>', methods=['GET'])
def get_event_detail(event_id):
    event_detail = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT id, name, society, location, type, date, time, url, description FROM events where id = %s;" % str(event_id))
    # select name, society, date, time, location, type, replace(description,X'0A',' '), url from events
    row = c.fetchone()
    event_detail.append({'id': row[0],
                         'name': row[1],
                         'society': row[2],
                         'location': row[3],
                         'type': row[4],
                         'date': row[5],
                         'time': row[6],
                         'url': row[7],
                         'lat': u'53.406566',
                         'lon': u'-2.966531',
                         'description': row[8]})
    conn.close()
    return jsonify({'event': event_detail[0]})


@app.route('/api/v1.0/events', methods=['POST'])
def create_event():
    if not request.json:    # or not 'name' in request.json:
        abort(400)
    # insert into database
    conn2 = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c2 = conn2.cursor()
    name_text = request.json['name']
    soc_text = request.json.get('society', "")
    loc_text = request.json.get('location', "")
    link_url = request.json.get('url', "")
    type_text = request.json.get('type', "")
    desc_text = request.json.get('description', "")
    date_text = request.json.get('date', "")
    time_text = request.json.get('time', "")
    creator_text = request.json.get('u_email', "")
    tickets = request.json.get('tickets')
    if tickets:
        c2.execute("INSERT INTO events(name,society,location,type,description,date,time,url,creator,tickets_remaining) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s','%s',%s);" \
                   % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,link_url,creator_text,tickets))
    else:
        c2.execute("INSERT INTO events(name,society,location,type,description,date,time,url,creator) VALUES ('%s','%s','%s','%s','%s',date('%s'),'%s','%s','%s');" \
                   % (name_text,soc_text,loc_text,type_text,desc_text,date_text,time_text,link_url,creator_text))
    conn2.commit()
    conn2.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/deleteevent', methods=['POST'])
def delete_event():
    if not request.json:
        abort(400)
    conn2 = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c2 = conn2.cursor()
    e_id = request.json['e_id']
    c2.execute("DELETE FROM events WHERE id = %s;" % e_id)
    conn2.commit()
    conn2.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/events/<u_email>', methods=['GET'])
def get_created_events(u_email):
    events = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events where creator = '%s' order by date, time;" % u_email)
    for row in c.fetchall():
        events.append({'id': row[0],
                       'name': row[1],
                       'society': row[2],
                       'location': row[3],
                       'type': row[4],
                       'description': row[5],
                       'date': row[6],
                       'time': row[7],
                       'url': row[8],
                       'lat': u'53.406566',
                       'lon': u'-2.966531',
                       'tickets_remaining': row[10]})
    conn.close()
    return jsonify({'events': events})


@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    users = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users;")
    id_num = 0
    for row in c.fetchall():
        id_num += 1
        users.append({'id': id_num,
                      'email': row[0],
                      'fname': row[1],
                      'sname': row[2],
                      'pword': row[3],
                      'acc_type': row[4],
                      'age': row[5],
                      'gender': row[6],
                      'ethnicity': row[7],
                      'major': row[8],
                      'frequency': row[9],
                      'saved_events': row[10],
                      'organizer_freq': row[11],
                      'organizer_event_type': row[12],
                      'aca_exp': row[13],
                      'art_exp': row[14],
                      'bus_exp': row[15],
                      'cha_exp': row[16],
                      'dan_exp': row[17],
                      'gam_exp': row[18],
                      'cul_exp': row[19],
                      'mus_exp': row[20],
                      'pol_exp': row[21],
                      'rel_exp': row[22],
                      'soc_exp': row[23],
                      'spo_exp': row[24],
                      'tra_exp': row[25]})
    conn.close()
    return jsonify({'users': users})


@app.route('/api/v1.0/user/<email>', methods=['GET'])
def login(email):
    user = {}
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = '%s';" % str(email))
    for row in c.fetchall():
        user = {'email': row[0],
                'fname': row[1],
                'sname': row[2],
                'pword': row[3],
                'acc_type': row[4],
                'age': row[5],
                'gender': row[6],
                'ethnicity': row[7],
                'major': row[8],
                'frequency': row[9],
                'saved_events': row[10]}
    conn.close()
    return jsonify({'user': user})


@app.route('/api/v1.0/users', methods=['POST'])
def create_users():
    conn2 = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c2 = conn2.cursor()
    email = request.json['email']
    fname = request.json['fname']
    sname = request.json['sname']
    pword = request.json['pword']
    acc_type = request.json['acc_type']
    age = request.json['age']
    gender = request.json['gender']
    ethnicity = request.json['ethnicity']
    major = request.json['major']
    frequency = request.json['frequency']
    o_freq = request.json['o_freq']
    o_type = request.json['o_type']
    # soc_admin_text = ''
    # if email.endswith('@society.liverpoolguild.org'):
    #     soc_admin_text = email.split('@')[0]
    c2.execute("INSERT INTO users(email,fname,sname,pword,acc_type,age,gender,ethnicity,major,frequency,organizer_freq,organizer_event_type) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" \
               % (email, fname, sname, pword, acc_type, age, gender, ethnicity, major, frequency, o_freq, o_type))
    conn2.commit()
    conn2.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/timetable/<c_code>', methods=['GET'])
def get_timetable(c_code):
    timetable = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT title, date, time, location FROM lecture_timetable where c_code = '%s' order by date, time;" % c_code)
    id_num = 0
    for row in c.fetchall():
        id_num += 1
        timetable.append({'id': id_num,
                       'title': row[0],
                       'date': row[1],
                       'time': row[2],
                       'location': row[3]})
    return jsonify({'timetable': timetable})


@app.route('/api/v1.0/saveevent', methods=['POST'])
def save_event():
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    u_email = request.json['u_email']
    e_id = request.json['e_id']
    c.execute("select tickets_remaining from events where id = %s" % e_id)
    tickets_remaining = c.fetchone()[0]
    if tickets_remaining is not None:
        if tickets_remaining > 0:
            c.execute("SELECT saved_events FROM users where email = '%s';" % u_email)
            saved_events = c.fetchone()[0]
            if saved_events:
                if e_id in saved_events.split(','):
                    new_events = saved_events
                else:
                    new_events = saved_events + ',' + e_id
            else:
                new_events = e_id
            c.execute("UPDATE users SET saved_events = '%s' WHERE email = '%s';" % (new_events, u_email))
            conn.commit()
            conn.close()
            return jsonify({'successful': "yes"}), 201
        else:
            conn.close()
            return jsonify({'successful': "no"}), 201
    else:
        c.execute("SELECT saved_events FROM users where email = '%s';" % u_email)
        saved_events = c.fetchone()[0]
        if saved_events:
            new_events = saved_events + ',' + e_id
        else:
            new_events = e_id
        c.execute("UPDATE users SET saved_events = '%s' WHERE email = '%s';" % (new_events, u_email))
        conn.commit()
        conn.close()
        return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/savedevents/<u_email>', methods=['GET'])
def get_saved_events(u_email):
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT saved_events FROM users where email = '%s';" % u_email)
    row = c.fetchone()
    saved_events = row[0]
    conn.commit()
    conn.close()
    return jsonify({'saved_events': saved_events}), 201


@app.route('/api/v1.0/removesavedevent', methods=['POST'])
def remove_saved_event():
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    u_email = request.json['u_email']
    e_id = request.json['e_id']
    c.execute("SELECT saved_events FROM users where email = '%s';" % u_email)
    row = c.fetchone()
    saved_events = row[0].split(',')
    saved_events.remove(str(e_id))
    new_se_str = ','.join(saved_events)
    c.execute("UPDATE users SET saved_events = '%s' WHERE email = '%s';" % (new_se_str, u_email))
    conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/decrementtickets', methods=['POST'])
def decrement_event_tickets():
    if not request.json:
        abort(400)
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    e_id = request.json['e_id']
    c.execute("select tickets_remaining FROM events WHERE id = %s;" % e_id)
    tickets = c.fetchone()[0]
    if tickets and tickets > 0:
        tickets = tickets - 1
        c.execute("UPDATE events SET tickets_remaining = %s WHERE id = %s;" % (tickets, e_id))
        conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/incrementtickets', methods=['POST'])
def increment_event_tickets():
    if not request.json:
        abort(400)
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    e_id = request.json['e_id']
    c.execute("select tickets_remaining FROM events WHERE id = %s;" % e_id)
    tickets = c.fetchone()[0]
    if tickets:
        tickets = tickets + 1
        c.execute("UPDATE events SET tickets_remaining = %s WHERE id = %s;" % (tickets, e_id))
        conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/changepassword', methods=['POST'])
def change_password():
    if not request.json:
        abort(400)
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    email = request.json['email']
    new_pword = request.json['new_pword']
    c.execute("update users set pword = '%s' where email = '%s';" % (new_pword, email))
    conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/deleteaccount', methods=['POST'])
def delete_account():
    if not request.json:
        abort(400)
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    email = request.json['email']
    c.execute("delete from users where email = '%s';" % email)
    conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/messages', methods=['GET'])
def get_messages():
    messages = []
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages order by date, time;")
    for row in c.fetchall():
        messages.append({'id': row[0],
                         'email': row[1],
                         'type': row[2],
                         'message': row[3],
                         'date': row[4],
                         'time': row[5]})
    return jsonify({'messages': messages})


@app.route('/api/v1.0/messages', methods=['POST'])
def create_message():
    if not request.json:
        abort(400)
    # insert into database
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    email_text = request.json.get('email', "")
    type_text = request.json.get('type', "")
    message_text = request.json.get('message', "")
    date_url = request.json.get('date', "")
    time_text = request.json.get('time', "")
    c.execute("INSERT INTO messages(email,type,message,date,time) VALUES ('%s','%s','%s',date('%s'),'%s');"
              % (email_text, type_text, message_text, date_url, time_text))
    conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.route('/api/v1.0/incrementexp', methods=['POST'])
def increment_exp(email, skill, exp):
    if not request.json:
        abort(400)
    conn = sqlite3.connect('/home/borderlessfinder/borderless_finder.db')
    c = conn.cursor()
    email = request.json['email']
    skill = request.json['skill']
    exp = request.json['exp']
    c.execute("select %s_exp FROM users WHERE email = %s;" % (skill, email))
    c_exp = c.fetchone()[0]
    c_exp = c_exp + exp
    c.execute("UPDATE users SET %s_exp = %s WHERE email = %s;" % (skill, c_exp, email))
    conn.commit()
    conn.close()
    return jsonify({'successful': "yes"}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
