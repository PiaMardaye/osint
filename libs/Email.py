#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os
import requests
import json


def extract(dictionary):
	pass



def getEmails(company_name, company_domain):
	data = {}


	print("[*] Searching emails linked to "+company_name.upper()+".\n")

	# Create a file to put the results of the requests below in it.
	os.system("touch emails.json")

	#Search for emails.
	req = requests.get("https://api.hunter.io/v2/domain-search?company=" + company_name + "&api_key=120a3fe9378ed32c9fced6973f43cc85ede7fb5e")

	#Write the results in the file that had been created.
	fichier = open("emails.json", "w")
	fichier.write(req.text)

	#From json file to python dictionary.
	with open("emails.json") as json_file:
		results = json.load(json_file)



	return results