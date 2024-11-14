import sys
import os
import requests
import csv

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DOMAIN = "https://api.iucnredlist.org/api/v4"

# Authorization token for IUCN API
TOKEN = os.environ.get("IUCN_API")
# if not TOKEN:
#     print("IUCN token does not exists!")
#     sys.exit()
HEADERS = {"Authorization": TOKEN}

# Download directory
DATA_DIR = Path("../../raw_data")


def testing():
    print('hello world')


def get_metatdata_en_species():
    """Returns total count and page count for list of endangered species."""
    try:
        r = requests.get(
            f"{DOMAIN}/red_list_categories/EN?year_published={datetime.now().year}",
            headers=HEADERS,
        )
        return int(r.headers['total-count']), int(r.headers['total-pages'])
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    

def get_en_species(page):
    """Returns a list of the latest assessments for endangered species."""
    try:
        r = requests.get(
            f"{DOMAIN}/red_list_categories/EN?page={page}&year_published={datetime.now().year}",
            headers=HEADERS,
        )
        return r.json()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


def get_assess(id):
    """Returns assessment data for a supplied assessment_id. 
    This endpoint returns the same assessment data that you would see on an assessment page 
    on the IUCN Red List website. Accepts both latest and historic assessment_id."""
    try:
        r = requests.get(
            f"{DOMAIN}/assessment/{id}",
            headers=HEADERS,
        )
        return r.json()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


def transform_assess(id, data):
    """Tranform JSON data into rows for CSV file."""
    return [
        id,
        [conser['code'] for conser in data['conservation_actions']],
        [(h['code'], h['majorImportance'], h['season']) for h in data['habitats']],
        [loc['code'] for loc in data['locations']],
        data['population_trend']['code'],
        data['possibly_extinct'],
        data['possibly_extinct_in_the_wild'],
        data['sis_taxon_id'],
        data['supplementary_info']['estimated_area_of_occupancy'],
        data['supplementary_info']['estimated_extent_of_occurence'],
        data['taxon']['kingdom_name'],
        [(thr['code'], thr['timing'], thr['scope'], thr['score'], thr['severity']) for thr in data['threats']],
        data['url']
    ]


def main():
    total_count, total_pages = get_metatdata_en_species()
    with open(Path(DATA_DIR / 'EN.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        fields = ['id', 'conservation_actions', 'habitats', 'locations', 'population_trend', 'possibly_extinct', 'possibly_extinct_in_the_wild', 'sis_taxon_id', 'estimated_area_of_occupancy', 'estimated_extent_of_occurence', 'taxon', 'threats', 'url']
        writer.writerow(fields)

    with open(Path(DATA_DIR / 'EN.csv'), 'a', newline='') as f:
        writer = csv.writer(f)
        for page in range(1, total_pages + 1):
            for assess in get_en_species(page)['assessments']:
                id = assess['assessment_id']
                data = get_assess(id)
                row = transform_assess(id, data)
                writer.writerow(row)
            print(f'Page {page} data downloaded!')


if __name__ == "__main__":
    main()