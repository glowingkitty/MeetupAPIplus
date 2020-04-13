# Meetup-API
Use the combined power of the official Meetup API and a web scraper to implement Meetup into your project.

Want to support the development financially? Donations are always welcomed! 
[Click here to donate on Liberapay](https://liberapay.com/marcoEDU)

[<img src="http://img.shields.io/liberapay/receives/marcoEDU.svg?logo=liberapay">](https://liberapay.com/marcoEDU)

## Installation

```
pip install MeetupAPI
```

## Usage

```
from MeetupAPI import Meetup
```

### API credentials optional

#### Meetup().events()

Based on [https://www.meetup.com/meetup_api/docs/:urlname/events/#list](https://www.meetup.com/meetup_api/docs/:urlname/events/#list)

Meetup().events() will return a JSON with events from the group you enter. By default it returns the first 10.000 events of the group.

Required inputs for Meetup():
```
groupname = str
```

Optional inputs for .events():
```
results_per_page = int
pages = 'all' or int
maximum_num_events = int
fields = list
```

### API credentials required

#### Meetup().create()

Based on [https://www.meetup.com/meetup_api/docs/:urlname/events/#create](https://www.meetup.com/meetup_api/docs/:urlname/events/#create)

If successfull, Meetup().create() will return the event it was given, but with the meetup link as event.url_meetup_event.
If the request fails, Meetup().create returns None.

Required inputs for Meetup():
```
groupname = str
email = str, (from your meetup account, for authentication)
password = str (from your meetup account, for authentication)
client_id = str
client_secret = str
redirect_uri = str
```

Optional inputs for Meetup():
```
default_space_name = str
default_space_address_street = str
default_space_address_zip = str
default_space_address_city = str
default_space_address_countrycode = str
default_space_how_to_find_us = str
default_space_timezonestring = str
```

Required inputs for .create():
```
event = Event class (with fields 
    'str_name_en_US',
    'text_description_en_US',
    'int_minutes_duration',
    'float_lat',
    'float_lon',
    'str_name_en_US',
    'int_UNIXtime_event_start',
    'url_meetup_event' 
    and Event.save() function)
```

Optional inputs for .create():
```
announce = boolean (announces the event to group members on meetup)
publish_status = 'draft' or 'published' (default is 'draft')
```


#### Meetup().delete()

Based on [https://www.meetup.com/meetup_api/docs/:urlname/events/#delete](https://www.meetup.com/meetup_api/docs/:urlname/events/#delete)

If successfull, Meetup().delete() will return the event it was given, but with event.url_meetup_event = None.
If the request fails, Meetup().delete returns None.

Required inputs for Meetup():
```
groupname = str
email = str, (from your meetup account, for authentication)
password = str (from your meetup account, for authentication)
client_id = str
client_secret = str
redirect_uri = str
```

Required inputs for .delete():
```
event = Event class (with field 'url_meetup_event' and Event.save() function)
```