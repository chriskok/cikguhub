# CikguHub

## Installation

- Download Anaconda: https://docs.anaconda.com/anaconda/install/index.html
- `conda create -n cikgu python=3.9`
- `pip install -r requirements.txt`

## Setup 
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- temporarily using user: 'admin', pass: 'cikgupass'

## Running the Application
- `python manage.py runserver`