import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options

client = MongoClient('mongodb://localhost:27017')

db = client['flight']
coll = db['traveloka']

options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome( options=options) 
driver.get("https://www.traveloka.com/en-id/holiday-stays/search?checkInDate=&checkOutDate=&totalGuest=0&geoId=101786&geoType=HOTEL_GEO&geoName=East%2520Kalimantan")

soup_base = BeautifulSoup(driver.page_source, 'html.parser')

# model
prices = []
time_departure = []
time_arrival = []
time_duration = []
plane_vendors = []

# price
for item in soup_base.find_all('div', class_='_27kIL'):
    price = str(item.get_text())
    price_int = int(''.join(price[3:-4].split('.')))
    prices.append(price_int)

# time
for index, item in enumerate(soup_base.find_all('div', class_='_32ZNg')):
    if ((index + 1) % 3 == 0):
        time_duration.append(str(item.get_text()))
    elif ((index + 2) % 3 == 0):
        time_arrival.append(str(item.get_text()))
    elif ((index + 3) % 3 == 0):
        time_departure.append(str(item.get_text()))

# plane vendor
for item in soup_base.find_all('div', class_='_2HE-b'):
    plane_vendors.append(str(item.get_text()))

zip_list = zip(plane_vendors, prices, time_departure, time_arrival, time_duration)

for item in zip_list:
    obj = {
        "plane_vendor": item[0],
        "price": item[1],
        "departure": item[2],
        "arrival": item[3],
        "duration": item[4],
        "source": {
            "source_id": 1,
            "source_name": "Traveloka"
        }
    }
    coll.insert_one(obj)