FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get install -y curl \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
WORKDIR /snowball_dbt
COPY . /snowball_dbt
RUN pip install -r requirements.txt
ENTRYPOINT ["dbt"]