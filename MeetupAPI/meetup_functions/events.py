import time

from MeetupAPI.log import Log


class MeetupEvents():
    def __init__(self,
                 meetup_class,
                 results_per_page=200,
                 pages='all',
                 maximum_num_events=10000,
                 fields=['group_key_photo', 'series', 'simple_html_description', 'rsvp_sample']):

        # Events
        # https://www.meetup.com/meetup_api/docs/:urlname/events/#list
        import requests

        self.logs = ['self.__init__']
        self.started = round(time.time())

        self.log('events()')
        self.value = []
        self.offset = 0
        self.response_json = ['']

        if pages == 'all':
            pages = 10000

        while pages >= self.offset and len(self.response_json) > 0:
            self.response = requests.get('https://api.meetup.com/'+meetup_class.group+'/events',
                                         params={
                                             'fields': fields,
                                             'photo-host': 'public',
                                             'page': results_per_page,
                                             'offset': self.offset
                                         })
            self.offset += 1

            self.response_json = self.response.json()
            if 'errors' in self.response_json and self.response_json['errors'][0]['code'] == 'group_error':
                self.log('-> ERROR: Group name doesnt exist')
            else:
                self.value += [
                    {
                        'str_name_en_US': meetup_class.str_name_en_US(event),
                        'int_UNIXtime_event_start': meetup_class.int_UNIXtime_event_start(event),
                        'int_UNIXtime_event_end': meetup_class.int_UNIXtime_event_end(event),
                        'int_minutes_duration': meetup_class.int_minutes_duration(event),
                        'url_featured_photo': meetup_class.url_featured_photo(event),
                        'text_description_en_US': meetup_class.text_description_en_US(event),
                        'str_location': meetup_class.str_location(event),
                        'one_space': meetup_class.one_space(event) if hasattr(meetup_class, 'one_space') else None,
                        'one_guilde': meetup_class.one_guilde(event) if hasattr(meetup_class, 'one_guilde') else None,
                        'str_series_id': meetup_class.str_series_id(event),
                        'int_series_startUNIX': meetup_class.int_series_startUNIX(event),
                        'int_series_endUNIX': meetup_class.int_series_endUNIX(event),
                        'text_series_timing': meetup_class.text_series_timing(event),
                        'url_meetup_event': meetup_class.url_meetup_event(event),
                        'int_UNIXtime_created': meetup_class.int_UNIXtime_created(event),
                        'int_UNIXtime_updated': meetup_class.int_UNIXtime_updated(event),
                        'str_timezone': meetup_class.str_timezone(event)
                    } for event in self.response_json
                ]

                if len(self.value) >= maximum_num_events:
                    self.log('Collected maximum number of events.')
                    break

                self.log('Collected {} events...'.format(len(self.value)))

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
