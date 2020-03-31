#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

# Linux with whois package needed.
import subprocess

#Regex1 for the function getWhois.
#regex1 = re.compile(r"^[\s]*([\w\- ]+):\s*([\w\-: ]+)")
regex1 = re.compile(r"^[\s]*([\w\- ]+):\s*([\w\-:. \/]+)")
regex2 = re.compile(r"^([\w\- ]+):\s*([\w\-: ]+)")

#Regex2 for the expiry date in the function getWhois (2021-01-09T18:56:18Z --> 2021-01-09).
regex3 = re.compile(r"^(\d*-\d*-\d*)[\w][\d]*[:][\d]*[:][\d]*[\w]$")

def getWhois(domain):
    info = {}
    r = subprocess.run(["whois",domain], stdout=subprocess.PIPE)
    
    out = r.stdout.decode('utf-8')

    if out.count("No entries found") > 0:
        return info

    #Two types of output exists with the Whois command : paraf0 treats one of them and paraf1, the other one.

    paraf0 = out.split("\n\n")[0]
    # Only the first paragraphe of the result.
    paraf1 = out.split("\n\n")[1]

    #"Domain Name:" only exists in the first type of output.
    if paraf0.count("Domain Name:") > 0:
        for l in paraf0.split("\n"):
            m = regex1.match(l)
            if m != None:
                g = m.groups()
                info[g[0]]=g[1] 

        if "Registry Expiry Date" in info:
            m = regex3.match(info["Registry Expiry Date"])
            if m != None:
                info["Registry Expiry Date"] = m.groups()[0]

        print("\t\tRegistrar : ", info["Registrar"])
        print("\t\tExpiry date : ", info["Registry Expiry Date"])


    #"hold:" only exists in the second type of output.
    elif paraf1.count("hold:") > 0:
        for l in paraf1.split("\n"):
            m = regex2.match(l)
            if m != None:
                g = m.groups()
                info[g[0]]=g[1]

        if "Expiry Date" in info:
            m = regex3.match(info["Expiry Date"])
            if m != None:
                info["Expiry Date"] = m.groups()[0]

        print("\t\tRegistrar : ", info["registrar"])
        print("\t\tSource : ", info["source"])
        print("\t\tExpiry date : ", info["Expiry Date"])



def getHost(company_domain):
    ip_adresses = []
    r = subprocess.run(["host",company_domain], stdout=subprocess.PIPE)
    out = r.stdout.decode('utf-8')

    if out == "":
        return ip_adresses

    #Create a list that contains each line of the result.
    lines = out.split("\n")

    #Keep only the ip adresses.
    for line in lines:
        if line.count("has address") == 1:
            ip_adress = line.split(" ")[3]
            ip_adresses.append(ip_adress)

    for i in range(len(ip_adresses)):
        print("\t\tIP adress ", str(i+1), " : ", ip_adresses[i])

