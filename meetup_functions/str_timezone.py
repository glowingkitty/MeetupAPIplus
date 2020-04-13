
class MeetupSTRtimezone():
    def __init__(self, event, TIMEZONE_STRING):
        from meetup_functions.list_offsetToTimezone import MeetupListOffsetToTimezone
        from meetup_functions.int_timezoneToOffset import MeetupIntTimezoneToOffset

        if 'utc_offset' in event and event['utc_offset'] != MeetupIntTimezoneToOffset(TIMEZONE_STRING).value:
            self.value = MeetupListOffsetToTimezone(event['utc_offset']).value
        else:
            self.value = TIMEZONE_STRING
