#!/bin/sh

export AIRFLOW_HOME=${PWD}/airflow
export AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
export AIRFLOW__CORE__LOAD_EXAMPLES=False

export AIRFLOW__METRICS__STATSD_ON=True
export AIRFLOW__METRICS__STATSD_HOST=statsd-exporter
export AIRFLOW__METRICS__STATSD_PORT=8125
export AIRFLOW__METRICS__STATSD_PREFIX=airflow
export B2B_FOLDER=data/b2b_input
export VALIDATION_FOLDER=data/validation_input
export PREDICTION_FOLDER=data/prediction_input
export REJECT_FOLDER=data/rejected
export OUTPUT_FOLDER=data/output

airflow db init
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@admin.com \
    --password admin

airflow scheduler &
airflow webserver --port 9091