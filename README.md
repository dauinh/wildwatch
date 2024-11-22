# wildwatch

The aim is to create a dashboard that:

1. Monitors endangered species populations over time.
2. Tracks species conservation status changes.
3. Provides visual insights into trends and factors affecting their survival, focusing on endangered species.

## TODO

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