#!/usr/bin/python3

from os       import system
from sys      import exit
from time     import sleep
from pandas   import DataFrame, concat
from requests import get
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

sleep_time = 5

system("clear")

print("CYBERPUERTA WEBSCRAPING\n")
print("Extracting data, please wait...\n")

data = DataFrame(columns=["size", "proccessor", "proccessor_turbo", "ram", "hdd", "sku", "price"])

def extraction_product(page_number, product_number):
		options = Options()
		options.headless = True
		driver = webdriver.Firefox(options=options, executable_path="/usr/lib/firefox-esr/geckodriver")
	
		driver.get("https://www.cyberpuerta.mx/Computadoras/Laptops/%(page_number)s" %locals())
		link_laptop = driver.find_element_by_id('productList-%(product_number)s' %locals())
		link_laptop.click()

		driver.execute_script('$(".emdetails_attributes_showmore_box").slideDown();')

		labels  = [i.text for i in driver.find_elements_by_css_selector('td.label')]
		values  = [i.text for i in driver.find_elements_by_css_selector('td.value')]
		labels.append("sku")
		labels.append("precio")
		values.append(driver.find_element_by_css_selector('div.detailsInfo_right_artnum').text.replace("SKU: ", ""))
		values.append(driver.find_element_by_css_selector('span.priceText').text.replace("$ ", "").replace(",", ""))
		data_clean = []

		try:
			data_clean.append(values[labels.index("Diagonal de la pantalla")].replace("pulg.", ""))
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("Frecuencia del procesador")].replace(" GHz", "").replace(",", "."))
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("Frecuencia del procesador turbo")].replace(" GHz", "").replace(",", "."))
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("Memoria interna")].replace(" GB", ""))
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("Capacidad total de almacenaje")].replace(" GB", ""))
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("sku")])
		except:
			data_clean.append("Not found")
		try:
			data_clean.append(values[labels.index("precio")])
		except:
			data_clean.append("Not found")

		data_clean_df = DataFrame({"size":[data_clean[0]],
                                   "proccessor":[data_clean[1]],
                                   "proccessor_turbo":[data_clean[2]],
                                   "ram":[data_clean[3]],
                                   "hdd":[data_clean[4]],
                                   "sku":[data_clean[5]],
                                   "price":[data_clean[6]]})
		driver.close()
		return data_clean_df	


pages_range = [""]+list(range(2,41))

for page in pages_range:
	page_number = str(page)

	for product in range(1,17):
		product_number = str(product)
		new_data = extraction_product(page_number, product_number)
		data = concat([data, new_data], axis=0, sort=False, ignore_index=True)
		print("Page: "+page_number+" / "+"Product: "+product_number)

print(data)




