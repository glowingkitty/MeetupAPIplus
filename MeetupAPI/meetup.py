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
                 test=False):
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

        self.setup_done = True if group or (access_token and access_token_valid_upto) or (
            client_id and client_secret and redirect_uri) else False
        self.help = 'https://www.meetup.com/meetup_api/docs/'
        self.test = test

    @property
    def config(self):
        return {
            "group": self.group,
            "email": self.email,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }

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
                        filter=None):
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
            filter).value

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
