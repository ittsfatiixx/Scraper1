
#   https://www.amazon.in/s?k=mobile+phones&page=3&crid=1BB5FR6QL6S8D&qid=1677875529&sprefix=mobile+phones%2Caps%2C226&ref=sr_pg_3
# for Amazon 

#  data-component-type="s-search-result"    for each phone data
# h2 > a > href value to go to th phone details.


#to get colors available,  <img> with class="imgSwatch" Alt=color name
# to get ram rom, <div> id=variation_size_name   <div> class=twisterTextDiv  usme ka p.text

# tr with class a-spacing-small po-model_name    td with class a-span9  .. for phone name
# <i> with class a-icon-star for rating as '4.1 out of 5 stars'


#code to scape data from website
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
# mydict={'name':[],'rating':[],'price':[]}
client=MongoClient('localhost',27017)
db = client["mydb"]
collection=db['data_sample']
