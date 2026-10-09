from pathlib import Path

import pytest

pytest.importorskip("airflow")

from airflow.models.dagbag import DagBag  # noqa: E402

DAGS_DIR = Path(__file__).resolve().parents[1] / "dags"
DAG_ID = "ecommerce_pipeline"


@pytest.fixture(scope="module")
def dagbag():
    return DagBag(dag_folder=str(DAGS_DIR), include_examples=False)


@pytest.fixture(scope="module")
def dag(dagbag):
    found = dagbag.dags.get(DAG_ID)
    assert found is not None, f"No se encontró el DAG {DAG_ID}"
    return found


def test_sin_errores_de_importacion(dagbag):
    assert dagbag.import_errors == {}


def test_tareas_esperadas(dag):
    assert set(dag.task_ids) == {"load_raw_data", "dbt_run", "dbt_test"}


def test_orden_de_dependencias(dag):
    assert dag.get_task("load_raw_data").upstream_task_ids == set()
    assert dag.get_task("dbt_run").upstream_task_ids == {"load_raw_data"}
    assert dag.get_task("dbt_test").upstream_task_ids == {"dbt_run"}


def test_una_sola_ejecucion_a_la_vez(dag):
    assert dag.max_active_runs == 1


def test_catchup_desactivado(dag):
    assert dag.catchup is False


def test_reintentos(dag):
    # La carga es idempotente, así que reintentarla es seguro; dbt falla de forma determinista.
    assert dag.get_task("load_raw_data").retries == 2
    assert dag.get_task("dbt_run").retries == 0
    assert dag.get_task("dbt_test").retries == 0


def test_todas_las_tareas_tienen_timeout(dag):
    for task in dag.tasks:
        assert task.execution_timeout is not None, f"{task.task_id} sin timeout"


def test_todas_las_tareas_tienen_callback_de_fallo(dag):
    for task in dag.tasks:
        assert task.on_failure_callback, f"{task.task_id} sin on_failure_callback"


def test_comandos_de_cada_tarea(dag):
    assert "load_raw_data.py" in dag.get_task("load_raw_data").bash_command
    assert "dbt run" in dag.get_task("dbt_run").bash_command
    assert "dbt test" in dag.get_task("dbt_test").bash_command
