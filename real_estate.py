'''
Author: Soroosh and Pouya
Date: 1/19/2019
Desc: Scarping Tool
Problems:
    1. too many if statements beutiful soup has 'find(text=Bedrooms)' option which may be a better way of doing this
    2. if something is missing it could stop the programs
    3. need delays or will get kicked off the server

Results:
    31/32 houses were captured
    it outputed https://www.mlslistings.com/Search/Result/26b18b9d-ae6e-424c-b7a6-3261a43e950d/2?view=list which is right but id didnt go through the code again to scrape it
    for 31 houes it took 2030.798 seconds or 33.847 minutes (thats with all the timouts not commented out I went through and commented out a bunch of the timeouts)
'''

import requests
from bs4 import BeautifulSoup
import csv
import time

# Put URL here:
urls = 'https://www.mlslistings.com/Search/Result/26b18b9d-ae6e-424c-b7a6-3261a43e950d/1?view=list'

# CSV name here
csv_file = open('mls3.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    [
        'address', 'price', 'listing_status', 'days_on_site', 'type', 'MLS_number', 'beds', 'baths', 'sq_ft_lot', 'garage', 'sq_ft', 'year_built', 'desc', 'bedrooms_desc', 'bathroom_desc',
        'kitchen_desc', 'dining_room_desc', 'family_room_desc', 'fireplace_desc', 'flooring_desc', 'laundry_desc', 'cooling_desc', 'heating_desc', 'roof_desc', 'fundation_desc', 'pool_desc',
        'style_desc', 'horse_property_desc', 'garage_desc', 'elementary_district_desc', 'high_school_district_desc', 'unit_levels_desc', 'sewer_desc', 'water_desc', 'hoa_fee_desc',
        'complex_amenities_desc', 'zoning_desc'
    ])
# API
while urls:
    payload = {
                'key': '10f2bf398f398075ba707a72d2909dfb', 'url':
                urls
              }

    r = requests.get('http://api.scraperapi.com', params=payload).text

    soup = BeautifulSoup(r, 'lxml')
# Looks at a page and extracts all of the variables listed below
    for houses in soup.find_all('div', class_='card card-block pt-1 pb-1 px-1'):
        try:
            address = houses.find('h5', class_='card-title font-weight-bold listing-address mb-25').text
            print(address)
            price = houses.find('span', class_='font-weight-bold listing-price d-block pull-left pr-25').text
            print(price)
            listing_status = houses.find('span', class_='listing-statusd-block pull-left pl-50 pr-1 status-marker status-active').text
            print(listing_status)
            days_on_site = houses.find('span', class_='listing-dom-block pull-left pl-25 ').text.strip(' Days on Site')
            print(days_on_site)
            type = houses.find('div', class_='listing-info clearfix font-size-sm line-height-base listing-type mb-25').text.strip()
            print(type)
            MLS_number = houses.find('span', class_='info-item-label d-block pull-left font-weight-bold').text
            print(MLS_number)
            beds = houses.find('span', class_='listing-info-item font-size-sm line-height-base d-block pull-left pr-50 listing-beds').span.text
            print(beds)
            baths = houses.find('span', class_='listing-info-item font-size-sm line-height-base d-block pull-left pr-50 listing-baths').span.string
            print(baths)
            sq_ft = houses.find('span', class_='font-weight-bold info-item-value d-block pull-left pr-25').text
            print(sq_ft)
            sq_ft_lot = houses.find('span', class_='listing-info-item font-size-sm line-height-base d-block pull-left pr-50 listing-lot-size').span.text
            print(sq_ft_lot)
            garage = houses.find('span', class_='listing-info-item font-size-sm line-height-base d-block pull-left pr-50 listing-garage').span.text
            print(garage)
            # Time delay of 2 seconds
            time.sleep(2)
            for sy in houses.find_all('span', class_='listing-info-item font-size-sm line-height-base d-block pull-left pr-50 listing-sqft last'):
                if sy.find('span', class_='info-item-label d-block pull-left').text == 'Sq Ft':
                    # Don't know why I hace two sq_ft but I think there is a valid reason
                    sq_ft = sy.span.text
                    print(sq_ft)
                elif sy.find('span', class_='info-item-label d-block pull-left').text == 'Year Built':
                    year_built = sy.span.text
                    print(year_built)
                else:
                    sq_ft = None
                    year_built = None
        except Exception as e:
            result = None
# Goes in each house link
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
            # There are three levels of information but the first two levels are consistent. Example: level 1 = Interior Features ===> levle 2 = Bedrooms ===> level 3 = is the description that is different for every house
            for cards in ss.find_all('div', class_='col-xs-12 px-0'):
                try:
                    # Looks for level 1
                    if cards.div.div.div.h5.text == 'About this Property':
                        # Level 3
                        desc = cards.div.div.div.findNext('div').p.text.replace(',', '')
                        #print(desc)
                        time.sleep(2)
                    # Looks for level 1
                    elif cards.div.div.div.h5.text == 'Interior Features':
                        for tt in cards.find_all('p', class_='card-title font-weight-bold mb-0 font-size-midr line-height-xl'):
                            # Looks for level 2
                            if tt.text == 'Bedrooms' and tt.findNext('p').text != '�':
                                # Looks for level 3
                                bedrooms_desc = tt.findNext('p').text.replace(',', '')
                                #print(bedrooms_desc)
                                #time.sleep(2)
                            elif tt.text == 'Bathrooms' and tt.findNext('p').text != '�':
                                bathroom_desc = tt.findNext('p').text.replace(',', '')
                                #print(bathroom_desc)
                                #time.sleep(2)
                            elif tt.text == 'Kitchen' and tt.findNext('p').text != '�':
                                kitchen_desc = tt.findNext('p').text.replace(',', '')
                                #print(kitchen_desc)
                                #time.sleep(2)
                            elif tt.text == 'Dining Room' and tt.findNext('p').text != '�':
                                dining_room_desc = tt.findNext('p').text.replace(',', '')
                                #print(dining_room_desc)
                                #time.sleep(2)
                            elif tt.text == 'Family Room' and tt.findNext('p').text != '�':
                                family_room_desc = tt.findNext('p').text.replace(',', '')
                                #print(family_room_desc)
                                #time.sleep(2)
                            elif tt.text == 'Fireplace' and tt.findNext('p').text != '�':
                                fireplace_desc = tt.findNext('p').text.replace(',', '')
                                #print(fireplace_desc)
                                #time.sleep(2)
                            elif tt.text == 'Flooring' and tt.findNext('p').text != '�':
                                flooring_desc = tt.findNext('p').text.replace(',', '')
                                #print(flooring_desc)
                                #time.sleep(2)
                            elif tt.text == 'Laundry' and tt.findNext('p').text != '�':
                                laundry_desc = tt.findNext('p').text.replace(',', '')
                                #print(laundry_desc)
                                #time.sleep(2)
                            elif tt.text == 'Cooling' and tt.findNext('p').text != '�':
                                cooling_desc = tt.findNext('p').text.replace(',', '')
                                #print(cooling_desc)
                                #time.sleep(2)
                            elif tt.text == 'Heating' and tt.findNext('p').text != '�':
                                heating_desc = tt.findNext('p').text.replace(',', '')
                                #print(heating_desc)
                                time.sleep(2)
                            else:
                                bedrooms_desc = None
                                bathroom_desc = None
                                kitchen_desc = None
                                dining_room_desc = None
                                family_room_desc = None
                                fireplace_desc = None
                                flooring_desc = None
                                laundry_desc = None
                                cooling_desc = None
                                heating_desc = None
                    # Looks for level 1
                    elif cards.div.div.div.h5.text == 'Exterior Features':
                        for tt in cards.find_all('p', class_='card-title font-weight-bold mb-0 font-size-midr line-height-xl'):
                            # Looks for level 2
                            if tt.text == 'Roof' and tt.findNext('p').text != '�':
                                # Looks for level 3
                                roof_desc = tt.findNext('p').text.replace(',', '')
                                #print(roof_desc)
                                #time.sleep(2)
                            elif tt.text == 'Foundation' and tt.findNext('p').text != '�':
                                fundation_desc = tt.findNext('p').text.replace(',', '')
                                #print(fundation_desc)
                                #time.sleep(2)
                            elif tt.text == 'Pool' and tt.findNext('p').text != '�':
                                pool_desc = tt.findNext('p').text.replace(',', '')
                                #print(pool_desc)
                                #time.sleep(2)
                            elif tt.text == 'Style' and tt.findNext('p').text != '�':
                                style_desc = tt.findNext('p').text.replace(',', '')
                                #print(style_desc)
                                #time.sleep(2)
                            elif tt.text == 'Horse Property' and tt.findNext('p').text != '�':
                                horse_property_desc = tt.findNext('p').text.replace(',', '')
                                #print(horse_property_desc)
                                time.sleep(2)
                            else:
                                roof_desc = None
                                fundation_desc = None
                                pool_desc = None
                                style_desc = None
                                horse_property_desc = None
                    # Looks for level 1
                    elif cards.div.div.div.h5.text == 'Parking, School, and Other Information' and tt.findNext('p').text != '�':
                        for tt in cards.find_all('p', class_='card-title font-weight-bold mb-0 font-size-midr line-height-xl'):
                            # Looks for level 2
                            if tt.text == 'Garage/Parking' and tt.findNext('p').text != '�':
                                # Looks for level 3
                                garage_desc = tt.findNext('p').text.replace(',', '')
                                #print(garage_desc)
                                #time.sleep(2)
                            elif tt.text == 'Elementary District' and tt.findNext('p').text != '�':
                                elementary_district_desc = tt.findNext('p').text.replace(',', '')
                                #print(elementary_district_desc)
                                #time.sleep(2)
                            elif tt.text == 'High School District' and tt.findNext('p').text != '�':
                                high_school_district_desc = tt.findNext('p').text.replace(',', '')
                                #print(high_school_district_desc)
                                #time.sleep(2)
                            elif tt.text == 'Unit Levels' and tt.findNext('p').text != '�':
                                unit_levels_desc = tt.findNext('p').text.replace(',', '')
                                #print(unit_levels_desc)
                                #time.sleep(2)
                            elif tt.text == 'Sewer' and tt.findNext('p').text != '�':
                                sewer_desc = tt.findNext('p').text.replace(',', '')
                                #print(sewer_desc)
                                #time.sleep(2)
                            elif tt.text == 'Water' and tt.findNext('p').text != '�':
                                water_desc = tt.findNext('p').text.replace(',', '')
                                #print(water_desc)
                                #time.sleep(2)
                            elif tt.text == 'HOA Fee' and tt.findNext('p').text != '�':
                                hoa_fee_desc = tt.findNext('p').text.replace(',', '')
                                #print(hoa_fee_desc)
                                #time.sleep(2)
                            elif tt.text == 'Complex Amenities' and tt.findNext('p').text != '�':
                                complex_amenities_desc = tt.findNext('p').text.replace(',', '')
                                #print(complex_amenities_desc)
                                time.sleep(2)
                            elif tt.text == 'Zoning' and tt.findNext('p').text != '�':
                                zoning_desc = tt.findNext('p').text.replace(',', '')
                                #print(zoning_desc)
                                time.sleep(2)
                            else:
                                garage_desc = None
                                elementary_district_desc = None
                                high_school_district_desc = None
                                unit_levels_desc = None
                                sewer_desc = None
                                water_desc = None
                                hoa_fee_desc = None
                                complex_amenities_desc = None
                                zoning_desc = None

                except Exception as e:
                    result = None

            csv_writer.writerow(
                [
                    address, price, listing_status, days_on_site, type, MLS_number, beds, baths, sq_ft_lot, garage, sq_ft, year_built, desc, bedrooms_desc, bathroom_desc,
                    kitchen_desc, dining_room_desc, family_room_desc, fireplace_desc, flooring_desc, laundry_desc, cooling_desc, heating_desc, roof_desc, fundation_desc, pool_desc,
                    style_desc, horse_property_desc, garage_desc, elementary_district_desc, high_school_district_desc, unit_levels_desc, sewer_desc, water_desc, hoa_fee_desc,
                    complex_amenities_desc, zoning_desc
                ])
    # Goes to next page if there are no more houses on the page it will break
    try:
        urls = 'https://www.mlslistings.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
    except Exception as e:
        break

    print(urls)

csv_file.close()
