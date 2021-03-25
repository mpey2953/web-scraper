import sys
import time

import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

class ProcessRequest(object):
	def __init__(self):
		pass
	
	# msg script abruptly terminated		
	def script_terminated(self, msg):
		print("___________________________________________________________________________________")
		print("Number of failed attempts. Script abruptly terminated...due to the following error:")
		print("___________________________________________________________________________________")
		print(msg)
		sys.exit()

	def retry(self, n):
		N_ATTEMPS = 20
		WAIT_TIME = 15
		print("reconnecting...", flush=True)
		time.sleep(WAIT_TIME)
		return False if n == N_ATTEMPS else True

	# validate the status of the page
	def set_request(self, url, stream=None, params=None, headers=None):
		count = 0
		loop = True
		msg = ""
		while loop:
			try:
				if params is None:
					response = requests.get(url, timeout=60, headers=headers)
				else:
					response = requests.post(url, data=params, timeout=60)
				response.raise_for_status()
				loop = (response.status_code != 200)
			except requests.exceptions.HTTPError as httpErr: 
				msg = "Http Error: ", httpErr
			except requests.exceptions.ConnectionError as connErr: 
				msg = "Error Connecting: ", connErr
			except requests.exceptions.Timeout as timeOutErr: 
				msg = "Timeout Error: ", timeOutErr 
			except requests.exceptions.RequestException as reqErr: 
				msg = "Something Else: ", reqErr 
			if loop:
				print(msg)
				count = count + 1
				if not self.retry(count):
					self.script_terminated(msg)

		return response