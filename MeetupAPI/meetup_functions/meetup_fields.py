
class MeetupFields():
    # define functions to get event details based on meetup data
    def str_name_en_US(self, event):
        return event['name']

    def int_UNIXtime_event_start(self, event):
        return round(event['time']/1000)

    def int_UNIXtime_event_end(self, event):
        return round((event['time']/1000)+(event['duration']/1000))

    def int_minutes_duration(self, event):
        return round((event['duration']/1000)/60)

    def url_featured_photo(self, event):
        return event['featured_photo']['photo_link'] if 'featured_photo' in event else event['image_url'] if 'image_url' in event and event['image_url'] else None

    def text_description_en_US(self, event):
        return event['description']

    def str_location(self, event):
        from MeetupAPI.meetup_functions.str_location import MeetupSTRlocation
        return MeetupSTRlocation(event, self.default_space_name, self.default_space_address).value

    def str_series_id(self, event):
        return event['series']['id'] if 'series' in event else None

    def int_series_startUNIX(self, event):
        return round(event['series']['start_date'] / 1000) if 'series' in event and 'start_date' in event['series'] else None

    def int_series_endUNIX(self, event):
        return round(event['series']['end_date'] / 1000) if 'series' in event and 'end_date' in event['series'] else None

    def text_series_timing(self, event):
        from MeetupAPI.meetup_functions.text_series_timing import MeetupTextSeriesTiming
        return MeetupTextSeriesTiming(event).value

    def url_meetup_event(self, event):
        return event['link'] if 'link' in event else None

    def int_UNIXtime_created(self, event):
        return round(event['created']/1000)

    def int_UNIXtime_updated(self, event):
        return round(event['updated']/1000) if 'updated' in event else None

    def int_timezoneToOffset(self, timezone_name):
        from MeetupAPI.meetup_functions.int_timezoneToOffset import MeetupIntTimezoneToOffset
        return MeetupIntTimezoneToOffset(timezone_name).value

    def list_offsetToTimezone(self, offset_ms):
        from MeetupAPI.meetup_functions.list_offsetToTimezone import MeetupListOffsetToTimezone
        return MeetupListOffsetToTimezone(offset_ms).value

    def str_timezone(self, event):
        from MeetupAPI.meetup_functions.str_timezone import MeetupSTRtimezone
        return MeetupSTRtimezone(event, self.default_space_timezonestring).value
