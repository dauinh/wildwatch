# wildwatch

[Live dashboard](https://wildwatch.streamlit.app/)

This dashboard shows:
- Habitat Distribution: Analysis of the habitats of endangered species.
- Threat Analysis: Identification of key threats to endangered species.
- Conservation Actions: Overview of conservation efforts for species at risk.
- Country Ranking: Top 20 countries with the highest number of endangered species.

## Methods

#### Endangered species ETL pipelines

**Tools**: Airflow, pandas

**Objective**: 
- Extract data from IUCN official API
- Transform raw data into structured tables
- Upload data to AWS S3 for storage and further use

#### Dashboard

**Tools**: streamlit

**Objective**: Visualize data distribution using pie charts and other graphical representations

## Dataset

IUCN Red List: Provides conservation status for various species

IUCN 2024. IUCN Red List of Threatened Species. Version 2024-2 <www.iucnredlist.org>

[API documentation](https://api.iucnredlist.org/api-docs/index.html)
