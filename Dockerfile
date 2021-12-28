FROM python:3.9.5-slim-buster

COPY . /interview_platform
WORKDIR /interview_platform

RUN apt-get update && pip install --upgrade pip && \
	apt-get -y install libpq-dev gcc && \
	pip install psycopg2 && pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP = 'int_platform.py'
ENV DATABASE_URL="postgresql://xoxoji:password@192.168.0.105/inter_platform"

COPY requirements.txt /app/requirements.txt




ENV PGPASSWORD password
CMD psql --host=192.168.0.105 --port=5432 --username=xoxoji -c "SELECT 'SUCCESS !!!';"

EXPOSE 5000
EXPOSE 5432

CMD ["python","int_platfrom.py"]
