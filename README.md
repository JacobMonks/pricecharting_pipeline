# Pricecharting Prices Pipeline

This is an ETL application that will run an automated job on a schedule to update the user's video game collection.

The general workflow is to query all items from the current collection and run an HTTP request to retrieve
the most up-to-date data from Pricecharting.com to update the user's database.

The user will also be able to add new items to their collection by providing the name, the console, and the
desired condition (loose, complete in box, or individual items).

The scheduled job will run using Apache Airflow via Google Cloud Composer. The collection addition feature 
will be done by reading in new CSV files uploaded to Google Cloud Storage.

## Project Updates

*June 20, 2025*
- Project Repo created. Wrote first draft of README.

*July 4, 2025*
- Testing out requests to Pricecharting.com.
- Testing out extracting prices from HTML.

*July 12, 2025*
- Setting up Airflow and Docker environments.

*July 19, 2025*
- Running Airflow in Docker.

*July 28, 2025*
- Created gitignore.
- Tested local MySQL database connection.

*August 2, 2025*
- SQL table populated using new script.

*August 9, 2025*
- Created MySQL local connection functionto return specified table results.
- Created main file for running all functions locally.

*August 16, 2025*
- Created MySQL table for reporting failed requests.
- Created function to overwrite failed URLs table.
- Created interactive CLI for running code locally.

*October 19, 2025*
- Updated CLI user interface to handle page scrolling.
