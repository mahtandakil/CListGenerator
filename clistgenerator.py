#!/usr/bin/python
# -*- coding: latin-1 -*-
#****************************************************************************
# Created for: SDLApi v1
# Dev line: AGE v2
# Creation day: 05/08/2015
# Last change: 10/02/2016
#
# Reserved words: 
#***************************************************************************/


import app.menu
import app.engine


import time


#############################################################################


if __name__ == "__main__":
	
	#The Menu class obtains the path to the CLS file
	menu = app.menu.Menu()
	source = menu.selectFiles()
	
	#The Engine class generates the new dynamic files
	obj = app.engine.Engine()
	obj.process(source)
	
	#A pause to check that everything it's ok
	print 
	raw_input(">")


#############################################################################
