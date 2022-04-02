# sistema operativo
import os
# libreria google.cloud para py
from google.cloud import storage
from google.cloud import bigquery

#dataframe
import pandas as pd

# elementos BQ
DATASET = "transactions"
TABLE = "records"
# table id =transactions.records
TABLE_ID = f"{DATASET}.{TABLE}"
print(f"Table ID BQ {TABLE_ID}")

#1. metodo formato dataframe tabla.
'''
ARGUMENTOS
    bucket_name= nombre bucket
    source_blob_name=nombre blob guardado en el bucket
    destination_file_name=tmp archivo temporal donde se guarda el blob como un DF con el fw panda (se guarda en el so)
DEVUELVE EL DF correspondiente al blob del bucket
'''
def download_blob_as_dataframe(
        bucket_name,
        source_blob_name,
        destination_file_name="/tmp/transaction.csv"):
    
    """Downloads a blob from a bucket and returns it as a DataFrame
    Cliente storage cloud-> obtener bucket y blob
    Blob download to filename temporal
    """
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name=bucket_name)

    blob = bucket.get_blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        f"Downloaded storage object {source_blob_name} "
        f"from bucket {bucket_name} to local file {destination_file_name}."
    )

    # DATAFRAME, con panda se lee formato csv el archivo temporal
    df = pd.read_csv(destination_file_name)
    # lo borramos porque no lo necesitamos en local
    os.remove(destination_file_name)
    return df
 
# 2. metodo subir tabla (con dataframe) a BQ
'''
ARGUMENTOS
    df: archivo destino blob en formato df
    destination_table_id: id tabla BQ
DEVUELVE NULL. Sube el df a la tabla correspondiente
'''
def upload_to_bigquery(dataframe, destination_table_id):
    
    """Uploads as dataframe into BigQuery
    bq cliente biqwuery cloud
    job config= define un esquema parcial. data type de las columnas.
    write_disposition= añadir nueva entrada a la tabla existente, no sustituir.(por defecto append)
    """
    bq = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        # ID= String, AMOUNT = float
        schema=[
            bigquery.SchemaField("ID", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("AMOUNT", bigquery.enums.SqlTypeNames.FLOAT)
        ],
        write_disposition="WRITE_APPEND"
    )
    #df del blob
    print(f"Data to be ingested:\n{dataframe}")
    '''
    metodo bq para subir tabla desde df
    ARGUMENTOS: dataframe, tabla destino (id), job_config (esquema tabla, tipos de datos para cada columna)
    '''
    bq.load_table_from_dataframe(
        dataframe=dataframe,
        destination=destination_table_id,
        job_config=job_config
    )

'''
entrypoint, la funcion que se ejecuta cuando se desencadena el evento -> trigger CF
'''
def ingest_transaction(event, context):
    """The entrypoint of the Cloud Function"""
    # evento ESCUCHANDO AL BUCKET
    bucket_name = event["bucket"]
    blob_name = event["name"]

    print(f"[i] Bucket name: {bucket_name}")
    print(f"[i] Filename storage path: {blob_name}")

    #obtenemos df del blob subido
    df = download_blob_as_dataframe(
        bucket_name=bucket_name,
        source_blob_name=blob_name,
    )
    #subir tabla a bq
    upload_to_bigquery(
        dataframe=df,
        destination_table_id=TABLE_ID
    )


if __name__ == "__main__":
    # This is just for local testing purposes"
    # bucket name donde se encuentra escuchando la CF =
    # file name que se guarda en el bucket
    event = {
        "bucket": "asr-cloud-201701454",
        "name": "transaction.csv"
    }

    # ejecutar entrypoint. evento=file, contexto no es relevante
    ingest_transaction(event, None)
