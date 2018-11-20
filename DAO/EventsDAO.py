from bson import ObjectId

import constants.DAO


class EventsDAO:
    def __init__(self, database):
        self.database = database
        self.events = database.events

    # Handle read events
    def find_events(self, page=1):
        events = self.events.find()
            # .skip((page - 1) * constants.DAO.PAGINATION)\
            # .limit(constants.DAO.LIMIT)

        return events

    # Handle create new events data
    def insert_event(self, date, description, lang, granularity):
        event = {
            'date': date,
            'description': description,
            'lang': lang,
            'granularity': granularity
        }

        self.events.insert(event)

    # Handle delete an events data
    def remove_event(self, event_id):
        self.events.remove({"_id": ObjectId(event_id)})
