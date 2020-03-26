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

#PDF GENERATION
from fpdf import FPDF 

def checkPythonVersion():

	# Check the current version of Python
	if sys.version_info[0] < 3:
	    print("Please, use at least Python 3.6")
	    # Quit the program
	    exit()
	elif (sys.version_info[0] == 3) and (sys.version_info[1] < 6):
		print("Please, use at least Python 3.6")
		# Quit the program
		exit()


