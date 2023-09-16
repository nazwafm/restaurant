from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests


password = 'sparta'
cxn_str = f'mongodb+srv://test:{password}@cluster0.drj7way.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str, tlsCAFile=certifi.where())
db = client.dbsparta_plus_week3


driver = webdriver.Chrome()

url ='https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA'

driver.get(url)

sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)

access_token = 'pk.eyJ1IjoibmF6d2EwMiIsImEiOiJjbGxuNW14enkwZHE0M3BsNDE2bm5jMGhxIn0.9U-lBCWgoV5TvNHvGf0kYg'
long = -122.420679
lat = 37.772537

start = 0

seen ={}


for _ in range(5):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurants = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurants:
        busisness_name = restaurant.select_one('div[class*="businessName__"]')
        if not busisness_name:
            continue
        
        name = busisness_name.text.split('.')[-1].strip()


        if name in seen:
            continue

        seen[name] = True

        link = busisness_name.select_one('a')['href']
        link = 'https://www.yelp.com' + link
        
        categories_price_location = restaurant.select_one('div[class*="priceCategory__"]')
        spans = categories_price_location.select('span')
        categories = spans[0].text.strip()
        location = spans[-1].text.strip()
               
        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={access_token}"
        geo_response = requests.get(geo_url)
        geo_json = geo_response.json()
        if 'features' in geo_json and len(geo_json['features']) > 0:
            center = geo_json['features'][0]['center']
        else:
            center = None
    
        print(name, ',', categories, ',', location, ',', link)

        doc = {
            'name': name,  
            'categories': categories,
            'location': location,
            'link': link,
            'center': center,
        }
        db.restaurants.insert_one(doc)

    start += 10
    driver.get(f'{url}&start={start}')
    sleep(3)


driver.quit()