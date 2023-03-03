from django.shortcuts import render


import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

# Create your views here.
def connectdb():
    client=MongoClient('localhost',27017)
    db_name = client["mydb"]
    collection=db_name['data']
    return client,db_name,collection


num=0

flist={'RAM':'','ROM':'','color':'','Camera':'','Battery':'','Processor':'','Year':'','Display':''}
    

def parse_name(raw_name,flist):
    flist=flist
    name,color,rom='', '',  ''
    if '(' in raw_name:
        pos=raw_name.index('(')
        name=raw_name[:pos]
        if ',' in raw_name:
            pos2=raw_name.index(',') 
            color=raw_name[pos+1:pos2] 
            rom=raw_name[pos2+1:len(raw_name)-1]
        elif 'GB' not in raw_name:
            pos2=raw_name.index(')')
            color=raw_name[pos+1:pos2] 
    else:
        name=raw_name
    flist['color']=color
    flist['ROM']=rom
    return name,flist


#feature_list has the whole raw description RAM,ROM,camera etc
def get_features(feature_list):
    #seperate all raw features with 'li'  
    lst=feature_list.find_all('li')
    #extract feature texts from raw
    newlst=[]
    for i in lst:
        newlst.append(i.text)
    templist=['Display','Camera','Battery','Processor','Year']
    
    for f in newlst:
        #extract RAM ROM
        if 'RAM' in f:
            x=newlst[newlst.index(f)].split()
            rampos=x.index('RAM')
            flist['RAM'] =  x[rampos-2]
            if 'ROM' in f:
                rompos=x.index('ROM')
                flist['ROM'] =  x[rompos-2]
        #extract all other features
        for i in templist:
            if i in f:
                flist[i]=newlst[newlst.index(f)]
    return flist


def scrape_data(collection): 
    # client,db_name,collection = connectdb()
    for num in range(1,42): #there is just 41 page content for phones on flipkart
        print(num)
        response= requests.get('https://www.flipkart.com/search?q=mobile+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&page='+str(num))
        soup=BeautifulSoup(response.content,'html.parser')
        phones=soup.find_all('div',class_="_3pLy-c row")
        for phone in phones:
            flist={'RAM':'','ROM':'','color':'','Camera':'','Battery':'','Processor':'','Year':'','Display':''}
            mydict={}
            raw_name=phone.find('div',class_='_4rR01T').text
            name,flist=parse_name(raw_name,flist)
            rating=phone.find('div',class_='_3LWZlK')
            r=rating.text if rating is not None else ''
            p=phone.find('div',class_='_30jeq3 _1_WHN1')
            price=p.text if p is not None else ''
            price=''.join(re.findall('\d',price))
            featurelst=phone.find('div',class_='fMghEO')
            features=get_features(featurelst)
            mydict['name']=name
            mydict['rating']=r
            mydict['price']=price
            mydict['features']=features
            collection.insert_one(mydict)
            print('inserted ',name)
    return collection.find()

#  _3G6awp   for currently unavailable phones


# def get_features(feature_list):
#     return
'''
def parse_name(name1):
    if '(' in name1:
        pos=name1.index('(')
        name=name1[:pos]
        if ',' in name1:
                pos2=name1.index(',') 
                color=name1[pos+1:pos2] 
                rom=name1[pos2+1:len(name1)-1] 
    return name, color,rom
'''

def scrapeview(request):
    client,db_name,collection = connectdb()
    scrape_data(collection)
    return render(request,'home.html')

def HomeView(request):
    client,db_name,collection = connectdb()
    # col=scrape_data(collection)
    col=collection.find()
    return render(request,'home.html',{'data':col})
