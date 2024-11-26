# wildwatch

#### Overview

This repository contains my personal project created to learn and explore [Apache Airflow](https://airflow.apache.org/). The goal of this project is to gain hands-on experience with workflow orchestration, DAG creation, and task scheduling

[Live dashboard](https://wildwatch.streamlit.app/)

This dashboard shows:
- Habitat Distribution: Analysis of the habitats of endangered species.
- Threat Analysis: Identification of key threats to endangered species.
- Conservation Actions: Overview of conservation efforts for species at risk.
- Country Ranking: Top 20 countries with the highest number of endangered species.

## Methods

### Endangered species ETL pipeline

**Tools**: Airflow, pandas

**Objective**: 
- Extract data from IUCN official API
- Transform raw data into structured tables
- Upload data to AWS S3 for storage and further use

**Structure**

<img width="483" alt="Screenshot 2024-11-26 at 12 16 50 PM" src="https://github.com/user-attachments/assets/9da3f000-f258-42f4-91f3-f47866f86700">


1. Extraction

Data is retrieved from the IUCN Red List API in two main categories:

- Code Descriptions: Metadata about habitat, threat, and conservation action codes.
- Endangered Species Data: Information on species names, categories, population trends, and other attributes.

2. Transformation

The raw endangered species data is processed and aggregated to prepare it for analysis:

- Aggregations include summarizing species counts by habitat, threat type, and country.
- The pipeline maps habitat and threat codes to their descriptions using the metadata extracted earlier.

The processed data is saved locally as CSV files.

3. Loading

The aggregated CSV files are uploaded to AWS S3.

**Usage guide**

Prerequisite: [Docker](https://www.docker.com/), [AWS S3](https://aws.amazon.com/s3/)

- Create `.env` file with user id, project directory and [IUCN api key](https://api.iucnredlist.org/). User id can be found by running `id -u` in terminal
- Run Docker containers. Here are some helpful commands
```
# Initialize
$ docker compose up airflow-init
$ docker compose build

# Start all services
$ docker compose up

# Clean up to restart
$ docker compose down --volumes --remove-orphans
$ rm -rf '<DIRECTORY>'

# Stop and delete containers, delete volumes with database data and download images
$ docker compose down --volumes --rmi all
```
- Open Airflow UI via http://localhost:8080/
- Connect AWS S3 bucket in Airflow. Go to Admin > Connection and add following fields
   - Connection Id: s3_conn
   - Connection Type: Amazon Web Services
   - Extra: `{
        "aws_access_key_id": "your_access_key_id",
        "aws_secret_access_key": "your_secret_access_key"
        }`
- Run DAG `en_species_etl`

### Dashboard

**Tools**: streamlit

**Objective**: Visualize data distribution using pie charts and other graphical representations

## Dataset

IUCN Red List: Provides conservation status for various species

IUCN 2024. IUCN Red List of Threatened Species. Version 2024-2 <www.iucnredlist.org>

[API documentation](https://api.iucnredlist.org/api-docs/index.html)
