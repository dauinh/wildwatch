```
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose down --volumes --remove-orphans
```