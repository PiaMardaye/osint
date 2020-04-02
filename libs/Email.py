#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import ast


#Get the web sites where the account corresponding to the given email has been part of a data breach.
def getBreaches(email):
	url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + email
	key = "5488e632b6a24e3c8df0aebd15324f8f"
	headers = {"hibp-api-key":key}

	breaches = requests.get(url, headers=headers)

	breaches_list = breaches.text.replace("[","").replace("]","").split('{"Name":')
	
	for i in range(1, len(breaches_list)):
		breaches_list[i] = breaches_list[i].replace('"', "").replace('}', "").replace(",", "")
	
	return breaches_list



#Get information about emails.
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

			breaches = ""
			breaches_list = getBreaches(e["value"])
			for i in range(1, len(breaches_list)):
				breaches += breaches_list[i] + ", "
			if breaches == "":
				breaches = "Aucune."
			
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
				"breaches": breaches,
				"position": e["position"],
				"twitter": True if e["twitter"] != None else False
			})

	else:
		return data

	return data

