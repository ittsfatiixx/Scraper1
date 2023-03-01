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
num=0
def scrape_data(collection): 
    # client,db_name,collection = connectdb()
    for num in range(1,42): #there is just 41 page content for phones on flipkart
        print(num)
        response= requests.get('https://www.flipkart.com/search?q=mobile+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&page='+str(num))
        soup=BeautifulSoup(response.content,'html.parser')
        phones=soup.find_all('div',class_="_3pLy-c row")
        for phone in phones:
            mydict={}
            name1=phone.find('div',class_='_4rR01T').text
            name,color,rom=parse_name(name1)
            rating=phone.find('div',class_='_3LWZlK')
            r=rating.text if rating is not None else ''
            price=phone.find('div',class_='_30jeq3 _1_WHN1').text #'_30jeq3 _1_WHN1'
            featurelst=phone.find('div',class_='fMghEO').text
            features=get_features(featurelst)
            mydict['name']=name
            mydict['rating']=r
            mydict['price']=price
            mydict['features']=features
            collection.insert_one(mydict)
            print('inserted ',name)
    return collection.find()

def get_features(feature_list):
    return

def parse_name(name1):
    if '(' in name1:
        pos=name1.index('(')
        name=name1[:pos]
        if ',' in name1:
                pos2=name1.index(',') 
                color=name1[pos+1:pos2] 
                rom=name1[pos2+1:len(name1)-1] 
    return name, color,rom


def scrapeview(request):
    client,db_name,collection = connectdb()
    scrape_data(collection)
    return render(request,'home.html')

def HomeView(request):
    client,db_name,collection = connectdb()
    # col=scrape_data(collection)
    col=collection.find()
    return render(request,'home.html',{'data':col})
