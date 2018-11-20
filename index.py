from constants.index import *
from DAO.EventsDAO import *

import bottle
import pymongo


class Index:
    def __init__(self):
        self.collection = None

    # Create new database
    def _set_collection(self):
        connection_string = CONNECTION_STRING
        connection = pymongo.MongoClient(connection_string)
        database = connection.events
        collection = EventsDAO(database)

        self.collection = collection

    # Set routes
    def _set_routes(self):
        bottle.route('/', callback=self.read_index())
        bottle.route('/create', method='POST', callback=self.create_event())
        bottle.route('/delete', method='POST', callback=self.delete_event())

    # Create Method
    def create_event(self):
        date = bottle.request.forms.get('date')
        description = bottle.request.forms.get('description')
        lang = bottle.request.forms.get('lang')
        granularity = bottle.request.forms.get('granularity')

        self.collection.insert_event(date=date,
                                     description=description,
                                     lang=lang,
                                     granularity=granularity)
        bottle.redirect('/')

    # Read Method
    def read_index(self):
        file = open('./public/src/index.html', 'r')
        html = file.read().replace('\n', '')

        events = self.collection.find_events(page=1)

        return bottle.template(html, dict(events=events))

    # Delete Method
    def delete_event(self):
        event_id = bottle.request.forms.get('id')

        self.collection.remove_event(event_id=event_id)
        bottle.redirect('/')

    # Main
    def run(self):
        self._set_collection()
        self._set_routes()

        bottle.debug(True)
        bottle.run(host=HOST, port=PORT)


def main():
    index = Index()
    index.run()

if __name__ == '__main__':
    main()