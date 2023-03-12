# CikguHub

## Installation

- Download Anaconda: https://docs.anaconda.com/anaconda/install/index.html
- `conda create -n cikgu python=3.9`
- `pip install -r requirements.txt`

## Setup 
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py loaddata dump.json`
- `export DEVELOPMENT_MODE=True`
- `export DEBUG=True`
<!-- - `python manage.py collectstatic` -->
<!-- - `python manage.py createsuperuser` -->

## Running the Application
- `python manage.py runserver`
- temporarily using user: 'admin', pass: 'cikgupass'
- NOTE: if you're running the system locally, you'll need to set:
    - environment variable: `set DEVELOPMENT_MODE=True` or `export DEVELOPMENT_MODE=True` (on MacOS)
    - and run the app with: `python manage.py runserver --insecure`

## Dumping and Loading Data
#### Dumping
- `python manage.py dumpdata > dump.json`
#### Loading
- `python manage.py migrate`
- `python manage.py loaddata dump.json`