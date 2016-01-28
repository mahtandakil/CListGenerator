#!/usr/bin/python
# -*- coding: latin-1 -*-
#****************************************************************************
# Created for: SDLApi v2
# Dev line: AGE v2
# Creation day: 11/01/2016
# Last change: 11/01/2016
#***************************************************************************/

import os
from app.util import *


#-----------------------------------------------------------------------

class Menu():
	
	def __init__(self):
		
		self.initValues()
		
		
#-----------------------------------------------------------------------

	def initValues(self):

		self.options = []
		self.selection = ""


#-----------------------------------------------------------------------

	def selectFiles(self):
		
		self.searchFiles(os.path.join(".", "sources"))
		self.selectOption()

		return self.selection
		

#-----------------------------------------------------------------------

	def searchFiles(self, source):
		
		for element in os.listdir(source):

			if element[-4:] == ".cls":				
				self.options.append(os.path.join(source, element))

			if os.path.isdir(element):
				self.searchFiles(os.path.join(source, element))

		self.options.sort()
		

#-----------------------------------------------------------------------

	def selectOption(self):

		counter = 1
		selection = -1

		while selection == -1:
			
			clear()

			print "SELECT FILE"
			print

			counter = 1
			
			for file_path in self.options:
				
				print str(counter) + ". " + file_path[2:]
				counter += 1

			print
			selection = int(raw_input("> "))
			selection -= 1
			
			if selection>=0 and selection<len(self.options):
				self.selection = self.options[selection]
			
			else:
				selection = -1
				
				
#-----------------------------------------------------------------------



