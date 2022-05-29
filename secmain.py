import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

f = json.load(open('all-cards-20220521091445.json', 'rb'))
ln = []
pngs = []
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def run(item):
    if item["object"] == "card" and item["lang"] == "en" and "paper" in item["games"]:

        if item["layout"] in ['leveler', 'saga', 'modal_dfc', 'split', 'art_series', 'flip', 'scheme',
                              'adventure', 'normal', 'augment', 'meld', 'transform', 'class', 'planar', 'host']:

            if item["layout"] in ["transform", 'modal_dfc']:

                for jtem in item["card_faces"]:
                    pngs.append((jtem["image_uris"]["png"], jtem["name"]))

            elif item["layout"] == "art_series":
                pass

            else:
                pngs.append((item["image_uris"]["png"], item["name"]))


def main(item):
    name = item[1].replace("/", "").replace('"', '').replace('?', '')
    if not os.path.exists(f'images/{name}.ppm'):
        file = open(f'images/{name}.ppm', 'wb')
        file.write(session.get(item[0]).content)
        file.close()
        print(f'{pngs.index(item)}/{len(pngs)}')

if __name__ == '__main__':
    for item in f:
        run(item)

    for item in pngs:
        main(item)


