#!/usr/bin/env bash

## !!! IMPORTANT:
## Uncomment the following line for the first running. After you've authenticated
## once, you won't need to run this line anymore:
# gcloud auth application-default login

# GS: Check if blob name exists, else it's created
gsutil ls -b gs://asr-cloud-201701454 || gsutil mb -l US gs://asr-cloud-201701454

# Copy the example transaction in the desired bucket:
gsutil cp transaction.csv gs://asr-cloud-201701454

# BQ: Check if dataset transactions exists, else it's created. 
bq.cmd ls transactions || bq.cmd mk -d transactions

# BQ: Check if table records exists, else it's created
#ID table= dataset.table
bq.cmd ls transactions | grep records || bq.cmd mk --table transactions.records ID:STRING,AMOUNT:FLOAT

# Deployment CLOUD FUNCTION
: '
Definimos la cloud function que se EJECUTA=DEPLOY
nombre ingester-transactions
entry-point=funcion que se ejecuta en el codigo= ingest_transactions. 
lenguaje py3.8
trigger-resource= CLOUD STORAGE BUCKET. SE ENCUENTRA ESCUCHANDO LOS EVENTOS DEL BUCKET.
trigger-event= finaliza la carga del objeto (blob). Cuando se guarde el archivo, se ejecutara el entrypoint
memory que ocupa
timeout =duracion de la cloud function (como mucho). pasado ese tiempo finaliza.
'

gcloud functions deploy ingester-transactions \
        --entry-point=ingest_transaction \
        --runtime python38 \
        --trigger-resource asr-cloud-201701454 \
        --trigger-event google.storage.object.finalize \
        --memory 512MB \
        --timeout 60s