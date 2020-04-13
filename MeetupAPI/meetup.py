import json
import time

import requests

from meetup_api.log import Log
from meetup_api.meetup_functions.meetup_fields import MeetupFields


class Meetup(MeetupFields):
    def __init__(self,
                 group,
                 email=None,
                 password=None,
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
        self.groups = []
        self.response = None
        self.email = email
        self.password = password
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

        self.setup_done = True if group else False
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
        from meetup_api.meetup_functions.access_token import MeetupAcessToken
        return MeetupAcessToken(self.email, self.password, self.client_id, self.client_secret, self.redirect_uri).value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def events(self,
               results_per_page=200,
               pages='all',
               maximum_num_events=10000,
               fields=['group_key_photo', 'series',
                       'simple_html_description', 'rsvp_sample']
               ):
        from meetup_api.meetup_functions.events import MeetupEvents
        return MeetupEvents(self, results_per_page,
                            pages, maximum_num_events, fields).value

    def create(self, event, announce=False, publish_status='draft'):
        from meetup_api.meetup_functions.create import MeetupCreate
        return MeetupCreate(self.access_token, self.group, event, announce, publish_status, self.default_space_how_to_find_us).value

    def delete(self, event):
        from meetup_api.meetup_functions.delete import MeetupDelete
        return MeetupDelete(self.access_token, self.group, event).value
