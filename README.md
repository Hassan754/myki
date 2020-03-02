# Myki

Myki Backend Assignment by Hassan Hammoud

## Dependencies
Django>=2.0,<3.0 #Django Framework 

psycopg2>=2.7,<3.0  # Postgresql adapter

djangorestframework # Django rest framework , the most powerful  and flexible toolkit for building Web APIs

drf-yasg # Api docs Viewer

## Installation
Build and run the project
```bash
docker-compose up
```
Migrate the database (dummy data script will populate the database)
```bash
docker-compose run web python manage.py migrate
```
Create Super User

```bash
docker-compose run web python manage.py createsuperuser
```
(To disable password validation , go to settings file and remove the content of AUTH_PASSWORD_VALIDATORS)

## Usage
Docs 

```bash
http://0.0.0.0:8000/redoc
http://0.0.0.0:8000/swagger
```

