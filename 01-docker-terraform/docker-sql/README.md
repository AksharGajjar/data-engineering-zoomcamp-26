# Docker SQL Directory

This directory contains resources for managing PostgreSQL and PgAdmin services using Docker, as well as Python scripts for data ingestion. The Docker images rely on the virtual environment (`venv`) located in the root directory of the project.

## Contents

- **Dockerfiles**:
  - `Dockerfile.ingest_data_csv`: Builds a Docker image for ingesting CSV data using Python.
  - `Dockerfile.ingest_data_parquet`: Builds a Docker image for ingesting Parquet data using Python.
  - `Dockerfile.ingest_zones_data`: Builds a Docker image for ingesting zone data using Python.
- **docker-compose.yaml**:
  - Defines services for PostgreSQL (`pgdatabase`) and PgAdmin (`pgadmin`) and connects them to the `data_engineering_network`.
- **Python Scripts**:
  - `ingest_data_csv.py`: Script for ingesting CSV data.
  - `ingest_data_parquet.py`: Script for ingesting Parquet data.
  - `ingest_zones_data.py`: Script for ingesting zone data.

## Important Notes

1. **Virtual Environment**:
   - The Docker images use the `venv` environment from the root directory (`/workspaces/data-engineering-zoomcamp-26`).
   - All `docker build` commands must be executed from the root directory to ensure proper access to the virtual environment.

2. **Docker Network**:
   - The `docker-compose.yaml` file creates a custom Docker network named `data_engineering_network`.
   - This network must be used when running the Docker images.

## Commands

### Build Docker Images
Run the following commands from the root directory:

```bash
# Build the ingest_data_csv image
docker build -f 01-docker-terraform/docker-sql/Dockerfile.ingest_data_csv -t ingest_data_csv:v001 .

# Build the ingest_data_parquet image
docker build -f 01-docker-terraform/docker-sql/Dockerfile.ingest_data_parquet -t ingest_data_parquet:v001 .

# Build the ingest_zones_data image
docker build -f 01-docker-terraform/docker-sql/Dockerfile.ingest_zones_data -t ingest_zones_data:v001 .
```

### Start Services with Docker Compose
Run the following command to start PostgreSQL and PgAdmin services:

```bash
docker-compose -f 01-docker-terraform/docker-sql/docker-compose.yaml up -d
```

### Test Docker Images
Run the following commands to test the Docker images:

```bash
# Test the ingest_data_csv image
docker run --rm --network=data_engineering_network ingest_data_csv:v001

# Test the ingest_data_parquet image
docker run --rm --network=data_engineering_network ingest_data_parquet:v001

# Test the ingest_zones_data image
docker run --rm --network=data_engineering_network ingest_zones_data:v001
```

### Stop Services
Run the following command to stop the services:

```bash
docker-compose -f 01-docker-terraform/docker-sql/docker-compose.yaml down
```

### Troubleshooting
Ensure the data_engineering_network exists and the containers are attached to it:

```bash
docker network inspect data_engineering_network
```

If the network is missing, recreate it:

```bash
docker network create data_engineering_network
```