#!/usr/bin/python
# -*- coding: latin-1 -*-
#****************************************************************************
# Created for: AGE v2
# Dev line: AGE v2
# Creation day: 11/01/2016
# Last change: 22/01/2016
#***************************************************************************/


from app.util import *


import os
import re
import shutil


#-----------------------------------------------------------------------

class Engine():
	
	def __init__(self):
		
		self.initValues()
		
		
#-----------------------------------------------------------------------

	#This function initializes the variables. Must be called every time
	#that a new CLS is used.
	
	def initValues(self):
		
		self.file_list = []
		self.cld_values = None
		self.checks = [["", ".h", "template_h.clc"], ["", ".cpp", "template_cpp.clc"], ["Index", ".h", "template_index_h.clc"], ["Index", ".cpp", "template_index_cpp.clc"]]
		self.FORARGSOPEN = "<<<FOR_ARGS>>>\n"
		self.FORARGSCLOSE = "<<</FOR_ARGS>>>\n"
		self.ER_ARG1 = ""
		self.ER_ARG2 = ""
		
		
#-----------------------------------------------------------------------

	#This is the main function for the generator. Starts the generation.
	def processSource(self, source):
		
		#Loads the options for the solution and the single code files.
		values = self.findData(source)
		self.searchFiles(values["SOURCE"])
		
		#The generator processes every CLC file one by one.
		for file_name in self.file_list:
			self.processCode(file_name, values)


#-----------------------------------------------------------------------

	#This function looks for the CLD files in the destination folder.
	def searchFiles(self, source):
		
		for element in os.listdir(source):

			if element[-4:] == ".cld":				
				self.file_list.append(os.path.join(source, element))

			if os.path.isdir(element):
				self.searchFiles(os.path.join(source, element))

		self.file_list.sort()


#-----------------------------------------------------------------------

	#This functions loads the options contained in a solution's file. The 
	#result can be a dicctionary or a list, depending on the 'search_style'
	#variable.
	
	def findData(self, source, search_style=0):
		
		result_dic = {}
		result_list = []
		args = []

		f = open(source)
		
		if search_style == 0:
			pattern1 = '(.*)=\"(.*)\"'
			pattern2 = '(.*)=\"(.*)\"'

		elif search_style == 1:
			pattern1 = '(.*)=\"(.*),(.*)\"'
			pattern2 = '(.*)=\"(.*),(.*)\"'
		
		
		for line in f:
			search1 = re.match(pattern1, line[:-1])
			search2 = re.match(pattern2, line[:-1])

			if search1 and search_style == 0:
				result_dic[search1.group(1)] = search1.group(2)
			
			elif search1 and search_style == 1:
				result_list.append([search1.group(1), search1.group(2), search1.group(3)])

		f.close()
		
		if search_style == 0:
			return result_dic
		
		elif search_style == 1:
			return result_list
			
		
#-----------------------------------------------------------------------

	#This is the main function for the single file generation.
	def processCode(self, file_path, values):
		
		self.cld_values = self.findData(file_path, 1)
		self.createLostCLCs(file_path, values)
		self.generateCode(file_path, values)
				

#-----------------------------------------------------------------------

	#This function check if the proper CLD files are contained in the destination
	#folder. If not, it creates a new one using the code templates located
	#in the "app" folder.

	def createLostCLCs(self, file_path, values):
		
		for check in self.checks:
			
			check_path = (file_path + check[0] + check[1] + ".clc").replace(".cld", "")
			
			if not fileExists(check_path):
			
				template_path = os.path.join(".", "app", check[2])
				shutil.copy(template_path, check_path)
				

#-----------------------------------------------------------------------

	#This functions uses the solution configuration for create the new code
	#files.
	
	def generateCode(self, file_path, values):
		
		for clc in self.checks:
			
			clc_path = (file_path + clc[0] + clc[1] + ".clc").replace(".cld", "")
			code_path = clc_path[:-4]
			code = []
			
			f = open(clc_path)
			for line in f:
				code.append(line)
			f.close()

			block = []
			tokens = self.tokenize(code)
			for token in tokens:
				block = code[token[2]-1:token[3]]
				block = self.generateArgsLoop(block);


#-----------------------------------------------------------------------

	#This function proccesses the ARG loops contained in the CLC files and 
	#creates a semi-generated code.

	def generateArgsLoop(self, code_lines):
		
		result = []
		
		for line in code_lines:
			
			line = line.replace(self.FORARGSOPEN, "")
			line = line.replace(self.FORARGSCLOSE, "")

			for opt in self.cld_values:
				
				if opt[0] == "ARG":

					comm = self.findARGCommands(line)
					line = self.generateArgCommand(line, comm, opt[1], opt[2])
					result.append(line)
		
		return result
		
		
#-----------------------------------------------------------------------

	def generateArgCommand(self, line, commands, arg_type, arg_name):
		
		line_len = len(line)
		diff = 0
		print "*", arg_name
		print line
		for comm in commands:
			
			if comm[0] == "ARG_NAME":
				line = "SUST"
				#line = line[:comm[2]-diff] + arg_name + line[comm[3]+1-diff:]

			#if comm[0] == "ARG_TYPE":
			#	line = line[:comm[2]-diff] + arg_type + line[comm[3]+1-diff:]

			#if comm[0] == "ARG_DEF":
			#	line = line[:comm[2]-diff] + arg_type + " " + arg_name + line[comm[3]+1-diff:]
			
			diff = line_len - len(line)
		print line
		print
		return line


#-----------------------------------------------------------------------

	def findARGCommands(self, code):
		
		comm_init = 0
		comm_end = 0
		result = []
		
		while not comm_init == -1:
		
			comm_init = code.find("<[ARG_", comm_end)
			comm_end = code.find(">", comm_init)
		
			label = code[comm_init:comm_end+1]
			command = label[label.find("[")+1:label.find("]")]
			
			mods = []
			mod_init = 0
			mod_end = 0
			
			while not mod_init == -1:
		
				mod_init = command.find("{", mod_end)
				mod_end = command.find("}", mod_init)
				
				if not mod_init == -1:
					mods.append(command[mod_init:mod_end])
			
			result.append([command, mods, comm_init, comm_end])
				
		return result


#-----------------------------------------------------------------------

	def tokenize(self, code):
		
		tokens = []
		count = 0
		problems = False
		count_problems = 0
		result = []
		level = -1
		
		for line in code:
			
			count+=1
			
			if line.find("<<<FOR_ARGS>>>") > -1:
				level+=1
				tokens.append(["forargs_open", count, level])

			elif line.find("<<</FOR_ARGS>>>") > -1:
				tokens.append(["forargs_close", count, level])
				level-=1
			
		for token in tokens:
			
			if token[0] == "forargs_open":
				count_problems += 1
		
			if token[0] == "forargs_open":
				count_problems -= 1

			if count_problems < 0:
				problems = True
		
		if not count_problems == 0:
			problems = True

		if problems:
			result.append("PROBLEMS")

		tokens = self.setHierarchy(tokens)

		return tokens
		

#-----------------------------------------------------------------------

	def setHierarchy(self, tokens):
		
		hierarchy = []
		level = -1
		ident = -1
		found = False


		for token in tokens:
						
			if token[0] == "forargs_open":
				level+=1
				ident+=1
				hierarchy.append([ident, level, token[1], -1])
		
			elif token[0] == "forargs_close":
				level-=1
		
		for count in range(0, len(hierarchy)):
			
			found = False
			
			for search in range(0, len(tokens)):

				if hierarchy[count][2] == tokens[search][1] and tokens[search][0] == "forargs_open":
					found = True
					
				if found == True and tokens[search][0] == "forargs_close" and tokens[search][2] == hierarchy[count][1]:
					found = False
					hierarchy[count][3] = tokens[search][1]
				
			
		return hierarchy


#-----------------------------------------------------------------------
