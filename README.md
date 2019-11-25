# Geosite takehome assignment

Tested on debian 10 (buster)

## Setup

- `python3 -m venv env`
- `source env/bin/activate`
- `pip install django`
- `pip install djangorestframework`
- `python manage.py makemigrations sysinfo`
- `python manage.py migrate`
- Run `python manage.py createsuperuser --username username` and follow the prompts to enter an email and **password** as `password`

## Running

- Launch the development server `python manage.py runserver localhost:5555`

## Examples

- Navigate to `http://localhost:5555` to a very basic table of the last 10 GET requests
- `curl -X GET -u username:password http://localhost:5555`
- `curl -X GET -u username:password http://localhost:5555/api/1/`
- `curl -H 'Content-Type: application/json' -X POST -d '{ "comment":"modifiedcomment"}' -u username:password http://localhost:5555/api/1/`

## Tests

```
$ python manage.py test geosite.sysinfo

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 2.017s

OK
Destroying test database for alias 'default'...

```

# Todo

- [ ] More tests
- [ ] Documentation
