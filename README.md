# CikguHub

## Installation

- Download Anaconda: https://docs.anaconda.com/anaconda/install/index.html
- `conda create -n cikgu python=3.9`
- `pip install -r requirements.txt`

## Setup 
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py loaddata db.json`
<!-- - `python manage.py createsuperuser` -->

## Running the Application
- `python manage.py runserver`
- temporarily using user: 'admin', pass: 'cikgupass'

## Dumping and Loading Data
#### Dumping
- `python manage.py dumpdata > db.json`
#### Loading
- `python manage.py migrate`
- `python manage.py loaddata db.json`