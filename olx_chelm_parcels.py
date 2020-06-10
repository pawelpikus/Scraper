import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

URL = 'https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/chelm/q-dzia%C5%82ka-budowlana/?search%5Bfilter_enum_type%5D' \
      '%5B0%5D=dzialki-budowlane '
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id='body-container')
offers_promoted = results.find_all('td', class_="offer promoted")
offers_regular = results.find_all('td', class_="offer")


def fetch_offer_details(offers):
    offers_dict = {}
    for offer in offers:
        name = offer.find('strong')
        price = offer.find('p', class_='price')
        link_tag = offer.find('a')
        if link_tag is None:
            continue
        link = link_tag['href']
        if (name, price) is None:
            continue
        price = price.text
        price = price.replace(" zł", "")
        price = "".join(price.split())
        price = int(price)
        name = name.text
        offers_dict[name] = (price, link)
    return offers_dict


def merge_dict(dict1, dict2):
    res = {**dict1, **dict2}
    return res


dict1 = fetch_offer_details(offers_promoted)
dict2 = fetch_offer_details(offers_regular)

parcels = merge_dict(dict1, dict2)

sorted_parcels = {k: v for k, v in sorted(parcels.items(), key=lambda item: item[1][0])}

for k, v in sorted_parcels.items():
    print("\n", k, "- ", end='')
    for i in range(len(v)):
        if isinstance(v[i], int):
            print(v[i], "zł")
        else:
            print(v[i])

input("Type any key to exit.")


