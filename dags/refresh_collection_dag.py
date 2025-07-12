from datetime import datetime, timedelta
from airflow.decorators import dag, task


@dag(
        dag_id="refresh_collection",
        start_date=datetime(2025, 7, 12),
        schedule="0 10 * * 0",
        tags=["sunday", "weekly"],
        catchup=False,
        retry_delay=timedelta(minutes=5),
        default_args={"retries": 2, "owner": "Jacob"}
)
def refresh_collection():

    @task()
    def dummy_task(**kwargs):
        pass

    dummy_task()


refresh_collection()
