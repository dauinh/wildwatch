import sys
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DOMAIN = 'https://api.iucnredlist.org/api/v4'
TOKEN = os.environ.get('IUCN_API')
if not TOKEN:
    print('IUCN token does not exists!')
    sys.exit()
HEADERS = {'Authorization': TOKEN}
DATA_DIR = Path('./data')

if os.path.exists(DATA_DIR) == False:
    os.mkdir(DATA_DIR)

def pull_realms():
    """Returns a list of List available biogeographical realms (e.g. Neotropical or Palearctic).
    """
    try:
        r = requests.get(f'{DOMAIN}/biogeographical_realms', headers=HEADERS)
        return r.json()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


if __name__ == '__main__':
    pull_realms()