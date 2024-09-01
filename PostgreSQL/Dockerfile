
FROM postgis/postgis:15-3.3

ENV POSTGRES_PASSWORD: ${DB_ADMIN_PASSWORD}

COPY Schema_definitions/ /docker-entrypoint-initdb.d/