#!/bin/sh

nohup mlflow server --backend-store-uri sqlite:////tmp/mlruns.db --default-artifact-root /tmp/mlruns --host 0.0.0.0 &

FILE=/model/models/model.joblib
if test -f "$FILE"; then
    echo "Model exists."
    sleep 5
else
    echo "Model does not exist. New model will be trained."
    python train.py
fi
tail -F nohup