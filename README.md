# Steps to setup & Run
1. `python -m pip install virtualenv`
2. `python -m virtualenv env`
3. for windows `env\Scripts\activate`, for linux/mac `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py runserver`