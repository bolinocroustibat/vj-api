# Automatic Video Jockey API

Provides a random YouTube video ID according to an optional given theme, and store cached YouTube IDs in a DB for later usage without depleting the YouTube API quota.

This branch is using Django and Django Ninja. There is [another branch using FastAPI and SQlite](https://github.com/bolinocroustibat/vj-api/tree/fastapi).


## Main dependencies

Python API with a SQLite database, using Django framework, and deployed to Heroku.

- Python 3.7 (also tested successfully with 3.9)
- [Poetry](https://python-poetry.org/)
- [Django](https://www.djangoproject.com/)
- [Django-Ninja](https://django-ninja.rest-framework.com/)
- A MySQL or MariaDB database
- A YouTube API v3 key


## Install

Create a virtual environnement and install the dependencies in it with Poetry single command:
```sh
poetry install
```

## Run 

Activate the virtual environement:
```sh
poetry shell
```

Put your YouTube API v3 key in your local_settings.py:
```sh
YOUTUBE_API_KEY="MY_API_KEY"
```

Launch the Django web server:
```sh
./manage.py runserver
```


### To run as async with ASGI with Uvicorn

```sh
gunicorn vj_api.asgi:application -k uvicorn.workers.UvicornWorker
```

For production, the number of workers `-w` should be adjusted based on the number of CPU cores.
For example, here with 20 cores, on port 8002 and adding a log file:
```sh
gunicorn vj_api.asgi:application -w 40 -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:8002"
```

To debug:
```sh
gunicorn vj_api.asgi:application -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:8002" --log-level debug
```
