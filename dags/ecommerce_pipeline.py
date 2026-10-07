import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

log = logging.getLogger(__name__)


def notify_failure(context):
    ti = context["task_instance"]
    log.error(
        "FALLO en pipeline: dag=%s task=%s run_id=%s",
        ti.dag_id,
        ti.task_id,
        context["run_id"],
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "on_failure_callback": notify_failure,
}

with DAG(
    "ecommerce_pipeline",
    default_args=default_args,
    description="Pipeline principal: Ingesta -> dbt run -> dbt test",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["ecommerce", "dbt"],
) as dag:

    load_raw_data = BashOperator(
        task_id="load_raw_data",
        bash_command="python /opt/airflow/src/ingestion/load_raw_data.py",
        retries=2,
        retry_delay=timedelta(minutes=1),
        execution_timeout=timedelta(minutes=10),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt/ecommerce && dbt run --profiles-dir .",
        execution_timeout=timedelta(minutes=15),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt/ecommerce && dbt test --profiles-dir .",
        execution_timeout=timedelta(minutes=15),
    )

    load_raw_data >> dbt_run >> dbt_test