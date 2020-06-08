import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = 'https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/chelm/q-dzia%C5%82ka-budowlana/?search%5Bfilter_enum_type%5D' \
      '%5B0%5D=dzialki-budowlane '
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id='body-container')
offers_promoted = results.find_all('td', class_="offer promoted")

offers_dict = {}
for offer in offers_promoted:
    name = offer.find('strong')
    price = offer.find('p', class_='price')
    link = offer.find('a')['href']
    if None in (name, price, link):
        continue

    offers_dict[name.text] = (price.text, link)

sorted_dict = {k: v for k, v in sorted(offers_dict.items(), key=lambda item: item[1][1])}
for k, v in sorted_dict.items():
    print(k, "-", end='')
    for i in range(len(v)):
        print(v[i])
