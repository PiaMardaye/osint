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



# Function that create a list the contains a certain number of dictionaries.
def createDict(number):
	dict_list = []

	for i in range(number):
		dictionary = {}
		dict_list.append(dictionary)

	return dict_list



def getHeadsResults2(browser, url):
	head_info_dict = {}
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
		return head_info_dict

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
			head_info_dict[element.contents[0]] = {}
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
					#Keep only the physical person and not moral person.
					name_clean = name.contents[0].replace("\n", "").replace("                        ", "").replace("                    ", "")

					#Get only a name with 2 words (ex : Frederic DUPONT).
					matche1 = regex1.match(name_clean)

					#Get only a name with 3 words (ex : Frederic LE MOINE).
					matche2 = regex2.match(name_clean)

					if (matche1 != None) or (matche2 != None):
						if matche2 != None :
							dict_list[m]["name"] = matche2.groups()[0]
						
						else:
							dict_list[m]["name"] = matche1.groups()[0]	
						
						print(dict_list[m])
						
					 	#Get the age of each person.
						link = name["href"]
						print(link)

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
								dict_list[m]["Birth year"] = birth_year[0].contents[0].replace("Né en ", "").replace("Née en  ", "")
								print("OK.")
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

			
			#Add dict_list to the final dictionary.
			head_info_dict[titles[i]] = dict_list

			#Do the same for the next table.
			i += 1

	print(head_info_dict)




if __name__=="__main__":
	url = "https://www.societe.com/dirigeants/sa-hlm-ville-d-alencon-et-de-l-orne-le-logis-familial-096820121.html"

	#Launch Selenium without displaying the open browser.
	options = Options()
	options.headless = True
	browser = wd.Firefox(options=options)
	browser.minimize_window()
	browser.implicitly_wait(10)

	getHeadsResults2(browser, url)

	browser.quit()