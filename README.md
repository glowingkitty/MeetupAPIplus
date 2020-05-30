![MeetupAPIplus](https://raw.githubusercontent.com/marcoEDU/MeetupAPIplus/master/images/headerimage.jpg "MeetupAPIplus")

Use the combined power of the official Meetup API and a web scraper to implement Meetup into your project.

Want to support the development and stay updated?

<a href="https://www.patreon.com/bePatron?u=24983231"><img alt="Become a Patreon" src="https://raw.githubusercontent.com/marcoEDU/MeetupAPIplus/master/images/patreon_button.svg"></a> <a href="https://liberapay.com/glowingkitty/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>


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
pages = 'all' or int ('all' is default)
maximum_num_results = int
fields = list
```


#### Meetup().message()

Meetup().message() can send a message (including optional placeholders) to one or multiple other users.

Required inputs for .message():
```
receiver_members = dict or list (Example: {'name':'xxxx','id':'yyyy'})
message = str
```

Optional inputs for .message():
```
json_placeholders = list (with json entries in this scheme: {'keyword':xxxx,'replace_with':yyyyy})
save_log = boolean
log_path = str (default: 'sent_messages_log.json')
spam_prevention = boolean (default: True, prevents sending the same message multiple times to the same user or sending too many messages in a short time period to the same user)
spam_prevention_wait_time_minutes = int (default: 1440)
test = boolean (default: False, makes a screenshot of the message instead of sending the message)
auto_close_selenium = boolean (default: True, closes the web browser when finished with sending a message)
scraper = PyWebScraper class (default: None, needed if you want to send multiple messages in the same browser window)
```

### API credentials required

#### Meetup().upcoming_events()

Based on [https://www.meetup.com/meetup_api/docs/find/upcoming_events/](https://www.meetup.com/meetup_api/docs/find/upcoming_events/)

Will return a list of upcoming events on Meetup.

Required inputs for Meetup():
```
groupname = str
client_id = str
client_secret = str
redirect_uri = str
```

Optional inputs for .upcoming_events():
```
results_per_page = int
pages = 'all' or int ('all' is default)
maximum_num_results = int
city = str (Example: 'Berlin, Germany' or 'New York, NY')
lat = float
lon = float
text = str
topic_category = int
min_num_attendees = int
filter = list (options are: 
    'online_meetups' -> filters for online meetups, on zoom, skype, jitsi, etc.
    'lang:{language short code}' -> filter for events who's title is in the language you define. Example: 'lang:en' or 'lang:de'
    'group_urls_only' -> returns urls of groups instead of events as json
```

#### Meetup().create()

Based on [https://www.meetup.com/meetup_api/docs/:urlname/events/#create](https://www.meetup.com/meetup_api/docs/:urlname/events/#create)

If successfull, Meetup().create() will return the event it was given, but with the meetup link as event.url_meetup_event.
If the request fails, Meetup().create returns None.

Required inputs for Meetup():
```
groupname = str
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
client_id = str
client_secret = str
redirect_uri = str
```

Required inputs for .delete():
```
event = Event class (with field 'url_meetup_event' and Event.save() function)
```


#### Meetup().message_group_organizer()

Meetup().message_group_organizer() can message the group organizers from all groups of all upcoming events in selected cities. Have in mind that there is a limit of 20 messages/day integrated into this function, to prevent you getting blocked by Meetup.

Optional inputs for .message_group_organizer():
```
messages = str or list (default: None. If a list is given, a random message will be selected)
messages_paths = str or list (default: 'message_to_organizer.txt', create a text file in that path to define a message which will be send. If a list is given, a random message will be selected)
cities = list (default: [
                        'San Francisco, CA',
                        'Los Angeles, CA',
                        'New York, NY',
                        'Seattle, WA',
                        'Boston, MA',
                        'Chicago, IL',
                        'Detroit, Michigan',
                        'Washington, DC',
                        'Miami, FL',
                        'Toronto, Canada',
                        'Barcelona, Spain',
                        'Madrid, Spain',
                        'Paris, France',
                        'Rome, Italy',
                        'Milano, Italy',
                        'London, UK',
                        'Berlin, Germany',
                        'Munich, Germany',
                        'Vienna, Austria',
                        'Amsterdam, Netherlands',
                        'Singapore, Singapore',
                        'Hong Kong, Hong Kong',
                        'Tokyo, Japan',
                        'Seoul, South Korea'
                    ])
cities_processed_path = str (default: 'processed_cities.json', where the progress of processed cities will be saved)
maximum_num_results = int (default: 20, how many group organizer per city should be messaged. Have in mind: the daily messaging limit is 20)
filters = list (default: ['online_meetups', 'lang:en'], filters for upcoming_events, from which the group organizers will be collected)
```