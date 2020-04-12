from config import Config


class MeetupSTRtimezone():
    def __init__(self, event):
        from meetup_functions.list_offsetToTimezone import MeetupListOffsetToTimezone
        from meetup_functions.int_timezoneToOffset import MeetupIntTimezoneToOffset
        TIMEZONE_STRING = Config('PHYSICAL_SPACE.TIMEZONE_STRING').value

        if 'utc_offset' in event and event['utc_offset'] != MeetupIntTimezoneToOffset(TIMEZONE_STRING).value:
            self.value = MeetupListOffsetToTimezone(event['utc_offset']).value
        else:
            self.value = TIMEZONE_STRING
