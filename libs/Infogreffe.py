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
import os




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
	head_info_list = []
	titles = []
	to_remove = []
	i = 0
	regex1 = re.compile(r"^((M|MME)\s\w*\s\w*)")
	regex2 = re.compile(r"^((M|MME)\s\w*\s\w*\s\w*)")

	browser.get(url)

	#BeautifulSoup parser
	html = browser.page_source
	soup = bs(html, 'html.parser')

	#If there is no page for the heads information : end the fonction by returning an empty dictionary.
	if soup.select_one("div#error") != None:
		return head_info_list

	#If the page exists :
	else:
		heads_info = soup.select_one("div.Card.frame.table.FicheOldDirigeantsList")

		#All kind of results.
		all_results = heads_info.find_all("h4")

		#All the tables of results (one table for each kind of results).
		head_list = heads_info.find_all("table")
		

		#Number of tables.
		l = len(head_list)

		#i = 0 at the beginning and will increase by one every time.
		i = 0

		#Create a dictionary like this : {title1 : {}, title2 = {}, ...}.
		for element in all_results:
			titles.append(element.contents[0])
			
			#Table number i.
			table = head_list[i]

			#All the lines in table i.
			lines = table.find_all("tr")

			j = len(lines)
			dict_list = createDict(j)

			m = 0

			#For each line of the table :
			for element in lines:
				#First column of each line gives the name of the person.
				column = element.find("td")

				#Get the a tag that contain the names.
				name = column.find("a", {"class":"Link name"}) 

				if name != []:

					dict_list[m]["position"] = titles[i]
					#Keep only the physical person and not moral person.
					name_clean = name.contents[0].replace("\n", "").replace("                        ", "").replace("                    ", "")

					#Get only a name with 2 words (ex : Frederic DUPONT).
					matche1 = regex1.match(name_clean)

					#Get only a name with 3 words (ex : Frederic LE MOINE).
					matche2 = regex2.match(name_clean)

					if (matche1 != None) or (matche2 != None):
						if matche2 != None :
							dict_list[m]["name"] = matche2.groups()[0].replace("M ", "").replace("MME ", "")
						
						else:
							dict_list[m]["name"] = matche1.groups()[0].replace("M ", "").replace("MME ", "")
						
						
					 	#Get the age of each person.
						link = name["href"]

						try:
							browser.get(link)
						except:
							break

						html = browser.page_source
						soup = bs(html, 'html.parser')
						cadre = soup.select_one("div#company_identity")
						if cadre != None:
							birth_year = cadre.find_all("p", {"class":"adressText"})
				
							if birth_year != None:
								dict_list[m]["birthyear"] = birth_year[0].contents[0]
								
				m += 1


			#Add the empty elements from dict_list to the to_remove list.
			for k in range(j):
				if dict_list[k] == {}:
					to_remove.append(dict_list[k])

			#For each element in to_remove list, remove it from dict_list.
			l = len(to_remove)	
			if l != 0:
				for n in range(l):
					dict_list.remove(to_remove[n])

			
			#Add the elements of dict_list to the final list.
			for e in dict_list:
				head_info_list.append(e)

			#Do the same for the next table.
			i += 1

	return head_info_list



# Return a list that contains all the information about the chosen company.
def getGeneralInfo(browser, company_name):
	results_list = []
	main_info = {}
	secondary_info = {}
	

	#Go to the web page to get more information about the chosen company.
	href = chooseCompany(browser,company_name)
	getURLChoosenCompany(browser, href)

	time.sleep(2)
	os.system("clear")

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
	#heads_info = getHeadsResults(browser, head_url)

	#main_info.update(heads_info)

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

		main_info["href"] = href

	return main_info