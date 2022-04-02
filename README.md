# GCP_project
This repo contains basic Google Cloud Platform programming routine for ingesting data with cloud functions, and also how include automatization and CI/CD pipeline.

# Data ingestion
In this part a Cloud Function is created and configured to listen to changes (new incoming local files) in a Cloud Storage bucket, and dump them formatted in a table in Big Query. Finally, the routine will be uploaded in a Cloud Source Repository.

To achieve this, it would be necessary to configure the following services:
- .csv local file 
- Cloud Storage Bucket
- Big Query DataSet and Table
- Cloud Source Repository

The complete data ingestion process would be the following:
1. Create Cloud Storage Bucket with an unique name
2. Create Big Query Dataset and table in wich transactions will be dumped
3. Define Cloud Function (deployment) with entry-point function
4. Define entry-point function of the CF-> trigger that is raised every time a file (event) is stored in the bucket. Function will load the file (blob) in BQ table.
  - Inside endpoint: 
  o Download blob local file.
  o Prepare blob with dataframe (rows, columns) -> requirements.txt.
  o Upload to BQ with appropriate format (pandas library dataframe)
5. Create Cloud Source Repository and upload the whole project.
6. Estimate project costs 1700 transactions/s -> CF processing, Storage and Big Query.

Steps 1-3 are included in deployment.sh file, which is executable.
Step 4 is included in main.py file.
Steps 5 and 6 (and also the whole process explanation) is included in the .pdf file (in Spanish).
Regarding code files, you will have to change the bucket and repo name according to your particular case.

This process and the actors involved in it are shown in the next figure:
![image](https://user-images.githubusercontent.com/46919127/161377310-8d343894-1398-4d64-95f6-7c7b8b012bcf.png)


The data ingested will be .csv files that collects a list of simple transactions. The format expected is shown with an example included in this repo.

# CI/CD pipeline
Besides, to include automatization and CI/CD pipeline to the current ingesting data project, Google Cloud Build service will be configured for the management of the Cloud Function Repository. 
To achieve this, it is necesarry to generate a Cloud Build trigger (with 3 states "dev", "pre" or "prod", located in create_triggers.sh file) will be listening to the repository in the "master" branch, and also configure Cloud Build (cloudbuild-prod.yaml file)so that the cloud function with the correct entry-point is deployed. Any change in the master (such as uploading new files to the repo or deleting them) will act as a trigger and make the CF deploy to update the repo.

To show how it works, in the .pdf file included, artificial changes are generated and pushed in the repo, and screenshots of the trigger history in Cloud Build are taken to show the evolution of the CI/CD Pipeline. 
