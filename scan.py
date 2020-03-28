#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SYS CALLS
import sys

# OS CALLS
import os

# JSON DUMPS AND SERIALIZATION
import json

# OS DETECTION
import platform
 
# TIME MANIUPLATIN
import time

# WEB REQUESTS
import requests

#ARGUMENTS PARSER
import getopt

#____PACKAGE_______________________________________OBJEECT_________________RENAME_
from selenium 								import webdriver 			as wd
from selenium.webdriver.firefox.options 	import Options
from selenium.webdriver.common.by 			import By
from selenium.webdriver.common.keys 		import Keys
from webdriver_manager.firefox 				import GeckoDriverManager
from bs4 									import BeautifulSoup 		as bs

#_____FILE_________________FUNCTIONS_
from libs.utils		       import *
from libs.Infogreffe       import *
from libs.Dns 			   import *
from libs.Email			   import *
from libs.Company 		   import Company
from libs.Employee 		   import Employee 



# Display an help message
def displayHelp():
	# Lines of the message
	lines = [
		"",
		"DO YOU NEED HELP ?",
		"",
		"Enter your arguments as follows:",
		"",
		"  ■ -h             or --help",
		'  ■ -n "<name>"    or --name="<name>"',
		'  ■ -d "<domain>"  or --domain="<domain>"',
		"",
	]
	# Print the final message
	print("\n".join(lines))



def parseArgs(argv):

	#Dictonary that will contain the name and the domain name of the company.
	data = {}

	try:
		opts, args = getopt.getopt(argv, 'hn:d:', ['help', 'name=', 'domain='])

	#If error : display help and quit the program.
	except getopt.GetoptError as e:
		displayHelp()
		print("Error : ", e)
		quit()

	#If there is no argument or there are not all the arguements required : display help and quit the program.
	if (len(argv) == 0) or (len(argv) < 4):
		displayHelp()
		print("Error: Please specify the name and the domain name of the company.")
		quit()


	for opt, arg in opts:

		#Display help
		if opt in ("-h", "--help"):
			displayHelp()
			quit()

		else:
			opt = opt.replace("-", "")

			key = None

			#If short option (n, d):
			if len(opt) == 1:
				if opt == "n": key = "name"
				elif opt == "d": key = "domain"

			#If long option (name, second_name, domain):
			else: 
				key = opt

			#Domain name check.
			if (key == "domain") and (arg.count(".") == 0):
					print("Error: Invalid domain name.")
					quit()

			#Add the key-value pair to data.
			data[key] = arg.strip()


	return data



def startScan(data):
	i = 1
	k = 1

	#Create a company.
	c = Company(data["name"], data["domain"])


	#------------------------------------EMAILS-------------------------------------
	
	emails = getEmails(data["domain"])

	# print("Emails : \n", emails, "\n")



	#------------------------------GENERAL INFORMATION------------------------------

	#Get the general information.
	general_info = getGeneralInfo(browser, data["name"])
	heads_info = getHeadsResults(browser, getURLHeads_info(general_info["href"])) + emails


	#Fill the data of the comany.
	if "N° de SIRET" in general_info:
		c.set_SIRET(general_info["N° de SIRET"])

	if "Adresse" in general_info:
		c.set_address(general_info["Adresse"])

	if "Libellé du code APE" in general_info:
		c.set_activity(general_info["Libellé du code APE"])

	if "Date de création entreprise" in general_info:
		c.set_date(general_info["Date de création entreprise"])

	while ("Adresse de l'établissement secondaire " + str(i) in general_info) or ("N° de SIRET de l'établissement secondaire " + str(i) in general_info) :
		cc = Company(data["name"], data["domain"])
		c.set_companies(cc, general_info["Adresse de l'établissement secondaire " + str(i)], general_info["N° de SIRET de l'établissement secondaire " + str(i)])
		i += 1

	for person in heads_info:
		if "name" in person:
			employee = Employee(person["name"])
			if "birthyear" in person:
				employee.set_birthyear(person["birthyear"])
			else:
				employee.set_birthyear("Unknown.")
			if "email" in person:
				employee.set_email(person["email"])
			else:
				employee.set_email("Unknown.")
			if "position" in person:
				employee.set_position(person["position"])
			else:
				employee.set_position("Unknown.")
			if "twitter" in person:
				if person["twitter"] != "False":
					employee.set_twitter("Has an account.")
				else:
					employee.set_twitter("No account.")
			else:
				employee.set_twitter("Unknown.")
		else:
			continue



	#Get the data of the company.
	print("\tGENERAL INFORMATION :")
	print("Name : ", c.get_name())
	print("Domain : ", c.get_domain())
	print("SIRET : ", c.get_SIRET())
	print("Address : ", c.get_address())
	print("Activity : ", c.get_activity())
	print("Date of registration : ", c.get_date())

	print("OTHER BUILDINGS :")
	for j in range(1, len(c.get_companies()) + 1):
		print("SIRET of secondary building ",k, " : ", c.get_companies()[k-1].get_SIRET())
		print("Adress of secondary building ",k, " : ", c.get_companies()[k-1].get_address())
		print("\n")
		k += 1




	#--------------------------------DNS INFORMATION--------------------------------

	# dns_info = getDNSInfo(data["name"], data["domain"])

	# print("DNS information : \n", dns_info, "\n")


	#----------------------------DOMAIN NAME INFORMATION----------------------------

	#TODO (Whois.net)




if __name__ == "__main__":

	checkPythonVersion()

	data = parseArgs(sys.argv[1:])

	#Launch Selenium without displaying the open browser.
	options = Options()
	options.headless = True
	browser = wd.Firefox(options=options)
	browser.minimize_window()
	browser.implicitly_wait(10)

	#BeautifulSoup parser
	html = browser.page_source
	soup = bs(html, 'html.parser')

	#Start of the scan.
	startScan(data)


	#Quit Selenium.
	browser.quit()