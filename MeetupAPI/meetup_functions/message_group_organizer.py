import json
import os
import random
import sys
import time

from MeetupAPI.log import Log


class MeetupMessageGroupOrganizer():
    def __init__(self,
                 client_id,
                 client_secret,
                 redirect_uri,
                 messages=None,
                 messages_paths='message_to_organizer.txt',
                 cities=[
                     'San Francisco, CA',
                     'Los Angeles, CA',
                     'New York, NY',
                     'Seattle, WA',
                     'Boston, MA',
                     'Chicago, IL',
                     'Detroit, Michigan',
                     'Washington, DC',
                     'Miami, FL',
                     'Toronto, Canada',
                     'Barcelona, Spain',
                     'Madrid, Spain',
                     'Paris, France',
                     'Rome, Italy',
                     'Milano, Italy',
                     'London, UK',
                     'Berlin, Germany',
                     'Munich, Germany',
                     'Vienna, Austria',
                     'Amsterdam, Netherlands',
                     'Singapore, Singapore',
                     'Hong Kong, Hong Kong',
                     'Tokyo, Japan',
                     'Seoul, South Korea'
                 ],
                 cities_processed_path='processed_cities.json',
                 maximum_num_results=20,
                 filters=['online_meetups', 'lang:en']
                 ):
        from MeetupAPI.meetup import Meetup

        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.cities_processed_path = cities_processed_path
        self.message = None
        self.message_path = None

        self.messages = messages
        self.messages_paths = messages_paths

        self.log('MeetupMessageGroupOrganizer()')

        # check if client_id etc. are given
        if not (client_id and client_secret and redirect_uri):
            self.log(
                'ERROR: Meetup() required client_id, client_secret and redirect_uri')
            self.value = False

        else:
            self.meetup_class = Meetup(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri
            )

            # select message
            self.select_message()

            if self.message:
                for city in cities:
                    # check if city is already on the json file list of processed cities, if not, send messages
                    if self.city_processed(city):
                        self.log(
                            '{} already processed. Process next city...'.format(city))

                    else:
                        self.log('Get groups for {} ...'.format(city))
                        group_organizer = self.meetup_class.upcoming_events(
                            city=city,
                            maximum_num_results=maximum_num_results,
                            filter=filters+['group_organizer_only']
                        )

                        self.log(
                            'Send messages to group organizers in {}'.format(city))
                        scraper = None
                        for organizer in group_organizer:
                            success, scraper = self.meetup_class.message(
                                receiver_members=organizer,
                                message=self.message,
                                json_placeholders=[{
                                    'keyword': 'organizer_name',
                                    'replace_with': organizer['name']
                                }],
                                auto_close_selenium=False,
                                scraper=scraper
                            )

                            if success:
                                time.sleep(random.randint(10, 20))

                                # select message for next receiver
                                self.select_message()

                            else:
                                self.log(
                                    'Failed to send message. Canceled script')
                                sys.exit()

                        # save city as processed
                        self.cities_processed.insert(0, city)
                        with open(self.cities_processed_path, 'w') as outfile:
                            json.dump(self.cities_processed, outfile, indent=4)

    def city_processed(self, city):
        if os.path.exists(self.cities_processed_path):
            with open(self.cities_processed_path, 'r') as json_file:
                self.cities_processed = json.load(json_file)

                if city in self.cities_processed:
                    return True

        else:
            self.cities_processed = []

        return False

    def select_message(self):
        # if multiple messages or message paths, randomly choose one
        if self.messages:
            if type(self.messages) == list:
                random_num = random.randint(0, len(self.messages)-1)
                self.message = self.messages[random_num]
            else:
                self.message = self.messages
        else:
            if type(self.messages_paths) == list:
                random_num = random.randint(0, len(self.messages_paths)-1)
                self.message_path = self.messages_paths[random_num]
            else:
                self.message_path = self.messages_paths

        # get message, from path or input
        if not self.message and not os.path.isfile(self.message_path):
            self.log(
                'ERROR: You havent defined a message. Use the "message" or the "message_path" input to define a message.')
            self.value = False

        elif not self.message and os.path.isfile(self.message_path):
            with open(self.message_path, 'r') as fh:
                self.message = fh.read()

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
