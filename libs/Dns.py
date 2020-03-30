#!/usr/bin/env python3
# -*- coding: utf-8 -

from bs4 import BeautifulSoup as bs 
import requests
import re
import shutil

#For debug only (Burpsuite).
proxyDict = { 
	"http" : "http://127.0.0.1:8080",
	"https" : "https://127.0.0.1:8080"
}


url = "https://dnsdumpster.com/"


#Create a session in order to keep the cookie.
s = requests.Session()
s.headers.update({"referer":url})


#Extract the name of the machine from a string.
# "10 test.domain.com." -> "test.domain.com"
def cleanDomain(tab):
	re_clean = re.compile(r"^(?:[\d\s]+)*([-\w\d.]+)\.$")
	for i in range(len(tab)):
		r = re_clean.match(tab[i]["domain"])
		if r != None:
			tab[i]["domain"] = r.groups()[0]



#Extract the domain name from a string.
# "test.domain.com." -> "domain.com" if domain.com is the domain name of the company.
def cleanDomain2(tab, liste, company_name, company_domain):
	re_clean = re.compile(r"^[\w]*[.](\w*.*\w*)$")
	for i in range(len(tab)):
		if tab[i]["domain"].count(company_name) > 0:
			r = re_clean.match(tab[i]["domain"])
			if r != None:
				if (r.groups()[0] not in liste) and (r.groups()[0] != company_domain):
					liste.append(r.groups()[0])

	return liste
	



#Extract a list of result from a table on the web site (dns record, mx record, host records).
def extract(s):
    table = []

    #For each line of the table :
    for l in s.find_all("tr"):
    	#Create a list of each column element of this line.
        a = [ c.contents[0] for c in l.find_all("td")]
        #Extract the information.
        table.append({
            "domain":str(a[0]),
            "ip":str(a[1]),
            "owner":str(a[2])
        })

    cleanDomain(table)
    return table


# MAIN FUNCTION
# Return a dictionary that contains all the DNS information about the chosen company.
def getDNSInfo(company_name, company_domain):
	results = {} #Dictionary that will _contain the results.
	domains_list = []
	empty_list = []

	#Go to the web page.
	req = s.get(url)
	soup = bs(req.text, 'html.parser')

	#Get the CSRF token named "csrfmiddlewaretoken".
	csrf_token = soup.find("input",{"name":"csrfmiddlewaretoken"})['value']

	data = {
		"csrfmiddlewaretoken" : csrf_token,
		"targetip" : company_domain
	}

	#POST request to get the DNS information.
	r = s.post(url, data=data)


	#Check if there is any result.
	if r.text.find("There was an error getting results. Check your query and try again") != -1:
		print("[-] No result found...")
		return None


	#BeautifulSoup parser
	soup = bs(r.text,'html.parser')


	#Find and extract the DNS results.
	a_dns = soup.find("a",{"name":"dnsanchor"})
	table_dns = a_dns.parent.next_sibling.next_sibling
	dns = extract(table_dns)
	list1 = cleanDomain2(dns, empty_list, company_name, company_domain)

	#Find and extract the MX results.
	a_mx = soup.find("a",{"name":"mxanchor"})
	table_mx = a_mx.parent.next_sibling.next_sibling
	mx = extract(table_mx)
	list2 = cleanDomain2(mx, list1, company_name, company_domain)

	#Find and extract the Hosts results.
	a_host = soup.find("a",{"name":"hostanchor"})
	table_host = a_host.parent.next_sibling.next_sibling
	hosts = extract(table_host)
	list3 = cleanDomain2(hosts, list2, company_name, company_domain)

	#Copy list3 in domains_list.
	domains_list = list(list3)

	#Get the graph (save it as a binary object).
	src_graph = soup.find("img",{"class":"img-responsive"})["src"]
	r = s.get(url+src_graph, stream=True)
	if r.status_code == 200:
		with open("graph_"+company_domain+".png","wb") as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)


	results = {"dns": dns, "mx" : mx, "host": hosts, "subdomains": domains_list}

	return results
