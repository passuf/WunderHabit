[![Build Status](https://travis-ci.org/passuf/WunderHabit.svg?branch=master)](https://travis-ci.org/passuf/WunderHabit) [![Coverage Status](https://coveralls.io/repos/passuf/WunderHabit/badge.svg?branch=master&service=github)](https://coveralls.io/github/passuf/WunderHabit?branch=master)
[![Join the chat at https://gitter.im/passuf/WunderHabit](https://badges.gitter.im/passuf/WunderHabit.svg)](https://gitter.im/passuf/WunderHabit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# WunderHabit
Level up in [Habitica](https://habitica.com) by completing todo's in [Wunderlist](https://wunderlist.com).

## Getting Started
There is a running instance hosted on my own server:
[https://wunderhabit.passuf.ch](https://wunderhabit.passuf.ch)

Please note, this is neither an official Wunderlist nor an official Habitica project. Please use WunderHabit at your own risk!

## Run It on Your Own Server
WunderHabit is a simple [Django](https://djangoproject.com) application written in Python, which you can run on your own server.

If you are not familiar with [Django](https://djangoproject.com), you might first head over to the [Getting Started with Django](https://www.djangoproject.com/start/) docs.


### Prerequisites
* You need a [Wunderlist](https://wunderlist.com) account
* Register your [Wunderlist App](https://developer.wunderlist.com/apps) to generate a Client ID and a Client Secret to interact with the [Wunderlist API](https://developer.wunderlist.com/documentation)
* In order to communicate with the [Wunderlist API](https://developer.wunderlist.com/documentation), you need a webserver together and a trusted SSL certificate for your domain. There are free certificates available, just google for it.

### Install the Requirements

Create a virtualenv:
```
virtualenv venv_dir
```

Activate the virtualenv:
```
source venv_dir/bin/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

### Run the Django app

Copy the local settings ``local_settings.py`` and and edit them according to your setup (do not share this file!):
```
cp wunderhabit/local_settings.example.py wunderhabit/local_settings.py
```

Prepare the database:
```
python manage.py migrate
```

Run the test server to verify the installation:
```
python manage.py runserver 127.0.0.1:8001
```

### Deploy the app
There are several good guides on how to deploy a Django application. Personally, I like the one from [Michal Karzynski](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/) or [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04).


## Acknowledgements
The following projects or libraries helped a lot to efficiantly implement WunderHabit:
* [Django Project](https://www.djangoproject.com/)
* [Requests: HTTP for Humans](http://docs.python-requests.org/en/latest/)
* [Bootstrap](http://getbootstrap.com/)
* [Django-Bootstrap3](https://github.com/dyve/django-bootstrap3)
* [Gunicorn](http://gunicorn.org/)
