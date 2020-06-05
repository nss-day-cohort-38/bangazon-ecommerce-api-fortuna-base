## Bangazon Django REST API 

# Steps to get the Bangazon API started

1. Create a directory in your termincal, and `cd` into that directory. From there you need to clone down this repo by using `git clone (ssh_key_here)`. 

1. In your terminal, you need to enter into that directory you just cloned down using `cd bangazon-ecommerce-api-fortuna-base/`.

1. Set up your virtual environment:
    `python -m venv bangazonEnv`

1. Activate virtual environment:
    `source ./bangazonEnv/bin/activate`

1. Install dependencies:
    `pip install -r requirements.txt`

1. Install pillow:
    `pip install Pillow`

1. Make migrations:
    `python manage.py makemigrations`

1. Run migrations:
    `python manage.py migrate`

1. Create super user for your local version:
    `python manage.py createsuperuser`

1. Populate your database with initial fixtures:
    `python manage.py loaddata */fixtures/*.json`

1. Boot up the server: 
    `python manage.py runserver`

1. Go back to https://github.com/nss-day-cohort-38/bangazon-ecommerce-web-app-fortuna-base and finish the last steps there.

## To view your data in the web browser go to http://localhost:8000
