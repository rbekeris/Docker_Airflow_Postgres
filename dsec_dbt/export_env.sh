#!/bin/bash
souce .env

export DB_HOST=$DB_HOST
export DB_USER=$DB_USER
export DB_ADMIN_PASSWORD=$DB_ADMIN_PASSWORD
export DB_PORT=$DB_PORT_OUTSIDE
export DB_NAME=$DB_NAME
export DB_SCHEMA=$DB_SCHEMA

#dbt run --select "MODEL_NAME"