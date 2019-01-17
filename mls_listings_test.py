import requests
from bs4 import BeautifulSoup
#import csv
import time


urls = 'https://www.mlslistings.com/Search/Result/e080a603-4e2f-4a46-bb87-b383825b4d10/1?view=list'

while urls:
    payload = {
                'key': '10f2bf398f398075ba707a72d2909dfb', 'url':
                urls
              }

    r = requests.get('http://api.scraperapi.com', params=payload).text

    soup = BeautifulSoup(r, 'lxml')

    for each in soup.find_all('a', class_='search-nav-link prerender'):
        inside_links = (each.get('href'))
        link = inside_links.splitlines()

        for links in link:
            pay = {
                    'key': '10f2bf398f398075ba707a72d2909dfb', 'url':
                    'https://www.mlslistings.com' + links
                  }

            xx = requests.get('http://api.scraperapi.com', params=pay).text
            ss = BeautifulSoup(xx, 'lxml')
            for cards in ss.find_all('div', class_='col-xs-12 px-0'):
                try:
                    headings = {'Interior Features': '', 'Exterior Features': '', 'Parking, School, and Other Information': ''}
                    for heading in headings.keys():
                        head = cards.div.div.div.h5.find(text=heading)
                        if head is not None:
                            headings[heading] = head
                            names = {'Bedrooms': '', 'Pool': '', 'Garage/Parking': ''}
                            for tt in cards.find_all('p', class_='card-title font-weight-bold mb-0 font-size-midr line-height-xl'):
                                for name in names.keys():
                                    ky = tt.find(text=name).findNext('p').text.replace(',', '')
                                    if ky is not None:
                                        names[name] = name
                                        print(name)

                except Exception as e:
                    result = None

    try:
        urls = 'https://www.mlslistings.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
    except Exception as e:
        break

    print(urls)
