## YAMDb API
![foodgram_workflow](https://github.com/BadBedBatPenguin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Foodgram is a product helper which helps user not only to pick up dishes but to get a shopping list filled with ingredients needed for chosen dishes. \
Used technologies: Python, Django, Django rest framework, PostgreSQL, Djoser, Gunicorn, Nginx, Docker-compose, Git Actions

## How to run project

Clone repo and move to its directory:

```Shell
git clone https://github.com/BadBedBatPenguin/foodgram-project-react.git
cd foodgram-project-react
```

Create and fill .env file as in sample:
```
SECRET_KEY=<secret_key_from_settings.py>
ALLOWED_HOSTS='<host IPs and names separated with whitespace>'
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<database_name>
POSTGRES_USER=<PostgreSQL_username>
POSTGRES_PASSWORD=<User_password>
DB_HOST=db
DB_PORT=5432
```
Save .env file to foodgram-project-react/infra/ directory

Start container with project:

```Shell
cd infra
docker-compose up -d --build
```

Run tests:

```Shell
docker-compose exec web python -m flake8
```

Migrate, create superuser and collect static:
```Shell
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## Filling database with data from csv files:
Put all necessary csv files to "foodgram-project-react/backend/foodgram/data/" \
run command:

```Shell
python3 manage.py import_csv
```

## Running project
To look how project runs follow this link: ([Foodgram](https://158.160.13.236))
## Autor

Tsyos Max ([BadBedBatPenguin](https://github.com/BadBedBatPenguin))

