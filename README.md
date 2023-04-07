# CikguHub

## Installation

- Download Anaconda: https://docs.anaconda.com/anaconda/install/index.html
- `conda create -n cikgu python=3.9`
- `pip install -r requirements.txt`

## Setup 
- `export DEVELOPMENT_MODE=True`
- `export DEBUG=True`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py loaddata dump.json`
<!-- - `python manage.py collectstatic` -->
<!-- - `python manage.py createsuperuser` -->

## Running the Application
- `python manage.py runserver --insecure`
- temporarily using user: 'admin', pass: 'cikgupass'
- NOTE: if you're running the system locally, you'll need to set:
    - environment variables: 
        - On Windows: `set DEVELOPMENT_MODE=True` & `set DEBUG=True` 
        - On MacOS: `export DEVELOPMENT_MODE=True` & `export DEBUG=True`

## Dumping and Loading Data
#### Dumping
- `python manage.py dumpdata > dump.json`
- OR `python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json`

#### Loading
- `python manage.py migrate`
- `python manage.py loaddata dump.json`

## Adding new libraries
- `pip list --format=freeze > requirements.txt`