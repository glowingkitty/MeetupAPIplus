import json
import os
import random
import time
import webbrowser

import requests

from MeetupAPI.log import Log


class MeetupAcessToken():
    def __init__(self, access_token, access_token_valid_upto, client_id, client_secret, redirect_uri):
        self.logs = ['self.__init__']
        self.started = round(time.time())

        # check if still usable token is saved in secrets.json - else get new one
        if access_token and access_token_valid_upto > time.time()+60:
            self.value = access_token, access_token_valid_upto

        else:
            # check if required fields exist
            if not client_id or not client_secret or not redirect_uri:
                self.log('-> ERROR: Meetup secrets incomplete!')
                self.value = None, None

            else:
                self.log('Getting Access Token from Meetup...')
                # else: following steps to get an API token - see https://www.meetup.com/meetup_api/auth/

                # Step 1: Open page to access token page
                self.log('Trying to open https://secure.meetup.com/oauth2/authorize?scope=basic+event_management&client_id={}&response_type=code&redirect_uri={}'.format(
                    client_id, redirect_uri))
                webbrowser.open('https://secure.meetup.com/oauth2/authorize?scope=basic+event_management&client_id={}&response_type=code&redirect_uri={}'.format(
                    client_id, redirect_uri))

                code_input = input(
                    'Login to generate the access key and enter the URL which you got redirected to (which ends with code=...)\n')
                while 'code=' not in code_input:
                    code_input = input(
                        'Login to generate the access key and enter the URL which you got redirected to (which ends with code=...)\n')

                code = code_input.split('code=')[1]

                # Step 2: get access token
                self.response_json = requests.post('https://secure.meetup.com/oauth2/access',
                                                   params={
                                                       'client_id': client_id,
                                                       'client_secret': client_secret,
                                                       'code': code,
                                                       'response_type': 'code',
                                                       'grant_type': 'authorization_code',
                                                       'redirect_uri': redirect_uri,
                                                       'scope': ['basic', 'event_management']
                                                   }).json()

                if 'access_token' in self.response_json:
                    access_token = self.response_json['access_token']
                    access_token_valid_upto = round(
                        time.time()+self.response_json['expires_in'])
                    # return access token and expire time and save in secrets.json
                    if os.path.exists('_setup/secrets.json'):
                        with open('_setup/secrets.json') as json_file:
                            secrets = json.load(json_file)
                    elif os.path.exists('secrets.json'):
                        with open('secrets.json') as json_file:
                            secrets = json.load(json_file)
                    else:
                        secrets = {}

                    secrets['MEETUP'] = {}
                    secrets['MEETUP']['ACCESS_TOKEN'] = access_token
                    secrets['MEETUP']['ACCESS_TOKEN_VALID_UPTO'] = access_token_valid_upto

                    if os.path.exists('_setup/secrets.json'):
                        with open('_setup/secrets.json', 'w') as outfile:
                            json.dump(secrets, outfile, indent=4)
                    else:
                        with open('secrets.json', 'w') as outfile:
                            json.dump(secrets, outfile, indent=4)

                    self.value = access_token, access_token_valid_upto
                else:
                    self.log(
                        '-> ERROR: Failed to get Access Token - {}'.format(self.response_json))
                    self.value = None

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
