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



def startScan(name, domain_name):

	#------------------------------GENERAL INFORMATION------------------------------

	general_info = getGeneralInfo(browser, name)

	print("General information : \n", general_info, "\n")
	

	#--------------------------------DNS INFORMATION--------------------------------

	dns_info = getDNSInfo(name, domain_name)

	print("DNS information : \n", dns_info, "\n")


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
	startScan(data["name"], data["domain"])

	#Quit Selenium.
	browser.quit()