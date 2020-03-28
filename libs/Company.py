#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Company:
	"Description of the company."

	#Constructor
	def __init__(self, p_name, p_domain):
		self._name = p_name
		self._domain = p_domain
		self._SIRET = None
		self._address = None
		self._activity = None
		self._tel = None
		self._date_registration = None
		self._dns_info = {}
		self._emails = []
		self._leaked_emails = {}
		self._employees = []
		self._companies = []

	
	#Accessors
	def get_name(self):
		return self._name

	def get_domain(self):
		return self._domain

	def get_SIRET(self):
		return self._SIRET

	def get_activity(self):
		return self._activity

	def get_address(self):
		return self._address

	def get_tel(self):
		return self._tel

	def get_date(self):
		return self._date_registration

	def get_dns_info(self):
		return self._dns_info

	def get_emails(self):
		return self._emails

	def get_leaked_emails(self):
		return self._leaked_emails

	def get_employees(self):
		return self._employees

	def get_companies(self):
		return self._companies


	#Mutators
	def set_SIRET(self, p_SIRET):
		self._SIRET = p_SIRET

	def set_address(self, p_address):
		self._address = p_address

	def set_activity(self, p_activity):
		self._activity = p_activity

	def set_tel(self, p_tel):
		self._tel = p_tel

	def set_date(self, p_date):
		self._date_registration = p_date

	def set_dns_info(self, p_dns_info):
		self._dns_info = p_dns_info

	def set_emails(self, p_emails):
		self._emails = p_emails

	def set_leaked_emails(self, p_leaked_emails):
		self._leaked_emails = p_leaked_emails

	def set_employees(self, p_employees):
		self._employees.append(p_employees)

	def set_companies(self, p_companies, p_adress, p_SIRET):
		p_companies.set_SIRET(p_SIRET)
		p_companies.set_address(p_adress)

		self._companies.append(p_companies)


