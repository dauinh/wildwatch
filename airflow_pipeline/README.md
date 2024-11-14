```
# Initialize
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose build

# Start all services
docker compose up

# Clean up to restart
docker compose down --volumes --remove-orphans
rm -rf '<DIRECTORY>'

# Stop and delete containers, delete volumes with database data and download images
docker compose down --volumes --rmi all
```

warning: The container is run as root user. For security, consider using a regular user account.