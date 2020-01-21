import requests
import json

# --------------- EVENTBRITE ---------------------

token = 'Q4CHW6L7QOZM43BXXTMW'
response = requests.get('https://www.eventbriteapi.com/v3/categories',headers={'Authorization':'Bearer '+token})
data = response.json()
for cat in data['categories']:
    print(cat['name'])

# --------------- TICKETMASTER ---------------------

def getEvents(countryCode):
    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?countryCode='+countryCode+'&apikey=HPjeXcOHk8SD7UDbxTmEKo5Lu3IPB0Oe')
    data = response.json()
    for d in data['_embedded']['events']:
        print()
        print(d['name'])
        print(d['dates']['start']['localDate'] + ' ' + d['dates']['start']['localTime'])
        print(d['_embedded']['venues'][0]['name'] + ', ' + d['_embedded']['venues'][0]['postalCode'])

#getEvents('UK')
#getEvents('GB')
