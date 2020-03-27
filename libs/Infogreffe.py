#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup											as bs
from selenium 								import webdriver 			as wd
from selenium.common.exceptions				import *
from selenium.webdriver.common.keys 		import Keys
from selenium.webdriver.common.by 			import By
from selenium.webdriver.firefox.options 	import Options
from selenium.webdriver.support.ui          import WebDriverWait
from selenium.webdriver.support             import expected_conditions  as EC 
from webdriver_manager.firefox 				import GeckoDriverManager

import time
import copy
import re




# Function that clean the href in order to get the href leading to the final web page.
def cleanHref(href_clean):
	re_clean = re.compile(r"^[\/(marques|societe)]*([\w]*)$")
	matches = re_clean.match(href_clean)

	#If the href contains the word "marques" or "societe", delete those words from it.
	if matches != None:
		href_clean = matches.groups()[0] 

	return href_clean



# Function that create a list the contains a certain number of dictionaries.
def createDict(number):
	dict_list = []

	for i in range(number):
		dictionary = {}
		dict_list.append(dictionary)

	return dict_list



# Functions that create correct URLs.
def getURNom_info(browser, company_name):
	#name = company_name.replace(" ", "+")
	url = "https://www.societe.com/cgi-bin/liste?nom="+company_name.upper()

	browser.get(url)


def getURLMarque_info(browser, company_name):
	#name = company_name.replace(" ", "+")
	url = "https://www.societe.com/cgi-bin/liste?marques="+company_name.upper()

	browser.get(url)


def getURLHeads_info(href):
	href_cleaned = cleanHref(href)

	url = "https://www.societe.com/dirigeants"+href_cleaned

	return url


def getURLChoosenCompany(browser, href):
	href_cleaned = cleanHref(href)

	url = "https://www.societe.com/etablissements"+href_cleaned

	browser.get(url)



#Function that lists all the results of the two first web pages of results.
#Return the href used to go to the page of the company the user has chosen.
def chooseCompany(browser, company_name):

	number_list = [] #List that contains the numero of the different choices of company.
	user_choice = None #The number that represents the result the user will choose from all the results.
	user_choice_int = 0
	chosen_company = None #The result the user will choose from all the results.
	href_chosen_company = None #The href of the page that contains more information about the chosen company.

	#Go to the fisrt page and get the results.
	getURNom_info(browser, company_name)
	result_dict1 = getResults_nom(browser)

	#Go to the second page, get the results and add them to the first dictionary (result_dict1).
	getURLMarque_info(browser, company_name)
	result_dict_final = getResults_marque(browser, result_dict1)
	

	#Ask the user to choose the company he/she wants to investigate.
	user_choice = input("Which company do you want to know about ? : ")

	#Create the list that contains the numero of the different choices of company.
	for i in range(1, len(result_dict_final)+1):
		number_list.append(str(i))


	#While the user does not enter a correct number : ask him/her again.
	while(user_choice not in number_list):
		print("Error : Please choose one between 1 and ", len(result_dict_final))
		user_choice = input("Which company do you want to know about ? : ")


	#Display the chosen company.
	chosen_company = result_dict_final[int(user_choice)]
	print("Chosen company :\n ", chosen_company, "\n")


	#There is one <a> tag before the <a> tags corresponding to the results.
	user_choice_int = int(user_choice)


	#Return to the page where the chosen result was.
	#If the user has chosen a company from the first web page :
	if int(user_choice) <= len(result_dict1):
		getURNom_info(browser, company_name)

	#If the user has chosen a company from the second web page :
	else:
		getURLMarque_info(browser, company_name)
		user_choice_int = user_choice_int - len(result_dict1)


	#BeautifulSoup parser
	html = browser.page_source
	soup = bs(html, 'html.parser')

	#Get the source code of the part where the results are listed.
	elements = soup.select_one("div#liste") 

	#If there is no result at all.
	if elements == None:
		print("We are enable to find general information about the company you are searching for.")
		quit()


	#Get the href corresponding to the chosen company, 
	#in order to have the URL leading to more information about this company.
	l = elements.find_all("a")
	liens = l[user_choice_int]
	href_chosen_company = liens["href"]

	return href_chosen_company	




# Function that creates a dictionary with the results on the first web page (see getURLNom_info).
def getResults_nom(browser):

	results_dict1 = {} #Dictionary that contains the results of the web search. 
	j = 1

	try:
		#Get a list of the results.
		results_list1 = browser.find_elements_by_class_name("resultat")

		#If there are less than 50 results:
		if len(results_list1) < 50:
			for i in range(len(results_list1)):
				if results_list1[i].text != "":
					print(j, ": ", results_list1[i].text.replace(">",""))
					print("\n")
					results_dict1[j] = results_list1[i].text.replace(">","")
					j += 1

		#If there are more than or exactly 50 results: limit the number of results to 50.
		else:
			for i in range(50):
				if results_list1[i].text != "":
					print(j, ": ", results_list1[i].text.replace(">",""))
					print("\n")
					results_dict1[j] = results_list1[i].text.replace(">","")
					j += 1

		return results_dict1

	except:
		return results_dict1



#Function that creates a dictionary with the results on the second web page (see getURLMarque_info).
def getResults_marque(browser, dictionary):

	j = (len(dictionary)) + 1

	#Independent copy of dictionary.
	results_dict2 = copy.deepcopy(dictionary)
   
	try:
		#Get a list of the results.
		results_list2 = browser.find_elements_by_class_name("resultat")


		#If there are less than 50 results:
		if len(results_list2) < 50:
			for i in range(len(results_list2)):
				if results_list2[i].text != "":
					print(j, ": ", results_list2[i].text.replace(">",""))
					print("\n")
					results_dict2[j] = results_list2[i].text.replace(">","")
					j += 1

		#If there are more than or exactly 50 results:
		else:
			for i in range(50):
				if results_list2[i].text != "":
					print(j, ": ", results_list2[i].text.replace(">",""))
					print("\n")
					results_dict2[j] = results_list2[i].text.replace(">","")
					j += 1

		return results_dict2

	except:
		return results_dict2



def getHeadsResults(browser, url):
	head_info_dict = {} #Dictionary that will contain information about the heads of the company.
	info = [] #List that will contain a certain number of dictionaries, one for each person.
	heads_title = [] #List for the role of the persons.
	heads_name = [] #List for the name of the persons.
	heads_date = [] #List for the date since when the person have been working in the company.
	heads_links = [] #List for the URLs leading to the web page where we can find the birth year of each person.
	heads_birthYear = [] #List for the birth each of the persons.

	browser.get(url)

	#BeautifulSoup parser
	html = browser.page_source
	soup = bs(html, 'html.parser')

	#If there is no page for the heads information : end the fonction by returning an empty dictionary.
	if soup.select_one("div#error") != None:
		return head_info_dict

	#If the page exists :
	else:
		heads_info = soup.select_one("div.Card.frame.table.FicheOldDirigeantsList")

		for element in heads_info.find_all("h4"):
			heads_title.append(element.contents[0])

		#Create l dictionaries, and add them in the list "info".
		l = len(heads_title)
		info = createDict(l)

		head_list = heads_info.find_all("a", {"class":"Link name"})
		if head_list != []:
			for element in head_list:
				heads_name.append(element.contents[0].replace("\n", "").replace("                        ", "").replace("                    ", "").replace("M ", ""))
		
		else:
			head_list = heads_info.find_all("span", {"class":"flex v-center"})
			if head_list != []:
				regex = re.compile(r"^(\w*\s*\w*)[G][\w\s\w-]*$")
				for element in head_list:
					match = regex.match(element.text.replace("\n", "").replace("                        ", "").replace("                    ", "").replace("M ", ""))
					if match != None:
						heads_name.append(match.groups()[0])


		head_list = heads_info.find_all("span", {"class":"ft-bold"})
		if head_list != []:
			for element in head_list:
				heads_date.append(element.contents[0])


		head_list = heads_info.find_all("table")
		if head_list != []:
			for element in head_list:
				if element.find("a") != None:
					heads_links.append(element.find("a")["href"])

		

		for i in heads_links:
			try:
				browser.get(i)
			except:
				break
			html = browser.page_source
			soup = bs(html, 'html.parser')
			cadre = soup.select_one("div#company_identity")
			if cadre != None:
				birth_year = cadre.find_all("p", {"class":"adressText"})
				if birth_year != None:
					heads_birthYear.append(birth_year[0].contents[0].replace("Né en ", "").replace("Née en  ", ""))

		

		#Put the information the final dictionary.
		if (heads_title != []):
			for i in range(l):
				if heads_name != []:
					info[i]["Nom"] = heads_name[i]
				if heads_birthYear != []:
					info[i]["Année de naissance"] = heads_birthYear[i]
				if heads_date != []:
					info[i]["Occupe ce poste depuis le"] = heads_date[i]
				head_info_dict[heads_title[i]] = info[i]

	return head_info_dict




# Return a list that contains all the information about the chosen company.
def getGeneralInfo(browser, company_name):
	results_list = []
	main_info = {}
	secondary_info = {}
	

	#Go to the web page to get more information about the chosen company.
	href = chooseCompany(browser,company_name)
	getURLChoosenCompany(browser, href)


	print("[*] Searching general information about "+company_name.upper()+".\n")


	#BeautifulSoup parser
	html = browser.page_source
	soup = bs(html, 'html.parser')


	#Get the part of the source code that contains all the results.
	results = soup.select_one("div#etabs")

	
	results_elements =  results.select(".Table.identity")

	for i in range(len(results_elements)):
		if i%2 != 0:
			results_list.append(results_elements[i])


	#Get the main information about the company.
	main_building = results_list[0]

	info = main_building.find_all("tr")

	if info != []:
		for line in info:
			info2 = line.find_all("td")
			if info2 != []:
				columns = [c.contents[0] for c in info2]
				if columns[0] in ["Dernière date maj", "N° d'établissement (NIC)", "Nature de l'établissement", "Code ape (NAF)", "Tranche d'effectif salarié"]:
					continue
				if columns[0] == "N° de SIRET":
					siret = columns[1].contents[0]
					main_info[columns[0]] = siret
				else:
					main_info[columns[0]] = columns[1]

	main_info["Adresse"] = main_info["Adresse"] + " " + main_info["Code postal"] + " " + main_info["Ville"] + ", " + main_info["Pays"]
	del main_info["Code postal"]
	del main_info["Ville"]
	del main_info["Pays"]

	#Add the information about the heads of the company in the main dictionary.
	head_url = getURLHeads_info(href)
	heads_info = getHeadsResults(browser, head_url)

	main_info.update(heads_info)

	#Get information about the other buildings the company may have.
	for i in range(1, len(results_list)):
		j = 0
		other_building = results_list[i]
		info = other_building.find_all("tr")
		if info != []:
			for line in info:
				info2 = line.find_all("td")
				if info2 != []:
					columns = [c.contents[0] for c in info2]
					if columns[0] in ["Complément d'adresse", "Dernière date maj", "N° d'établissement (NIC)", "Nature de l'établissement", "Date de création entreprise", "Code ape (NAF)", "Tranche d'effectif salarié", "Date de création établissement"]:
						continue
					#If the buildind is now closed : do not get the information about it.
					if columns[0] == "Statut":
						j = 1
						break
					elif columns[0] == "N° de SIRET":
						columns[0] += " de l'établissement secondaire "+str(i)
						siret = columns[1].contents[0]
						secondary_info[columns[0]] = siret
					else:
						columns[0] += " de l'établissement secondaire "+str(i)
						secondary_info[columns[0]] = columns[1]
		
		#If secondary_info exists for the current value of i, then concatenate the zip code, city and country to the adress.
		if j == 0:
			secondary_info["Adresse de l'établissement secondaire "+str(i)] = secondary_info["Adresse de l'établissement secondaire "+str(i)] + " " + secondary_info["Code postal de l'établissement secondaire "+str(i)] + " " + secondary_info["Ville de l'établissement secondaire "+str(i)] + ", " + secondary_info["Pays de l'établissement secondaire "+str(i)]
			del secondary_info["Code postal de l'établissement secondaire "+str(i)]
			del secondary_info["Ville de l'établissement secondaire "+str(i)]
			del secondary_info["Pays de l'établissement secondaire "+str(i)]

		#Add those information in the main dictionary.
		main_info.update(secondary_info)

	return main_info