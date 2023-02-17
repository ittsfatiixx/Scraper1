from django.shortcuts import render


import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# Create your views here.
def connectdb():
    client=MongoClient('localhost',27017)
    db_name = client["mydb"]
    collection=db_name['data']
    return client,db_name,collection

def scrape_data(collection): 
    # client,db_name,collection = connectdb()
    response= requests.get('https://www.flipkart.com/search?q=mobile+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY')
    soup=BeautifulSoup(response.content,'html.parser')
    phones=soup.find_all('div',class_="_3pLy-c row")
    for phone in phones:
        mydict={}
        name=phone.find('div',class_='_4rR01T').text
        rating=phone.find('div',class_='_3LWZlK').text
        price=phone.find('div',class_='_30jeq3 _1_WHN1').text
        mydict['name']=name
        mydict['rating']=rating
        mydict['price']=price
        collection.insert_one(mydict)
    return collection.find()


def scrapeview():
    client,db_name,collection = connectdb()
    scrape_data(collection)

def HomeView(request):
    client,db_name,collection = connectdb()
    # col=scrape_data(collection)
    col=collection.find()
    return render(request,'home.html',{'data':col})
