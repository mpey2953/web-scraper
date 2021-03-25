#-------------------------------------------------------------------

# /usr/local/bin/python3
# coding: utf-8
# author: mpey2953
# date: march 20, 2021
# version: 1.0

#-------------------------------------------------------------------

import os
import time
import csv
from urllib.parse import urljoin
from process_request import ProcessRequest 

class URL(object):
	def __init__(self):
		self.pr = ProcessRequest()

	# export dict to csv
	def to_csv(self, items):
		keys = items[0].keys()
		with open('AR11816_Salt_Locations.csv', 'w', newline='') as output_file:
		    dict_writer = csv.DictWriter(output_file, keys)
		    dict_writer.writeheader()
		    dict_writer.writerows(items)

	# cleean item
	def clean_item(self, item):
		item = item.replace("\n", "").replace(",", ", ")
		item = " ".join(item.split())
		return item

	# parser items
	def parser_items(self, item):
		items = {}
		items["name"] = item['businessName']
		address = item['address']
		items["address"] = self.clean_item("{}, {} {} {}".format(
			address['storeAddressLine1'], 
			address['storeAddressLine2'] if address['storeAddressLine2'] else "", 
			address['storePostCode'], 
			address['storeLocality']))
		location = item['location']
		items['latitude'] = location['storeLocationLatitude']
		items['longitude'] = location['storeLocationLongitude']
		return items

	# start scraper
	def parser(self, parsed):
		items = {}
		items_lst = []	
		for item in parsed:
			if item['storeType'] == "Store":
				items = self.parser_items(item)
				items_lst.append(items)
				print(items)
				print("_____________________________________________________________")
		self.to_csv(items_lst)

	def main(self):
		url = "https://fiber.salt.ch/en/api/details/en/pointsofsale?_format=json" 
		response = self.pr.set_request(url)
		self.parser(response.json()['data'])

if __name__ == "__main__":
	URL().main()