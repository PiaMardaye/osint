#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def getEmails(company_domain):
	data = []

	#Search for emails.
	req = requests.get("https://api.hunter.io/v2/domain-search?domain=" + company_domain + "&api_key=120a3fe9378ed32c9fced6973f43cc85ede7fb5e")

	# Write the results in the file that had been created (useful for debug or get more information).
	fichier = open("emails.json", "w")
	fichier.write(req.text)

	#Parse data from Web request results.
	r = json.loads(req.text)

	#Only email parts contain most valuable information.
	emails = r["data"]["emails"]

	if emails != []:
		for e in emails:

			if e["first_name"] == None:
				if e["last_name"] != None:
					name = e["last_name"]
				else:
					name = "Unknown"

			elif e["last_name"] == None:
				if e["first_name"] != None:
					name = e["first_name"]
				else:
					name = "Unknown"

			else:
				name = e["first_name"] + " " + e["last_name"]

			data.append({
				"email":e["value"],
				"name": name,
				"position": e["position"],
				"twitter": True if e["twitter"] != None else False
			})

	else:
		return data

	return data

