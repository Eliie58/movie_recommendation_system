#!/bin/sh

until test -f "/models/model.joblib"; do
    >&2 echo "Model is not available - sleeping"
    sleep 10
done

uvicorn api.main:app --host 0.0.0.0 --port 80
