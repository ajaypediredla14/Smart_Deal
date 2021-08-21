import requests
import difflib
from bs4 import BeautifulSoup as soup
from tinydb import TinyDB, Query
import time



#Function to comapre first 4 results
def match_product_among_four(tracks, word):
    if(difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.4)):
        return difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.4)
    elif(difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.3)):
        return difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.3)
    elif( difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.2)):
        return difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.2)
    elif( difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.1)):
        return difflib.get_close_matches(word, tracks, n = 1,cutoff = 0.1)
    else:
        list1=[]
        list1.append(tracks[0])
        return list1


#function to store data in JSON Format
def insert_data_as_json(new_data):
    tb = db.table("Product")
    tb.insert(new_data)

#Keyword to compare number of results 
class Numberofcomparisons:
    maxproducts=3


#Amazon tracer to trace the prices from the amazon
def amazon_tracer(source1,query):
    product=[]
    print ("Connecting to Amazon")
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    r= requests.get(source1, headers=headers).content
    page=soup(str(r),"html.parser")
    pdata=page.find_all(class_="a-size-medium a-color-base a-text-normal")[:Numberofcomparisons.maxproducts]
    [product.append(x.text) for x in pdata]
    x=query
    suggested_product_name=match_product_among_four(product,x)
    index = product.index(suggested_product_name[0])
    product_img = page.find_all(class_="s-image")[index]
    product_price = page.find_all(class_="a-price-whole")[index]
    product_link = page.find_all(class_="a-link-normal a-text-normal")[index]
    my_dict = { }
    my_dict["Website_Name"] = "Amazon"
    my_dict["Source_Link"] = source1
    my_dict["Website_Link"] = "https://www.amazon.in"
    my_dict["Product_Name"] = suggested_product_name[0]
    my_dict["Product_Link"] = "https://www.amazon.in/"+product_link['href']
    my_dict["Product_Price"] = product_price.text
    my_dict["Product_Image"] = product_img['src']
    my_dict["Product_Logo"] = "http://www.bizmonthly.com/wp-content/uploads/2020/04/Amazon-logo-black-template.png"
    insert_data_as_json(my_dict)
    print (" ---> Successfully retrieved the price from Amazon \n")

#Flipkart tracer to trace the prices from the flipkart
def flip_tracer(source1,query):
    my_dict = { }
    product=[]
    print ("Connecting to Flipkart")
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    r= requests.get(source1, headers=headers).content
    page=soup(str(r),"html.parser")
    pdata=page.find_all(class_="_4rR01T")[:Numberofcomparisons.maxproducts]
    [product.append(x.text) for x in pdata]
    x=query
    suggested_product_name=match_product_among_four(product,x)
    index = product.index(suggested_product_name[0])
    product_img = page.find_all(class_="_396cs4 _3exPp9")[index]['src']
    product_price = page.find_all(class_="_30jeq3 _1_WHN1")[index].text[12:]
    product_link = "https://www.flipkart.com/"+page.find_all(class_="_1fQZEK")[index]['href']
    my_dict["Website_Name"] = "Flipkart"
    my_dict["Source_Link"] = source1
    my_dict["Website_Link"] = "https://www.flipkart.com/"
    my_dict["Product_Name"] = suggested_product_name[0]
    my_dict["Product_Link"] =  product_link
    my_dict["Product_Price"] = product_price
    my_dict["Product_Image"] = product_img
    my_dict["Product_Logo"] = "https://www.freepnglogos.com/uploads/flipkart-logo-png/flipkart-icon-23.png"
    insert_data_as_json(my_dict)
    print (" ---> Successfully retrieved the price from Flipkart \n")


#Croma tracer to trace the prices from the croma store
def croma_tracer(source1,query):
    product=[]
    print ("Connecting to Croma")
    r= requests.get(source1)
    json_data=r.json()
    [product.append(x["name"]) for x in json_data["products"][:Numberofcomparisons.maxproducts]]
    x=query
    print(x)
    suggested_product_name=match_product_among_four(product,x)
    index = product.index(suggested_product_name[0])
    product_img = json_data["products"][index]["plpImage"]
    product_price = int(json_data["products"][index]["price"]["value"])
    product_link = "https://www.croma.com"+json_data["products"][index]["url"]
    my_dict = { }
    my_dict["Website_Name"] = "Croma"
    my_dict["Source_Link"] = "https://www.croma.com/search/?q="+x
    my_dict["Website_Link"] = "https://www.croma.com/"
    my_dict["Product_Name"] = suggested_product_name[0]
    my_dict["Product_Link"] = product_link
    my_dict["Product_Price"] = product_price
    my_dict["Product_Image"] = product_img
    my_dict["Product_Logo"] = "https://zeevector.com/wp-content/uploads/2021/02/Croma-Logo-Vector.png"
    insert_data_as_json(my_dict)
    print (" ---> Successfully retrieved the price from Croma \n")


#Reliance tracer to trace the prices from the Reliance Digital
def rel_tracer(source1,query):
    product=[]
    print ("Connecting to Reliance Digital")
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    }
    r= requests.get(source1, headers=headers).content
    page=soup(str(r),"html.parser")
    pdata=page.find_all(class_="sp__name")[:Numberofcomparisons.maxproducts]
    [product.append(x.text) for x in pdata]
    x=query
    print(x)
    suggested_product_name=match_product_among_four(product,x)
    index = product.index(suggested_product_name[0])
    product_img = "https://www.reliancedigital.in"+page.find_all(class_="sp__productbox")[index].find("img").get("data-srcset")
    product_price = page.find_all(class_="sc-bxivhb dmBTBc")[index].text[12:]
    product_link = "https://www.reliancedigital.in"+page.find_all(class_="sp grid")[index].find("a")['href']
    my_dict = { }
    my_dict["Website_Name"] = "Reliance digital"
    my_dict["Source_Link"] = source1
    my_dict["Website_Link"] = "https://www.reliancedigital.in/"
    my_dict["Product_Name"] = suggested_product_name[0]
    my_dict["Product_Link"] = product_link
    my_dict["Product_Price"] = product_price
    my_dict["Product_Image"] = product_img
    my_dict["Product_Logo"] = "https://searchlogovector.com/wp-content/uploads/2020/04/reliance-digital-logo-vector.png"
    insert_data_as_json(my_dict)
    print (" ---> Successfully retrieved the price from Reliance Digital \n")


#TATA tracer to trace the prices from the TATAcliQ
def tata_tracer(source1,query):
    product=[]
    print ("Connecting to TATACLIQ")
    r= requests.get(source1)
    json_data=r.json()
    [product.append(x["productname"]) for x in json_data["searchresult"][:Numberofcomparisons.maxproducts]]
    x=query
    suggested_product_name=match_product_among_four(product,x)
    index = product.index(suggested_product_name[0])
    product_img = json_data["searchresult"][index]["imageURL"]
    product_price = int(json_data["searchresult"][index]["price"]["sellingPrice"]["doubleValue"])
    product_link = "https://www.tatacliq.com"+json_data["searchresult"][index]["webURL"]
    my_dict = { }
    my_dict["Website_Name"] = "TATACLIQ"
    my_dict["Source_Link"] = "https://www.tatacliq.com/search/?q="+x
    my_dict["Website_Link"] = "https://www.tatacliq.com/"
    my_dict["Product_Name"] = suggested_product_name[0]
    my_dict["Product_Link"] = product_link
    my_dict["Product_Price"] = product_price
    my_dict["Product_Image"] = product_img
    my_dict["Product_Logo"] = "https://mma.prnewswire.com/media/958758/Tata_CLiQ_Logo.jpg?p=facebook"
    insert_data_as_json(my_dict)
    print (" ---> Successfully retrieved the price from tatacliq \n")



#function to modify and send search queries to different websites
def search_website(product):
    product_var=product
    query=product_var.title()
    print(query)
    amazon = f"https://www.amazon.in/s?k={query}"
    try:
        amazon_tracer(amazon,query)
    except Exception as e:
        print(e)
        print("\n")
        pass


    flip = f"https://www.flipkart.com/search?q={query}"
    try:
        flip_tracer(flip,query)
    except Exception as e:
        print(e)
        print("\n")
        pass


    croma=f"https://api.croma.com/product/allchannels/v1/search?currentPage=0&query={query}%3Arelevance%3AZAStatusFlag%3Atrue&fields=FULL"
    try:
        croma_tracer(croma,query)
    except Exception as e:
        print(e)
        print("\n")
        pass

    rel=f"https://www.reliancedigital.in/search?q={query}"
    try:
        rel_tracer(rel,query)
    except Exception as e:
        print(e)
        print("\n")
        pass

    tata=f'https://prodsearch.tatacliq.com/products/mpl/search/?searchText={query}%3Arelevance%3AinStockFlag%3Atrue&isKeywordRedirect=false&isKeywordRedirectEnabled=true&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=qcnobypass&page=0&isPwa=true&pageSize=40&typeID=all'
    try:
        tata_tracer(tata,query)
    except Exception as e:
        print(e)
        print("\n")
        pass

#to store the data in json file
open('./Product_details.json', 'w').close()
db = TinyDB('Product_details.json', sort_keys=False, indent=4, separators=(',', ': '))

t1=time.time()
search_website("LG washing machine")
t2=time.time()

print(t2-t1)