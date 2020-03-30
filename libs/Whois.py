#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

# Linux with whois package needed.
import subprocess

#Regex1 for the function getWhois.
regex1 = re.compile(r"^([\w\- ]+):\s*([\w\-: ]+)")

#Regex2 for the expiry date in the function getWhois (2021-01-09T18:56:18Z --> 2021-01-09).
regex2 = re.compile(r"^(\d*-\d*-\d*)[\w][\d]*[:][\d]*[:][\d]*[\w]$")

def getWhois(domain):
    info = {}
    r = subprocess.run(["whois",domain], stdout=subprocess.PIPE)
    
    out = r.stdout.decode('utf-8')

    if out.count("No entries found") > 0:
        return info

    # Only the first paragraphe of the result.
    paraf1 = out.split("\n\n")[1]

    for l in paraf1.split("\n"):
        m = regex1.match(l)
        if m != None:
            g = m.groups()
            info[g[0]]=g[1]

    m = regex2.match(info["Expiry Date"])
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
