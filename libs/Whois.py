#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

# Linux with whois package needed.
import subprocess

re_parse = re.compile(r"^([\w\- ]+):\s*([\w\-: ]+)")

def getWhois(domain):
    info = {}
    r = subprocess.run(["whois",domain], stdout=subprocess.PIPE)
    
    out = r.stdout.decode('utf-8')

    # Only the first paragraphe of the result.
    parag1 = out.split("\n\n")[1]

    for l in paraf1.split("\n"):
        m = re_parse.match(l)
        if m != None:
            g = m.groups()
            info[g[0]]=g[1]

    return info

inf = getWhois("esiea.fr")
print(inf["domain"])
print(inf["registrar"])
print(inf["source"])
print(inf["Expiry Date"])