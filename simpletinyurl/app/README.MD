# URL Shortener
Simple URL Shortener written in django

## Requirement
- python 3.8 and above

## Library Used
- Django restframework
- Django
- Bootstrap

## How to run project
1. Setup virtualenv
2. Run `pip install -r ../requirements.txt`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver 0.0.0.0:8000`
5. Access [http://localhost:8000] using web browser

## Additonal command
- For Testing `python manage.py test`

## Constraint / Limitation
- The minimum no of characters for alias is set to 5
- The maximum no of characters for alias is set to 10