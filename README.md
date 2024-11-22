# Docker_Airflow_Postgres
Starter Setup for Dockerized Airflow and Postgres

We will pull publickly available Commodity Futures Trading Commission data.

On every Friday 15:30 US/Eastern time, an airflow DAG will pull the data in local database.

![alt text](System_Diagram.png)

# Preparation

1. git clone this repo
2. make a copy of .env_sample.txt and rename it to .env
3. run the following shell code and place the value in .env (to avoid Linux permission error)

```sh
echo -e "AIRFLOW_UID=$(id -u)" 
```

4. Build & initialize aifrlow
```sh
docker compose build airflow-init
docker compose build
```

5. Start the project services
```sh
docker compose up -d
```
6. to remove everything, including data (done testing)
```sh
docker compose down --volumes --remove-orphans
```

7. Manual DBT model start
```sh
source .env
cd dsec_dbt

export DB_HOST=$DB_HOST
export DB_USER=$DB_USER
export DB_ADMIN_PASSWORD=$DB_ADMIN_PASSWORD
export DB_PORT=$DB_PORT_OUTSIDE
export DB_NAME=$DB_NAME
export DB_SCHEMA=$DB_SCHEMA

```


# Considerations

1. Airflow and the database should probably live in separate repositories (separation of concerns)
2. There is a lot of ways to configure Aiflow DAG's -> this is a great book on the topic: https://www.amazon.co.uk/Data-Pipelines-Apache-Airflow-Harenslak/dp/1617296902 
3. The following course was extremely useful for the wide subject of Docker: https://www.udemy.com/share/101Wek/
