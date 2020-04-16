import time

from geopy import geocoders
from langdetect import detect

from MeetupAPI.log import Log


class MeetupUpcomingEvents():
    def __init__(self,
                 access_token,
                 pages='all',
                 results_per_page=200,
                 maximum_num_results=10000,
                 city=None,
                 lat=None,
                 lon=None,
                 text=None,
                 topic_category=None,
                 min_num_attendees=None,
                 filter=None):

        # Find Upcoming Events
        # https://www.meetup.com/meetup_api/docs/find/upcoming_events/
        import requests

        self.logs = ['self.__init__']
        self.started = round(time.time())

        self.log('MeetupUpcomingEvents()')

        if not access_token:
            self.log('--> No ACCESS_TOKEN')
            self.log('--> return None')
            self.value = None

        else:

            self.value = []
            self.offset = 0
            self.num_of_unchanged_rounds = 0
            parameter = {
                'access_token': access_token,
                'sign': True,
                'page': results_per_page,
                'offset': self.offset
            }
            if city:
                gn = geocoders.GeoNames(username='meetupapi')
                parameter['lat'], parameter['lon'] = gn.geocode(city)[1]
            elif lat and lon:
                parameter['lat'] = lat
                parameter['lon'] = lon
            if text:
                parameter['text'] = text
            if topic_category:
                parameter['topic_category'] = topic_category
            self.response_json = ['']

            if pages == 'all':
                pages = 10000

            while pages >= self.offset and len(self.response_json) > 0:
                parameter['offset'] = self.offset

                self.response = requests.get('https://api.meetup.com/find/upcoming_events',
                                             params=parameter).json()
                self.offset += 1

                # check if events in response
                if not 'events' in self.response:
                    self.log('events not found in response. Ending loop')
                    self.log(self.response)
                    break

                # filter events further
                new_events = self.response['events']
                if filter:
                    if 'online_meetups' in filter:
                        new_events = [
                            x for x in new_events if self.event_is_online(x)]

                    if len([x for x in filter if 'lang:' in x]) > 0:
                        if type(filter) == str:
                            language = filter.split('lang:')[1]
                        else:
                            for entry in filter:
                                if 'lang:' in entry:
                                    language = entry.split('lang:')[1]
                                    break
                        new_events = [
                            x for x in new_events if detect(x['name']) == language]

                    if min_num_attendees:
                        new_events = [
                            x for x in new_events if x['yes_rsvp_count'] >= min_num_attendees]

                    if 'group_urls_only' in filter:
                        new_events_groups = []
                        for event in new_events:
                            if 'https://meetup.com/'+event['group']['urlname'] not in self.value and 'https://meetup.com/'+event['group']['urlname'] not in new_events_groups:
                                new_events_groups.append(
                                    'https://meetup.com/'+event['group']['urlname'])
                        new_events = new_events_groups

                self.previous_count = len(self.value)
                self.value += new_events
                self.value = self.value[:maximum_num_results]
                self.new_count = len(self.value)
                if self.previous_count == self.new_count:
                    self.num_of_unchanged_rounds += 1

                self.log('Collected {} {}'.format(len(self.value),
                                                  'groups' if 'group_urls_only' in filter else 'events'))

                if len(self.value) == maximum_num_results:
                    self.log('Collected maximum number of {}'.format(
                        'groups' if 'group_urls_only' in filter else 'events'))
                    break

                # see if 10 pages in a row num of results doesn't change
                if self.num_of_unchanged_rounds == 10:
                    self.log(
                        'Number of results isnt changing anymore. Exiting loop.')
                    break

                # add waiting to prevent meetup api limitation
                time.sleep(2)

    def event_is_online(self, event):
        trigger_urls = ['zoom.', 'meet.', 'skype.']
        trigger_words = ['Zoom', 'Google Meet', 'Jitsi',
                         'Google Hangout', 'Skype', 'video call', 'online meetup']

        if 'description' in event:
            for trigger in trigger_words:
                if trigger.lower() in event['description'].lower():
                    return True

        if 'how_to_find_us' in event:
            for trigger in trigger_urls:
                if trigger in event['how_to_find_us']:
                    return True

        return False

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
