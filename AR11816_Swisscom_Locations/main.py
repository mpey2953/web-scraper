#-------------------------------------------------------------------

# /usr/local/bin/python3
# coding: utf-8
# author: mpey2953
# date: march 20, 2021
# version: 1.0

#-------------------------------------------------------------------

import os
import time
from urllib.parse import urljoin
import csv

from process_request import ProcessRequest 

class URL(object):
	def __init__(self):
		self.pr = ProcessRequest()

	# export dict to csv
	def to_csv(self, items):
		keys = items[0].keys()
		with open('AR11816_Swisscom_Locations.csv', 'w', newline='') as output_file:
		    dict_writer = csv.DictWriter(output_file, keys)
		    dict_writer.writeheader()
		    dict_writer.writerows(items)

	# cleean item
	def clean_item(self, item):
		item = item.replace(" ,", ",").replace(".", "")
		item = " ".join(item.split())
		return item

	# parser items
	def parser_items(self, item):
		items = {}
		items["name"] = "Swisscom " + self.clean_item(item['place_name'])
		items["address"] = self.clean_item("{} {}, {} {}".format(item['street'], item['street_number'], item['postal_code'], item['city']))
		items['latitude'] = item['lat_individual']
		items['longitude'] = item['lng_individual']
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

	def get_params(self):
		params = {
			"type": "getmoreplacedata",
			"locator_id": "69",
			"client_id": "66",
			"x1": "43.72042123780492",
			"x2": "49.379621985508464",
			"y1": "17.95300210156251",
			"y2": "-2.404663914062488",
			"radius": "200",
			"table_postfix": "swisscom",
			"lang": "en",
			"lat": "46.6339116",
			"lng": "8.5935627",
			"topic": "1",
			"services": ""
		}
		return params

	def main(self):
		url = "https://swisscom.locator.cloud/core_functions/ajaxdata.php" 
		response = self.pr.set_request(url, params=self.get_params())
		self.parser(response.json()['data'])

if __name__ == "__main__":
	URL().main()	