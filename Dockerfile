FROM apache/airflow:3.0.6

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir \
    pandas \
    "psycopg[binary]" \
    dbt-postgres