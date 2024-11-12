import sys
import os
import requests
from pathlib import Path

DOMAIN = 'https://api.iucnredlist.org'
TOKEN = os.environ.get('IUCN_API')
if not TOKEN:
    print('IUCN token does not exists!')
    sys.exit()
print(TOKEN)
HEADERS = {'Authorization': TOKEN}
DATA_DIR = Path('./data')

if os.path.exists(DATA_DIR) == False:
    os.mkdir(DATA_DIR)

def pull_species():
    """Returns a list of comprehensive groups.
    """
    try:
        r = requests.get(DOMAIN + f'/api/v4/biogeographical_realms', headers=HEADERS)
        print(r.text)
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    

def main():
    pull_species()


if __name__ == '__main__':
    main()