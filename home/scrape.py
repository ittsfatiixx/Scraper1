#code to scape data from website
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
# from utils import get_db_handle
# mydict={'name':[],'rating':[],'price':[]}
client=MongoClient('localhost',27017)
db = client["mydb"]
collection=db['data_sample']

# flist={'RAM':'','ROM':'','color':'','Camera':'','Battery':'','Processor':'','Year':'','Display':''}


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



'''
4 GB RAM | 128 GB ROM | Expandable Upto 1 TB
Display  in  4 GB RAM |
 128 GB ROM | Expandable Upto 1 TB False
Camera  in  4 GB RAM | 128 GB ROM | Expandable Upto 1 TB False
Battery  in  4 GB RAM | 128 GB ROM | Expandable Upto 1 TB False
Processor  in  4 GB RAM | 128 GB ROM | Expandable Upto 1 TB False
Year  in  4 GB RAM | 128 GB ROM | Expandable Upto 1 TB False
Display  in  50MP + 2MP + 2MP | 16MP Front Camera False
Camera  in  50MP + 2MP + 2MP | 16MP Front Camera True
{'ram': '4', 'rom': '128', 'color': '', 'Camera': '50MP + 2MP + 2MP | 16MP Front Camera', 'Battery': '', 'Processor': 'Qualcomm Snapdragon 680 Processor', 'Year': '', 'Display': ''}
Camera
Processor  in  50MP + 2MP + 2MP | 16MP Front Camera False
Year  in  50MP + 2MP + 2MP | 16MP Front Camera False
Display  in  Qualcomm Snapdragon 680 Processor False
Battery  in  Qualcomm Snapdragon 680 Processor False
Processor  in  Qualcomm Snapdragon 680 Processor True
{'ram': '4', 'rom': '128', 'color': '', 'Camera': '50MP + 2MP + 2MP | 16MP Front Camera', 'Battery': '', 'Processor': 'Qualcomm Snapdragon 680 Processor', 'Year': '', 'Display': ''}
Processor
'''


response= requests.get('https://www.flipkart.com/search?q=mobile+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY')
soup=BeautifulSoup(response.content,'html.parser')
phones=soup.find_all('div',class_="_3pLy-c row")
names=soup.find_all('div',class_="_4rR01T")

prices=soup.find_all('div',class_="_30jeq3 _1_WHN1")
for phone in phones:
    flist={'RAM':'','ROM':'','color':'','Camera':'','Battery':'','Processor':'','Year':'','Display':''}
    mydict={}
    raw_name=phone.find('div',class_='_4rR01T').text
    name,flist=parse_name(raw_name,flist)
    rating=phone.find('div',class_='_3LWZlK')
    r=rating.text if rating is not None else ''
    price=phone.find('div',class_='_30jeq3 _1_WHN1').text
    price=''.join(re.findall('\d',price))
    featurelst=phone.find('div',class_='fMghEO')
    features=get_features(featurelst)
    mydict['name']=name
    mydict['rating']=r
    mydict['price']=int(price)
    mydict['features']=features
    collection.insert_one(mydict)


# print(mydict)
cols=collection.find()
for item in cols:
    print(item)




