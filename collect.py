import sys
import os
import requests
import json
from pprint import pprint
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DOMAIN = "https://api.iucnredlist.org/api/v4"

# Authorization token for IUCN API
TOKEN = os.environ.get("IUCN_API")
if not TOKEN:
    print("IUCN token does not exists!")
    sys.exit()
HEADERS = {"Authorization": TOKEN}

# Download directory
DATA_DIR = Path("./data")
if os.path.exists(DATA_DIR) == False:
    os.mkdir(DATA_DIR)


def get_realms():
    """Returns a list of available biogeographical realms (e.g. Neotropical or Palearctic)."""
    try:
        r = requests.get(f"{DOMAIN}/biogeographical_realms", headers=HEADERS)
        return r.json()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


def get_en_species():
    """Returns a list of the latest assessments for endangered species."""
    try:
        r = requests.get(
            f"{DOMAIN}/red_list_categories/EN?year_published={datetime.now().year}",
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


if __name__ == "__main__":
    # print(get_en_species())
    data = get_assess(949716)
    with open(Path(DATA_DIR / 'sample_assess.json'), 'w') as f:
        json.dump(data, f)
    pprint(data)