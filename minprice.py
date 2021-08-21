import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
import tkinter
from tkinter import *
import difflib
from tinydb import TinyDB, Query


main = tkinter.Tk()
main.title("TODO")
main.geometry("500x700")
main.resizable(True, True)

background_image=tkinter.PhotoImage(file="download.png")
background_label = tkinter.Label(main, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


product_var=tkinter.StringVar()


def search_website():
	query=product_var.get().title()
	print(query)
	amazon = f"https://www.amazon.in/s?k={query}"
	try:
		amazon_tracer(amazon)
	except Exception as e:
		print(e)
		print("\n")
		pass

	# time.sleep(2)
	flip = f"https://www.flipkart.com/search?q={query}"
	try:
		flip_tracer(flip)
	except Exception as e:
		print(e)
		print("\n")
		pass

	# # time.sleep(2)
	croma=f"https://www.croma.com/search/?q={query}"
	try:
		croma_tracer(croma)
	except Exception as e:
		print(e)
		print("\n")
		pass
	# # time.sleep(2)
	rel=f"https://www.reliancedigital.in/search?q={query}"
	try:
		rel_tracer(rel)
	except Exception as e:
		print(e)
		print("\n")
		pass
	# # time.sleep(2)
	tata=f"https://www.tatacliq.com/search/?searchCategory=all&text={query}"
	try:
		tata_tracer(tata)
	except Exception as e:
		print(e)
		print("\n")
		pass


wait_imp = 0
CO = webdriver.ChromeOptions()
CO.add_experimental_option('useAutomationExtension', False)
CO.add_argument('--ignore-certificate-errors')
CO.add_argument('--start-maximized')
# CO.add_argument('disable-infobars')
# CO.add_argument('--headless');
wd = webdriver.Chrome(r'D:\applicatios\chrome-driver\chromedriver.exe',options=CO)
open('Product_details.json', 'w').close()
db = TinyDB('Product_details.json', sort_keys=False, indent=4, separators=(',', ': '))


print ("*************************************************************************** \n")
print("                     Starting Tracer, Please wait ..... \n")	

product = Label(main,
     text="Product Name", 
     background="#49A",
     foreground="#ffffff",
     font=("Calibri", 12),
     width =15,).pack(pady=5)
E1 = Entry(main,textvariable = product_var,bd =5,width=50).pack(pady=5)

submit = Button(main,
         text = "Get Details",
         background="#FFDAB9",
         foreground="#000000",
         font=("Calibri", 13),
         width =12,
         command=search_website).pack(pady=5) 

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

#Keyword to compare number of results 
class Numberofcomparisons:
	maxproducts=3

#function to store data in JSON Format
def insert_data_as_json(new_data):
	tb = db.table("Product")
	tb.insert(new_data)


# create a webdriver object for chrome-option and configure
def amazon_tracer(source1):
	product=[]
	print ("Connecting to Amazon")
	wd.get(source1)
	wd.implicitly_wait(wait_imp)
	pdata=wd.find_elements_by_xpath("""//*[@class="sg-col-inner"]/div/div/h2/a/span""")[:Numberofcomparisons.maxproducts]
	[product.append(x.text) for x in pdata]
	# print(product)
	x=product_var.get().title()
	suggested_product=match_product_among_four(product,x)
	index = product.index(suggested_product[0])
	link = wd.find_elements_by_xpath("""//*[@class="sg-col-inner"]/div/div/h2/a""")[index].get_attribute("href")
	Image_link = wd.find_elements_by_xpath("""//*[@class="s-image"]""")[index].get_attribute("src")
	item_price = wd.find_elements_by_xpath("""//*[@class="a-price-whole"]""")[index].text
	my_dict = { }
	my_dict["Website_Name"] = "Amazon"
	my_dict["Source_Link"] = source1
	my_dict["Website_Link"] = "https://www.amazon.in"
	my_dict["Product_Name"] = suggested_product[0]
	my_dict["Product_Link"] = link
	my_dict["Product_Price"] = item_price[0:]
	my_dict["Product_Image"] = Image_link
	my_dict["Product_Logo"] = "http://www.bizmonthly.com/wp-content/uploads/2020/04/Amazon-logo-black-template.png"
	# print(my_dict)
	insert_data_as_json(my_dict)
	print (" ---> Successfully retrieved the price from Amazon \n")


def flip_tracer(source1):
	print ("Connecting to Flipkart")
	product=[]
	wd.get(source1)
	wd.implicitly_wait(wait_imp)
	pdata=wd.find_elements_by_xpath("""//*[@class="_4rR01T"]""")[:Numberofcomparisons.maxproducts]
	[product.append(x.text) for x in pdata]
	# print(product)
	x=product_var.get().title()
	suggested_product=match_product_among_four(product,x)
	index = product.index(suggested_product[0])
	link = wd.find_elements_by_xpath("""//*[@class="_1fQZEK"]""")[index].get_attribute("href")
	Image_link = wd.find_elements_by_xpath("""//*[@class="CXW8mj"]/img""")[index].get_attribute("src")
	item_price = wd.find_elements_by_xpath("""//*[@class="_30jeq3 _1_WHN1"]""")[index].text
	my_dict = { }
	my_dict["Website_Name"] = "Flipkart"
	my_dict["Source_Link"] = source1
	my_dict["Website_Link"] = "https://www.flipkart.com/"
	my_dict["Product_Name"] = suggested_product[0]
	my_dict["Product_Link"] = link
	my_dict["Product_Price"] = item_price[1:]
	my_dict["Product_Image"] = Image_link
	my_dict["Product_Logo"] = "https://www.freepnglogos.com/uploads/flipkart-logo-png/flipkart-icon-23.png"
	# print(my_dict)
	insert_data_as_json(my_dict)
	print (" ---> Successfully retrieved the price from Flipkart \n")


def croma_tracer(source1):
	product=[]
	print ("Connecting to Croma")
	wd.get(source1)
	wd.implicitly_wait(wait_imp)
	pdata=wd.find_elements_by_xpath("""//*[@class="product-info"]/div/h3/a""")[:Numberofcomparisons.maxproducts]
	[product.append(x.text) for x in pdata]
	# print(product)
	x=product_var.get().title()
	suggested_product=match_product_among_four(product,x)
	index = product.index(suggested_product[0])
	link = wd.find_elements_by_xpath("""//*[@class="product-info"]/div/h3/a""")[index].get_attribute("href")
	Image_link = wd.find_elements_by_xpath("""//*[@class="product-img"]/a/img""")[index].get_attribute("src")
	item_price = wd.find_elements_by_xpath("""//*[@class="price-rating-wrap"]/div/span[1]/span[2]""")[index].text
	my_dict = { }
	my_dict["Website_Name"] = "Croma"
	my_dict["Source_Link"] = source1
	my_dict["Website_Link"] = "https://www.croma.com/"
	my_dict["Product_Name"] = suggested_product[0]
	my_dict["Product_Link"] = link
	my_dict["Product_Price"] = item_price[1:]
	my_dict["Product_Image"] = Image_link
	my_dict["Product_Logo"] = "https://zeevector.com/wp-content/uploads/2021/02/Croma-Logo-Vector.png"
	# print(my_dict)
	insert_data_as_json(my_dict)
	print (" ---> Successfully retrieved the price from Croma \n")

def rel_tracer(source1):
	product=[]
	print ("Connecting to reliance Digital")
	wd.get(source1)
	wd.implicitly_wait(wait_imp)
	pdata=wd.find_elements_by_css_selector("p.sp__name")[:Numberofcomparisons.maxproducts]
	[product.append(x.text) for x in pdata]
	# print(product)
	x=product_var.get().title()
	suggested_product=match_product_among_four(product,x)
	index = product.index(suggested_product[0])
	# print(index)
	link = wd.find_elements_by_xpath("""//*[@class="sp grid"]/a""")[index].get_attribute("href")
	Image_link = wd.find_elements_by_xpath("""//*[@class="sp__productbox"]/div[2]/div/img""")[index].get_attribute("src")
	item_price = wd.find_elements_by_xpath("""//*[@class="sc-bxivhb dmBTBc"]""")[index].text
	my_dict = { }
	my_dict["Website_Name"] = "Reliance digital"
	my_dict["Source_Link"] = source1
	my_dict["Website_Link"] = "https://www.reliancedigital.in/"
	my_dict["Product_Name"] = suggested_product[0]
	my_dict["Product_Link"] = link
	my_dict["Product_Price"] = item_price[1:]
	my_dict["Product_Image"] = Image_link
	my_dict["Product_Logo"] = "https://searchlogovector.com/wp-content/uploads/2020/04/reliance-digital-logo-vector.png"

	# print(my_dict)
	insert_data_as_json(my_dict)
	print (" ---> Successfully retrieved the price from Reliance Digital \n")

def tata_tracer(source1):
	print ("Connecting to tatacliq")
	product=[]
	wd.get(source1)
	wd.implicitly_wait(wait_imp)
	pdata=wd.find_elements_by_xpath("""//*[@class="ProductDescription__description"]""")[:Numberofcomparisons.maxproducts]
	[product.append(x.text) for x in pdata]
	# print(product)
	x=product_var.get().title()
	suggested_product=match_product_among_four(product,x)
	index = product.index(suggested_product[0])
	# print(index)
	link = wd.find_elements_by_xpath("""//*[@class="ProductModule__aTag"]""")[index+1].get_attribute("href")
	Image_link = wd.find_elements_by_xpath("""//*[@class="Image__base"]/img""")[index].get_attribute("src")
	item_price = wd.find_elements_by_xpath("""//*[@class="ProductDescription__discount ProductDescription__priceHolder"]/h3""")[index].text
	my_dict = { }
	my_dict["Website_Name"] = "TATACLIQ"
	my_dict["Source_Link"] = source1
	my_dict["Website_Link"] = "https://www.tatacliq.com/"
	my_dict["Product_Name"] = suggested_product[0]
	my_dict["Product_Link"] = link
	my_dict["Product_Price"] = item_price[1:]
	my_dict["Product_Image"] = Image_link
	my_dict["Product_Logo"] = "https://mma.prnewswire.com/media/958758/Tata_CLiQ_Logo.jpg?p=facebook"
	insert_data_as_json(my_dict)
	print (" ---> Successfully retrieved the price from tatacliq \n")



main.mainloop()
