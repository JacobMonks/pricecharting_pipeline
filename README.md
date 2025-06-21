# Pricecharting Prices Pipeline

This is an ETL application that will run an automated job on a schedule to update the user's video game collection.

The general workflow is to query all items from the current collection and run an HTTP request to retrieve 
the most up-to-date data from Pricecharting.com to update the user's database.

The user will also be able to add new items to their collection by providing the name, the console, and the
desired condition (loose, complete in box, or individual items).

The scheduled job will run using Apache Airflow via Google Cloud Composer. The collection addition feature 
will be done by reading in new CSV files uploaded to Google Cloud Storage.

## Project Updates

### June 20, 2025
- Project Repo created. Wrote first draft of README.