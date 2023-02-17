#code to scape data from website
import requests
from bs4 import BeautifulSoup
# from utils import get_db_handle
# mydict={'name':[],'rating':[],'price':[]}
from pymongo import MongoClient

client=MongoClient('localhost',27017)
db_name = client["mydb"]
collection=db_name['data']




response= requests.get('https://www.flipkart.com/search?q=mobile+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY')
soup=BeautifulSoup(response.content,'html.parser')
phones=soup.find_all('div',class_="_3pLy-c row")
names=soup.find_all('div',class_="_4rR01T")

# prices=soup.find_all('div',class_="_30jeq3 _1_WHN1")
for phone in phones:
    mydict={}
    name=phone.find('div',class_='_4rR01T').text
    rating=phone.find('div',class_='_3LWZlK').text
    price=phone.find('div',class_='_30jeq3 _1_WHN1').text
    mydict['name']=name
    mydict['rating']=rating
    mydict['price']=price
    collection.insert_one(mydict)

# print(mydict)
cols=collection.find()
for item in cols:
    print(item)