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
		with open('AR11816_Mobilezone_Locations.csv', 'w', newline='') as output_file:
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
		items["name"] = "Mobilezone " + item["name"]
		item = item['address']
		items["address"] = self.clean_item("{}, {} {}".format(item['street'], item['zipCode'], item['city']))
		items['latitude'] = item['latitude']
		items['longitude'] = item['longitude']
		return items

	# start scraper
	def parser(self, parsed):
		items = {}
		items_lst = []		
		for item in parsed:
			items = self.parser_items(item)
			items_lst.append(items)
			print(items)
			print("_____________________________________________________________")
		self.to_csv(items_lst)

	def main(self):
		url = "https://www.mobilezone.ch/data/de/handy-shop-reparatur/overview" 
		response = self.pr.set_request(url)
		self.parser(response.json()['data']['data'])

if __name__ == "__main__":
	URL().main()