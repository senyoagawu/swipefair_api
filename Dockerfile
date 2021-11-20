FROM python:3.8

ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

EXPOSE 8000

WORKDIR /var/www
COPY . .

RUN pip install -r requirements.txt
RUN pip install psycopg2

CMD gunicorn app:app
