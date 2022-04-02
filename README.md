# GCP_project
This repo contains basic Google Cloud Platform programming routine for ingesting data with cloud functions, and also how include automatization and CI/CD pipeline.

# Data ingestion

En esta práctica vamos a preparar una 
Cloud Function que será responsable de "ingerir"
ficheros de transacciones que se volcarán en un 
Bucket de Google Cloud Storage (como zona de 
comunicación entre nuestro proyecto y el mundo
exterior). Para ello necesitamos:

- Un bucket de comunicación
- Un ejemplo fichero que se volcará en el Bucket de comunicación
- Un dataset y una tabla en BigQuery donde volcar la información del archivo 

La preparación de estos ingredientes ocurre en el 
fichero [deployment.sh](deployment.sh).
El último paso de este script de despliegue es 
precisamente el despliegue de la Cloud Function
en nuestro proyecto.


The data ingestion process and the actors involved in it are shown in the next figure:
![image](https://user-images.githubusercontent.com/46919127/161377310-8d343894-1398-4d64-95f6-7c7b8b012bcf.png)

# CI/CD pipeline
Besides, to include automatization a

The data ingested will be .csv files that collects a list of simple transactions. he The format expected is shown with an example included in this repo.
