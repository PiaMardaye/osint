#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from emailrep import EmailRep
import requests
import json


def getBreaches(email):
	url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + email
	key = "5488e632b6a24e3c8df0aebd15324f8f"
	headers = {"hibp-api-key":key}
	breaches = requests.get(url, headers=headers)
	breaches_list = json.loads(breaches.text)
	
	breaches_str = ""
	for i in breaches_list:
		print(i["Name"])
		breaches_str += i["Name"] + ", "

	print(breaches_str)

# emailrep = EmailRep('3ztcpnlra8cp8zktybanc7tkb1z2p1566jcqe6nz91oxye8q')
# r = emailrep.query("mardayeestelle@gmail.com")
# print(r)

getBreaches("mardayeestelle@gmail.com")