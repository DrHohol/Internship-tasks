FROM python:3.9.5-slim-buster

COPY . /interview_platform
WORKDIR /interview_platform

RUN apt-get update && pip install --upgrade pip && \
	apt-get -y install libpq-dev gcc && \
	pip install psycopg2 && pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV FLASK_APP = 'int_platform.py'
ENV DATABASE_URL="postgresql://xoxoji:Dbpassword1@database-1.cz11cjovxwbb.eu-central-1.rds.amazonaws.com/vstup_db"

COPY requirements.txt /app/requirements.txt





EXPOSE 5000

CMD ["python","parser.py"]
CMD ["python","bot.py"]
