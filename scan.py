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
from libs.Whois			   import *
from libs.Email			   import *
from libs.Company 		   import Company
from libs.Employee 		   import Employee 
from libs.Pdf 			   import PDF 



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



def generatePDF(data, dns_info, heads_info, company):
	p = 1

	pdf = PDF()	
	pdf.alias_nb_pages()

	pdf.add_page()
	pdf.set_font('Times', 'B', 30)
	pdf.cell(190, 150, "Résultats de l'OSINT", 0, 1, 'C')
	pdf.cell(0, -100, data["name"].upper(), 0, 1, 'C')
	
	#General information
	pdf.add_page()
	pdf.chapter_title("INFORMATIONS GENERALES")

	pdf.set_font("Times", "B", 16)
	pdf.cell(0, 10, "Bâtiment principal :", 0, 1)

	pdf.set_font('Times', '', 14)
	pdf.cell(0, 10, "Nom : " + company.get_name(), 0, 1)
	pdf.cell(0, 10, "Nom de domaine : " + company.get_domain(), 0, 1)
	pdf.cell(0, 10, "SIRET : " + company.get_SIRET(), 0, 1)
	pdf.cell(0, 10, "Adresse : " + company.get_address(), 0, 1)
	pdf.cell(0, 10, "Activité : " + company.get_activity(), 0, 1)
	pdf.cell(0, 10, "Date de création : " + company.get_date(), 0, 1)
	
	pdf.ln(3)

	companies_list = company.get_companies()
	for j in range(1, len(company.get_companies()) + 1):
		pdf.set_font("Times", "B", 16)
		pdf.cell(0, 10, "Bâtiment secondaire " + str(j) + " :", 0, 1)

		pdf.set_font('Times', '', 14)
		pdf.cell(0, 10, "SIRET : " + companies_list[p-1].get_SIRET(), 0, 1)
		pdf.cell(0, 10, "Adresse : " + companies_list[p-1].get_address(), 0, 1)
		p += 1



	#DNS Information
	pdf.add_page()
	pdf.chapter_title("INFORMATIONS DNS")

	pdf.set_font("Times", "B", 16)
	pdf.cell(0, 10, "A propos du nom de domaine :", 0, 1)

	whois_info = getWhois(data["domain"])
	ip_adresses = getHost(data["domain"])

	pdf.set_font('Times', '', 14)
	if "registrar" in whois_info:
		pdf.cell(0, 7, "Registrar : " + whois_info["registrar"], 0, 1)
	elif "Registrar" in  whois_info:
		pdf.cell(0, 7, "Registrar : " + whois_info["Registrar"], 0, 1)

	if "source" in  whois_info:
		pdf.cell(0, 7, "Source : " + whois_info["source"], 0, 1)

	if "Expiry Date" in  whois_info:
		pdf.cell(0, 7, "Expiry Date : " + whois_info["Expiry Date"], 0, 1)
	elif "Registry Expiry Date" in  whois_info:
		pdf.cell(0, 7, "Expiry Date : " + whois_info["Registry Expiry Date"], 0, 1)

	if ip_adresses != []:
		if len(ip_adresses) == 1:
			pdf.cell(0, 7, "Adresse IP :" + ip_adresses[0], 0, 1)
		else:
			for i in range(len(ip_adresses)):
				pdf.cell(0, 7, "Adresse IP " + str(i+1) + " :" + ip_adresses[i], 0, 1)
		pdf.ln(3)


	if dns_info["subdomains"] != []:
		pdf.set_font("Times", "B", 16)
		pdf.cell(0, 10, "Sous-domaines :", 0, 1)

		subdomains_list = company.get_subdomains() 
		for subdomain in subdomains_list:
			whois_info = getWhois(subdomain)
			ip_adresses = getHost(subdomain)
			pdf.set_font('Times', '', 14)
			pdf.cell(0, 7, "- " + subdomain, 0, 1)

			if "registrar" in whois_info:
				pdf.cell(0, 7, "	Registrar : " + whois_info["registrar"], 0, 1)
			elif "Registrar" in  whois_info:
				pdf.cell(0, 7, "	Registrar : " + whois_info["Registrar"], 0, 1)

			if "source" in  whois_info:
				pdf.cell(0, 7, "	Source : " + whois_info["source"], 0, 1)

			if "Expiry Date" in  whois_info:
				pdf.cell(0, 7, "	Expiry Date : " + whois_info["Expiry Date"], 0, 1)
			elif "Registry Expiry Date" in  whois_info:
				pdf.cell(0, 7, "	Expiry Date : " + whois_info["Registry Expiry Date"], 0, 1)

			if ip_adresses != []:
				if len(ip_adresses) == 1:
					pdf.cell(0, 7, "	Adresse IP :" + ip_adresses[0], 0, 1)
				else:
					for i in range(len(ip_adresses)):
						pdf.cell(0, 7, "	Adresse IP " + str(i+1) + " :" + ip_adresses[i], 0, 1)
			pdf.ln(4)			
		pdf.ln(3)		


	if dns_info["dns"] != []:
		pdf.set_font("Times", "B", 16)
		pdf.cell(0, 10, "Informations - DNS :", 0, 1)

		pdf.set_font('Times', '', 14)
		dns_list = company.get_dns_info()
		for dns in dns_list:
			pdf.cell(0, 7, "DNS : " + dns["domain"], 0, 1)
			pdf.cell(0, 7, "Adresse IP : " + dns["ip"], 0, 1)
			pdf.cell(0, 7, "Propriétaire : " + dns["owner"], 0, 1)
			pdf.ln(4)
		pdf.ln(3)	


	if dns_info["mx"] != []:
		pdf.set_font("Times", "B", 16)
		pdf.cell(0, 10, "Informations - Serveurs de messagerie :", 0, 1)

		pdf.set_font('Times', '', 14)
		mx_list = company.get_mx_info()
		for mx in mx_list:
			pdf.cell(0, 7, "Serveur MX : " + mx["domain"], 0, 1)
			pdf.cell(0, 7, "Adresse IP : " + mx["ip"], 0, 1)
			pdf.cell(0, 7, "Propriétaire : " + mx["owner"], 0, 1)
			pdf.ln(4)
		pdf.ln(3)


	if dns_info["host"] != []:
		pdf.set_font("Times", "B", 16)
		pdf.cell(0, 10, "Informations - Hôtes :", 0, 1)

		pdf.set_font('Times', '', 14)
		host_list = company.get_host_info()
		for host in host_list:
			pdf.cell(0, 7, "Serveur MX : " + host["domain"], 0, 1)
			pdf.cell(0, 7, "Adresse IP : " + host["ip"], 0, 1)
			pdf.cell(0, 7, "Propriétaire : " + host["owner"], 0, 1)
			pdf.ln(4)
		pdf.ln(3)

	pdf.add_page()
	pdf.chapter_title("GRAPHE - NOMS DE SERVEURS/HÔTES")
	pdf.image('graph_'+ data["domain"] + '.png', 10, 70, 190)



	#Employees informations
	pdf.add_page()
	pdf.chapter_title("INFORMATIONS EMPLOYES")

	pdf.set_font('Times', '', 14)
	if heads_info != []:
		employees_list = company.get_employees()
		for j in range(len(employees_list)):
			name = employees_list[j].get_name()
			if name != None:
				pdf.cell(0, 5, "Nom : " + name, 0, 1)
			else:
				pdf.cell(0, 5, "Nom : Inconnu.", 0, 1)

			birthyear = employees_list[j].get_birthyear()
			if birthyear != None:
				pdf.cell(0, 5, "Né(e) le : " + birthyear, 0, 1)
			else:
				pdf.cell(0, 5, "Né(e) le : Inconnu.", 0, 1)

			position = employees_list[j].get_position()
			if position != None:
				pdf.cell(0, 5, "Position : " + position, 0, 1)
			else:
				pdf.cell(0, 5, "Position : Inconnue.", 0, 1)

			email = employees_list[j].get_email()
			if email != None:
				pdf.cell(0, 5, "Email : " + email, 0, 1)
			else:
				pdf.cell(0, 5, "Email : Inconnu.", 0, 1)

			twitter = employees_list[j].get_twitter()
			if twitter != None:
				pdf.cell(0, 5, "Twitter : " + twitter, 0, 1)
			else:
				pdf.cell(0, 5, "Twitter : Inconnu.", 0, 1)
				
			pdf.ln(4)
		pdf.ln(3)

	#Generation of the PDF.
	pdf.output(data["name"] + '.pdf')




def startScan(data):
	i = 1
	k = 1

	#Create a company.
	c = Company(data["name"], data["domain"])


	#------------------------------------EMAILS-------------------------------------
	
	#Uncomment the second line only if it's necessary (Hunter.io offers only 50 requests/month).
	#emails = []
	emails = getEmails(data["domain"])


	#--------------------------------DNS INFORMATION--------------------------------

	dns_info = getDNSInfo(data["name"], data["domain"])


	#------------------------------GENERAL INFORMATION------------------------------

	#Get the general information.
	general_info = getGeneralInfo(browser, data["name"])
	heads_info = getHeadsResults(browser, getURLHeads_info(general_info["href"])) + emails


	#Fill the data of the company.
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

	if dns_info["subdomains"] != []:
		if dns_info["subdomains"] != []:
			for subdomain in dns_info["subdomains"]:
				c.set_subdomains(subdomain)

	if dns_info["dns"] != []:
		for info in dns_info["dns"]:
			c.set_dns_info(info)

	if dns_info["mx"] != []:
		for info in dns_info["mx"]:
			c.set_mx_info(info)

	if dns_info["host"] != []:
		for info in dns_info["host"]:
			c.set_host_info(info)

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

			c.set_employees(employee)

		else:
			continue


	#Generate the final PDF.
	generatePDF(data, dns_info, heads_info, c)



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