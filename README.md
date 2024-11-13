# wildwatch

The aim is to create a dashboard that:

1. Monitors endangered species populations over time.
2. Tracks species sightings or conservation status changes.
3. Provides visual insights into trends and factors affecting their survival, focusing on specific animals like penguins, crabs, or other endangered species.

## TODO

1. Data collection
- [x] Write Python scripts to pull data from API
- IUCN: Categories: `EN` - Endangered, `CR` - Critically Endangered
  - `conservation_actions`: `[<code>]`
  - `habitats`: `<code>`, `<majorImportance>`, `<season>`
  - `locations`: `<origin>:  <code>`
  - `population_trend`
  - `possibly_extinct`
  - `possibly_extinct_in_the_wild`
  - `sis_taxon_id`
  - `estimated_area_of_occupancy` (`supplementary_info`)
  - `estimated_extent_of_occurence` (`supplementary_info`)
  - `systems`
  - `taxon`: `<kingdom_name>`
  - `threats`: `[<code>, <timing>, <scope>, <score>, <severity>]`
  - `url`
- GBIF
- [x] Store in CSVs (AWS S3)
- [ ] Schedule scrips in Airflow for every 16 weeks ([Red List update](https://www.iucnredlist.org/assessment/updates#:~:text=To%20ensure%20a%20regular%20flow,at%20least%20twice%20each%20year.))

2. Data processing
- [ ] Use `pandas` for cleaning and transformation
- [ ] Use Airflow to create tasks (collect -> clean -> save)

3. Database
- [ ] Choose database (PostgreSQL with PostGIS or NoSQL)
- [ ] Write ETL process to load cleaned data into database

4. Data analysis
- [ ] State hypothesis 
- [ ] Use SQL to aggregate data
- [ ] Use `pandas` or Spark for tranformation

5. Data visualization

- Tools: Tableau/Power BI/Streamlit
- Components:
  - Species Population Trends: Line graphs showing population changes over time.
  - Geographic Distribution Map: Use latitude/longitude data to show sighting locations on a map.
  - Conservation Status Overview: Pie charts or bar graphs showing the distribution of conservation statuses (e.g., Endangered, Vulnerable).

- [ ] Connect data source to dashboard
- [ ] Build visualizations
- [ ] Add interactive filters

6. Deploy
- [ ] Deploy pipeline
- [ ] Deploy dashboard

## Dataset

1. IUCN Red List: Provides conservation status for various species

IUCN 2024. IUCN Red List of Threatened Species. Version 2024-2 <www.iucnredlist.org>

[API documentation](https://api.iucnredlist.org/api-docs/index.html)

2. GBIF (Global Biodiversity Information Facility): Offers datasets on species sightings with geographic coordinates, which can be filtered for endangered species.
3. NOAA: Use NOAA's datasets for environmental factors like ocean temperatures, which could help correlate with animal population trends.