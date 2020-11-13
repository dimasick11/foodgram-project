FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8020
