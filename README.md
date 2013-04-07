# CaG LoL #

## Features ##
* Leagueformat

## Planned features ##
* Automatic bracket creation/Tournament system.
* Design

## Issues ##
* Improve update for match, simplify to always redo the results, currently changing the teams in an edit will mess up scores
* Link Round Robin in Tournament with League
* Improve seeding in Tournament
* Autopromote teams in a matchup with "None", and propagate matchups that have two "None" in them
* Perhaps make a "Match" superclass, for Match in league and Matchup in Tourmante

## Requirements ##

* Django 1.3 `pip install django`
* South `pip install south`

## Initialization ##
create dbpw.py in settings.py directory
```python
database = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

admins = (
    ('name', '@email.com'),
)

secretkey = ''
```

1. python manage.py syncdb
2. python manage.py migrate
