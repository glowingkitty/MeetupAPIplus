import json
import os
import time

import requests

from MeetupAPI.log import Log
from MeetupAPI.meetup_functions.meetup_fields import MeetupFields


class Meetup(MeetupFields):
    def __init__(self,
                 group=None,
                 access_token=None,
                 access_token_valid_upto=None,
                 client_id=None,
                 client_secret=None,
                 redirect_uri=None,
                 default_space_name='',
                 default_space_address_street='',
                 default_space_address_zip='',
                 default_space_address_city='',
                 default_space_address_countrycode='',
                 default_space_how_to_find_us='',
                 default_space_timezonestring='America/Los_Angeles',
                 show_log=True,
                 test=False
                 ):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.group = group
        self.response = None

        self.access_token_input = access_token
        self.access_token_valid_upto = access_token_valid_upto
        # check if access token was not given and load from json in that case
        if not self.access_token_input:
            if os.path.exists('_setup/secrets.json'):
                with open('_setup/secrets.json') as json_file:
                    secrets = json.load(json_file)
                    self.access_token_input = secrets['MEETUP']['ACCESS_TOKEN']
                    self.access_token_valid_upto = secrets['MEETUP']['ACCESS_TOKEN_VALID_UPTO']
            elif os.path.exists('secrets.json'):
                with open('secrets.json') as json_file:
                    secrets = json.load(json_file)
                    self.access_token_input = secrets['MEETUP']['ACCESS_TOKEN']
                    self.access_token_valid_upto = secrets['MEETUP']['ACCESS_TOKEN_VALID_UPTO']

        self.client_id = client_id
        self.client_secret = client_secret,
        self.redirect_uri = redirect_uri

        self.default_space_name = default_space_name
        self.default_space_address = {
            "STREET": default_space_address_street,
            "ZIP": default_space_address_zip,
            "CITY": default_space_address_city,
            "COUNTRYCODE": default_space_address_countrycode,
        }
        self.default_space_how_to_find_us = default_space_how_to_find_us
        self.default_space_timezonestring = default_space_timezonestring

        self.help = 'https://www.meetup.com/meetup_api/docs/'
        self.test = test

    @property
    def access_token(self):
        if hasattr(self, 'access_token_value'):
            return self.access_token_value

        from MeetupAPI.meetup_functions.access_token import MeetupAcessToken
        self.access_token_value, self.access_token_valid_upto = MeetupAcessToken(
            self.access_token_input,
            self.access_token_valid_upto,
            self.client_id,
            self.client_secret,
            self.redirect_uri).value
        return self.access_token_value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def group_details(self, group_url):
        from MeetupAPI.meetup_functions.group import MeetupGroup
        return MeetupGroup(group_url).value

    def upcoming_events(self,
                        pages='all',
                        results_per_page=200,
                        maximum_num_results=10000,
                        city=None,
                        lat=None,
                        lon=None,
                        text=None,
                        topic_category=None,
                        min_num_attendees=None,
                        max_num_of_unchanged_rounds=10,
                        filter=None,
                        fields=[
                            'event_hosts',
                            'featured',
                            'group_category',
                            'group_key_photo',
                            'group_photo',
                            'group_topics',
                            'how_to_find_us',
                            'group_join_info',
                            'group_membership_dues']
                        ):
        from MeetupAPI.meetup_functions.upcoming_events import MeetupUpcomingEvents
        return MeetupUpcomingEvents(
            self.access_token,
            pages,
            results_per_page,
            maximum_num_results,
            city,
            lat,
            lon,
            text,
            topic_category,
            min_num_attendees,
            max_num_of_unchanged_rounds,
            filter,
            fields
        ).value

    def events(self,
               results_per_page=200,
               pages='all',
               maximum_num_results=10000,
               fields=['group_key_photo', 'series',
                       'simple_html_description', 'rsvp_sample']
               ):
        from MeetupAPI.meetup_functions.events import MeetupEvents
        return MeetupEvents(self, results_per_page,
                            pages, maximum_num_results, fields).value

    def create(self, event, announce=False, publish_status='draft'):
        from MeetupAPI.meetup_functions.create import MeetupCreate
        return MeetupCreate(self.access_token, self.group, event, announce, publish_status, self.default_space_how_to_find_us).value

    def delete(self, event):
        from MeetupAPI.meetup_functions.delete import MeetupDelete
        return MeetupDelete(self.access_token, self.group, event).value

    def message(self,
                receiver_members,
                message,
                json_placeholders=[],
                save_log=True,
                log_path='sent_messages_log.json',
                spam_prevention=True,
                spam_prevention_wait_time_minutes=1440,
                test=False,
                auto_close_selenium=True,
                scraper=None
                ):
        from MeetupAPI.meetup_functions.message import MeetupMessage
        return MeetupMessage(receiver_members, message, json_placeholders, save_log, log_path, spam_prevention, spam_prevention_wait_time_minutes, test, auto_close_selenium, scraper).value

    def message_group_organizer(self,
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
        from MeetupAPI.meetup_functions.message_group_organizer import MeetupMessageGroupOrganizer
        return MeetupMessageGroupOrganizer(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            messages=messages,
            messages_paths=messages_paths,
            cities=cities,
            cities_processed_path=cities_processed_path,
            maximum_num_results=maximum_num_results,
            filters=filters
        ).value
