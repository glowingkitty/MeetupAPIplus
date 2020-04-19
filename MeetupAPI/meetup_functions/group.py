import time

from MeetupAPI.log import Log


class MeetupGroup():
    def __init__(self, group_url):

        # Get Group
        # https://www.meetup.com/meetup_api/docs/:urlname/#get
        import requests

        self.logs = ['self.__init__']
        self.started = round(time.time())

        self.log('MeetupGroup()')
        self.response = requests.get('https://api.meetup.com/'+group_url)

        self.response_json = self.response.json()
        if 'errors' in self.response_json and self.response_json['errors'][0]['code'] == 'group_error':
            self.log('-> ERROR: Group name doesnt exist')
            self.log(self.response_json)
            self.value = None
        else:
            self.value = self.response_json

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
