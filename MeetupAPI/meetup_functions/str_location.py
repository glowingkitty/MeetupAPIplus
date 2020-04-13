
class MeetupSTRlocation():
    def __init__(self, event, default_space_name, default_space_address):
        str_location_name = event['venue']['name'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != default_space_name else default_space_name
        str_location_street = event['venue']['address_1'] if 'venue' in event and 'address_1' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != default_space_name else default_space_address['STREET']
        str_location_zip = event['venue']['zip'] if 'venue' in event and 'zip' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != default_space_name else default_space_address['ZIP']
        str_location_city = event['venue']['city'] if 'venue' in event and 'city' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != default_space_name else default_space_address['CITY']
        str_location_countrycode = event['venue']['country'].upper() if 'venue' in event and 'country' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != default_space_name else default_space_address['COUNTRYCODE']
        self.value = str_location_name+'\n'+str_location_street+'\n' + \
            str_location_zip+', '+str_location_city+', '+str_location_countrycode
