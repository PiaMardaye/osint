#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from libs.Infogreffe		import *
from libs.Email				import *


class Employee:
	"Description d'un employé."

	#Constructor
	def __init__(self, p_name):
		self._name = p_name
		self._birthyear = None
		self._email = None
		self._breaches = None
		self._position = None
		self._debut = None
		self._twitter = False


	#Accessors
	def get_name(self):
		return self._name

	def get_birthyear(self):
		return self._birthyear

	def get_email(self):
		return self._email

	def get_breaches(self):
		return self._breaches

	def get_position(self):
		return self._position

	def get_debut(self):
		return self._debut

	def get_twitter(self):
		return self._twitter

		
	#Mutators
	def set_birthyear(self, p_birthyear):
		self._birthyear = p_birthyear

	def set_email(self, p_email):
		self._email = p_email

	def set_breaches(self, p_breaches):
		self._breaches = p_breaches

	def set_position(self, p_position):
		self._position = p_position

	def set_debut(self, p_debut):
		self._debut = p_debut

	def set_twitter(self, p_twitter):
		self._twitter = p_twitter