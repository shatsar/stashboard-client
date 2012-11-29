# Stashboard Client

A Python **command line** suite to easily push statuses to a [stashboard](http://stashboard.org) instance.
Its goal is to easily check the status of different services.


## HOW-TO


To put this suite in production you have to work on two different parts: the *configuration* and the *main script*:

### Main Script
The main script is the one you want to put in crontab, to automatically perform a set of tests.

For example to test an HTTP server, it looks like this:

```
from stashboard_http_check import StashboardHttpCheck

v = StashboardHttpCheck("section_name")
v.check()

```

Where ``section_name`` is the section in the configuration file where to find the information needed


### Configuration
stashboard-client's configuration is a simple [configparser](http://docs.python.org/2/library/configparser.html) file with the ``stashboard`` section:

```
[stashboard]
base_url=https://stashboard.appspot.com
consumer_key=anonymous
consumer_secret=anonymous
oauth_key=
oauth_secret=
message.up=Up and Running
message.warning=Something is wrong
message.down=Issues
```

#### Stashboard-http-client

To test an HTTP server, the configuration section looks like this:

```
[mashape.com]
stashboard_service=redirect
url=https://mashape.com
status=301
response_time=200
```