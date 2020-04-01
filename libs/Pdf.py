#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from fpdf 	import FPDF 


class PDF(FPDF):
	"Création d'un PDF pour les résultats."

	def header(self):
		self.image('ESIEA_logo.png', 8, 8, 40)
		self.image('Logo_CNS_NOIR.jpg', 163, 7, 42)
		self.set_font('Times', 'B', 15)
		self.cell(80)
		self.ln(25)


	def footer(self):
		self.set_y(-15)
		self.set_font('Times', 'I', 8)
		self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


	def chapter_title(self, label):
		self.set_font("Times", 'B', 16)
		self.cell(0, 6, label, 0, 1, 'C')
		self.ln(6)


	def chapter_body(self, name):
		self.set_font("Times", '', 12)
		self.cell(0, 6, "Hey", 0, 1, 'L')
		self.ln()


	def print_chapter(self, num, title, name):
		self.add_page()
		self.chapter_title(num, title)
		self.chapter_body(name)