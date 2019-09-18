import requests
from bs4 import BeautifulSoup as bs
url = 'https://www.carsales.com.au'
product_url = url + "/cars/ferrari/"

#how you represent yourself for the website
response = requests.get(product_url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}) 

#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36''))

print(response.status_code) #requesnt might not get any info if it figures out im a bot 
#could be denial error 503 
print(response.content)
if response.status_code != 200:
    print("Error:" + str(response.status_code))
    exit(0)
else:
    print("Response:" + str(response.status_code))

def get_models(response):
    model_dict = {}
    html = response.content
    page_soup = bs(html, "lxml") #could be other parsers lmlx
    output = page_soup.find('ul',class_='default-facets')
    models = output.find_all('li',class_='facet-visible')
    links = {}


    stringLinks = ''
    for i in models:
        stringLinks = ''
        print(i, "thjis is i")

        x = i.find_all('a', href = True)#,class_='/cars/ferrari')
        y = x[0].text
        links[y] = x[0]['href']

        #print(type(x))
        #print(page_soup(x.text))
                #links = output.find_all('a', {'class':'/cars/ferrari/488spider/'})
    #print(models)
    #print(output)
    #print(links)
    #for i in (links):
        #print(models, 'models')
        #print(links, 'links')
    #    model_dict[links[i]] = links[i]['href']

    return links

def get_car_name(product):
    nameTag = product.find('a', {"data-webm-clickvalue":'sv-title'})
    print(nameTag)
    print(type(nameTag))
    name = nameTag.text
    return name
def get_product_price(product):
    priceTag = product.find('a', {"data-webm-clickvalue":'sv-price'})
    price = priceTag.text
    return price
def get_product_date(product):
    pass
def get_product_odometer(product):
    odometerTag = product.find('li',{'data-type':'Odometer'})
    odometer = odometerTag.text
    return odometer
def get_product_transmission(product):
    transmissionTag = product.find('li',{'data-type':'Transmission'})
    transmission = transmissionTag.text
    return transmission
def get_product_engine(product):
    EngineTag = product.find('li',{'data-type':'Engine'})
    Engine = EngineTag.text
    return Engine
def get_product_body_type(product):
    body_typeTag = product.find('li',{'data-type':'Body Style'})
    body_type = body_typeTag.text
    return body_type




import random
import time
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
def scrape(model, url, headers = header, response=response):
    car_dict = {}
    index = 1
    html = response.content
    for car, link in model.items():
        for page in range(1,9):

            wait_time = random.uniform(7,16)
            time.sleep(wait_time)
            print("Srapping:" + url + link + '&page=' + str(page))
            response = requests.get(url+link +  '&page=' + str(page), headers=header)
            page_soup = bs(html,"lxml")
            cars = page_soup.find_all('div', {'data-webm-make':'Ferrari'})

            if cars is None:
                break

            #price, model, date, odometer, transmission, bodytype
            car_models = {}
            for product in cars:
                car_models[index] = {
                    "car_name" : get_car_name(product),
                    "car_price" : get_product_price(product),
                    "car_date" : get_product_date(product),
                    "car_odometer" : get_product_odometer(product),
                    "car_transmission": get_product_transmission(product),
                    "car_bodytype" : get_product_body_type(product),
                    "car_engine" : get_product_engine(product)
                }
                index +=1
             #limit to one page
        #limit to one brand
    return car_models
model = get_models(response)
print(model)


cars = scrape(model, url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'})
print(cars)

import pandas as pd
df = pd.DataFrame(cars)
df = df.transpose()
df.to_csv("/Users/petrandreev/Desktop/webScraper/Cars.csv")

print(df.head)
#"/cars/results/?q=(And.Service.Carsales._.(Or.Make.Ferrari._.Make.Ferrari.))
#div.selected-facets
#div.facet-name
#<a class="clear-facet" href="/cars/results/?q=Service.Carsales."></a>


