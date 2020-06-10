import requests
import locale
import pprint
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from time import sleep
from random import randint

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

URL = 'https://www.zameen.com/Homes/Karachi-2-1.html?price_max=3500000'
main_page = requests.get(URL)

#print(page.text)
#pp = pprint.PrettyPrinter()

#pp.pprint(page.text)

soup = BeautifulSoup(main_page.content, 'html.parser')

pages = soup.find_all('div', class_="_5f5a3b34")[0].find("span").text.strip()
text_to = pages.find('to')
text_of = pages.find('of')
text_Homes = pages.find('Homes')
per_page = locale.atoi(pages[text_to+2:text_of].strip())
num_homes = locale.atoi(pages[text_of+2:text_Homes].strip())
num_pages = int(int(num_homes)/int(per_page))

pages = np.arange(0,num_pages,1)
print("{} pages loaded successfully".format(num_pages))

Price_list =[]
Location_list = []
Beds_list = []
Baths_list =[]
Sq_yd_list = []
URL_list =[]

for page in pages:
    #value = input("Proceed to next page? (y/n)")
    #if value == "n":
    #    break
    #elif value == "y":
    sleep(randint(2,10))
    page = requests.get('https://www.zameen.com/Homes/Karachi-2-'+str(page)+'.html?price_max=3500000')
    page_soup = BeautifulSoup(page.content, 'html.parser')

    results = page_soup.find_all('li', class_= "ef447dde")

    for result in results:
        counter = []
        property_URL_start = str(result.find_all('a', class_="_7ac32433")[0]).find('href="')+6
        property_URL_end = str(result.find_all('a', class_="_7ac32433")[0]).find('.html')+5
        property_URL = "https://www.zameen.com"+str(result.find_all('a', class_="_7ac32433")[0])[property_URL_start:property_URL_end]
        URL_list.append(property_URL)

        if result.find('span', class_="f343d9ce")['aria-label']=="Listing price":
            Price = result.find('span', class_="f343d9ce").text.strip()
            Price_list.append(Price)
        else:
            Price = "Not available"
            Price_list.append(Price)
        if result.find('div',class_="_162e6469")['aria-label'] == "Listing location":
            Location = result.find('div',class_="_162e6469").text.strip()
            Location_list.append(Location)
        else:
            Location = "Not available"
            Location_list.append(Location)
        for all_tags in result.find_all('span',{"class":"b6a29bc0","aria-label":True}):
            if all_tags['aria-label'] == "Beds":
                Beds = all_tags.text.strip()
                Beds_list.append(Beds)
                counter.append("Beds")
            elif all_tags['aria-label'] == "Baths":
                Baths = all_tags.text.strip()
                Baths_list.append(Baths)
                counter.append("Baths")
            elif all_tags['aria-label'] == "Area":
                Sq_yd = all_tags.text.strip()
                Sq_yd_list.append(Sq_yd)
                counter.append("Sq_yd")
            else:
                Beds = "Not available"
                Beds_list.append(Beds)
                Baths = "Not available"
                Baths_list.append(Baths)
                Sq_yd = "Not available"
                Sq_yd_list.append(Sq_yd)

        if not "Beds" in counter:
            Beds = "Not available"
            Beds_list.append(Beds)
        if not "Baths" in counter:
            Baths = "Not available"
            Baths_list.append(Baths)
        if not "Sq_yd" in counter:
            Sq_yd = "Not available"
            Sq_yd_list.append(Sq_yd)

    #        print("Property URL: ",property_URL)
    #        print("Listing location: ",Location)
    #        print("Listing price: ",Price)
    #        print("Beds: ",Beds)
    #        print("Baths: ",Baths)
    #        print("Sq_yd: ",Sq_yd)
    #        print('\n')

            Beds = ""
            Baths = ""
            Sq_yd = ""


print("Price_list: ",len(Price_list))
print("Location_list: ",len(Location_list))
print("Beds_list: ",len(Beds_list))
print("Baths_list: ",len(Baths_list))
print("Sq_yd_list: ",len(Sq_yd_list))
print("URL_list: ", len(URL_list))

properties_data = pd.DataFrame({"Prices": Price_list,
                                "Location": Location_list,
                                "Number of Bedrooms": Beds_list,
                                "Number of Bathrooms": Baths_list,
                                "Area in sq. yards": Sq_yd_list,
                                "URL": URL_list})

print("All data retrieved")
properties_data.to_csv("Zameen_Khi_data.csv")

#print(soup.prettify())
