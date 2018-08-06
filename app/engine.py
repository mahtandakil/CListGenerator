#!/usr/bin/python
# -*- coding: latin-1 -*-
#****************************************************************************
# Created for: AGE v2
# Dev line: AGE v2
# Creation day: 11/01/2016
# Last change: 17/07/2018
#***************************************************************************/


from app.util import *


import os
import re
import shutil
import time

from datetime import date


#-----------------------------------------------------------------------

class Engine():
	
	def __init__(self):
		
		self.initValues()
		
		
#-----------------------------------------------------------------------

	#This function initializes the variables. Must be called every time
	#that a new CLS is used.
	
	def initValues(self):
		
		self.file_list = []
		self.cls_values = None
		self.cld_values = None
		self.cld_base_name = ""
		self.checks = [["", ".h", "template_h.clc"], ["", ".cpp", "template_cpp.clc"], ["Index", ".h", "template_index_h.clc"], ["Index", ".cpp", "template_index_cpp.clc"]]
		self.FORARGSOPEN = "<<<FOR_ARGS"
		self.FORARGSCLOSE = "<<</FOR_ARGS"
		self.FORARGSBASEOPEN = "<<<FOR_BASE&ARGS"
		self.FORARGSBASECLOSE = "<<</FOR_BASE&ARGS"
		self.ER_ARG1 = ""
		self.ER_ARG2 = ""
		self.base_values = [["ARG", "int", "ident", None],["ARG", "string", "tag", None],["ARG", "bool", "available", None],[None, None, "next", "NODEPOINTER"]]
		
		self.engine_version = "1.1.2e"
		
		
#-----------------------------------------------------------------------

	#This functions uses the generate functions to compose the final code
	def generateCode(self, cld_path, clc_input, values):
		
		clc_path = (cld_path + clc_input[0] + clc_input[1] + ".clc").replace(".cld", "")
		code_path = clc_path[:-4]
		print code_path
		
		code = self.loadFile(clc_path)
		tokens = self.tokenizeArgs(code)
		code = self.processArgsCommands(code, tokens)
		tokens = self.tokenizeBase(code)
		code = self.processBaseCommands(code, tokens)
		self.saveFile(code_path, code)
				
		
#-----------------------------------------------------------------------

	#This is the main function for the CLD files.
	def processCLD(self, file_path, values):
		
		print file_path
		
		self.cld_base_name = os.path.basename(file_path)[:os.path.basename(file_path).find(".")]
		self.cld_values = self.findData(file_path, 1)
		self.createLostCLCs(file_path, values)
		
		for clc_input in self.checks:	
			self.generateCode(file_path, clc_input, values)


#-----------------------------------------------------------------------

	#This is the main function for the generator. Starts the generation.
	def process(self, source):
		
		#Loads the options for the solution and the single code files.
		self.cls_values = self.findData(source)
		self.searchFiles(self.cls_values["SOURCE"])
		
		#The generator processes every CLC file one by one.
		clear()
		for file_name in self.file_list:
			self.processCLD(file_name, self.cls_values)	
	
	
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
				result_list.append([search1.group(1), search1.group(2), search1.group(3), None])

		f.close()
		
		if search_style == 0:
			return result_dic
		
		elif search_style == 1:
			return result_list
			
		
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

	#This functions loads the CLC file in a list
	def loadFile(self, clc_path):
		
		code = []
		
		f = open(clc_path)
		for line in f:
			code.append(line)
		f.close()

		return code
		
		
#-----------------------------------------------------------------------

	#This function looks for the base commands inside the code and creates
	#a list with the information of all the changes that will be applied
	#to the code
	
	def tokenizeBase(self, code):

		tokens = []
		count = -1
		
		for line in code:
			
			count+=1
			
			token_init = 0
			token_end = 0
			
			while token_init > -1:
				
				token_init = line.find("<[", token_end)
				token_end = line.find(">", token_init)
			
				if token_init > -1 and token_init > -1:
					
					comm = line[token_init:token_end+1]
					base = line[line.find("[", token_init)+1:line.find("]", token_init)]
					mod = self.searchMods(line)
					tokens.append([count, comm, base, mod])
					
		return tokens
		
						
#-----------------------------------------------------------------------

	#This functions looks for the different argument loops and gets the
	#propper information from the CLC file.
	 
	def tokenizeArgs(self, code):
		
		tokens = []
		count = 0
		problems = False
		count_problems = 0
		result = []
		level = -1
		
		for line in code:
			
			count+=1
			
			if line.find(self.FORARGSOPEN) > -1:
				level+=1
				mod = self.searchMods(line)
				tokens.append(["forargs_open", count, level, mod])

			elif line.find(self.FORARGSCLOSE) > -1:
				tokens.append(["forargs_close", count, level, []])
				level-=1
			
			elif line.find(self.FORARGSBASEOPEN) > -1:
				level+=1
				mod = self.searchMods(line)
				tokens.append(["forargsbase_open", count, level, mod])

			elif line.find(self.FORARGSBASECLOSE) > -1:
				tokens.append(["forargsbase_close", count, level, []])
				level-=1
			
		for token in tokens:
			
			if token[0] == "forargs_open" or token[0] == "forargsbase_open":
				count_problems += 1
		
			if token[0] == "forargs_close" or token[0] == "forargsbase_close":
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

	#The tokenizeArgs funtion looks for the loops, but cannot understand
	#the hierarchy from  the code. This functions look the loops and set 
	#it up.
	
	def setHierarchy(self, tokens):
		
		hierarchy = []
		level = -1
		ident = -1
		found = False


		for token in tokens:
						
			if token[0] == "forargs_open":
				level+=1
				ident+=1
				hierarchy.append([ident, level, token[1], -1, "forargs", token[3]])
		
			elif token[0] == "forargs_close":
				level-=1

			elif token[0] == "forargsbase_open":
				level+=1
				ident+=1
				hierarchy.append([ident, level, token[1], -1, "forargsbase", token[3]])
		
			elif token[0] == "forargsbase_close":
				level-=1
		
		for count in range(0, len(hierarchy)):
			
			found = False
			
			for search in range(0, len(tokens)):

				if hierarchy[count][2] == tokens[search][1] and tokens[search][0] == "forargs_open":
					found = True
					
				if found == True and tokens[search][0] == "forargs_close" and tokens[search][2] == hierarchy[count][1]:
					found = False
					hierarchy[count][3] = tokens[search][1]

				if hierarchy[count][2] == tokens[search][1] and tokens[search][0] == "forargsbase_open":
					found = True
					
				if found == True and tokens[search][0] == "forargsbase_close" and tokens[search][2] == hierarchy[count][1]:
					found = False
					hierarchy[count][3] = tokens[search][1]
				
			
		return hierarchy


#-----------------------------------------------------------------------

	#Here is where the substitution of the base commands is applied.
	def processBaseCommands(self, code, tokens):
		
		for token in tokens:
			
			if token[2] == "PROJECT":
				value = self.applyMods(self.cls_values["PROJECT"], token[3])

			elif token[2] == "DEVLINE":
				value = self.applyMods(self.cls_values["DEVLINE"], token[3])
			
			elif token[2] == "CREATIONDATE":
				value = self.applyMods(self.cls_values["CREATIONDATE"], token[3])
			
			elif token[2] == "TODAY":
				value = self.applyMods(date.today().strftime("%d/%m/%y"), token[3])
			
			elif token[2] == "VERSION":
				value = self.applyMods(self.engine_version, token[3])

			elif token[2] == "BASENAME":
				value = self.applyMods(self.cld_base_name, token[3])

			elif token[2] == "FULLLIST_ARGS":
				exceptions = self.processExceptions(token[3])
				value = ""
				
				for arg in self.cld_values:
					if exceptions[0].count(arg[2]) == 0:
						value += arg[1] + " " + self.applyMods(arg[2], exceptions[1])+ ", "
						
				value = value[:-2]

			code[token[0]] = code[token[0]].replace(token[1], value)
			
		return code
		
		
#-----------------------------------------------------------------------

	#This functions generates the code for the loops realted to the
	#args commands.
	
	def processArgsCommands(self, code, tokens):
		
		
		new_code = []
		
		for token in tokens:
			
			ignores = self.searchIgnores(token[5])
			
			comm_values = self.cld_values
			if token[4] == "forargsbase":
				comm_values = self.base_values + self.cld_values

			for arg in comm_values:
				
				if arg[3] == "NODEPOINTER":
											
					arg[0] = "ARG"
					arg[1] = self.cld_base_name + "*"						
		
			lines = code[token[2]:token[3]-1]
			new_lines = []
			
			for arg in comm_values:
				
				if ignores.count(arg[2]) == 0:
	
					for line in lines:
						
						if arg[0] == "ARG":
							
							new_line = line
							modified = True
							
							while modified:
								result = self.applyCommand(new_line, arg)
								modified = result[0]
								new_line = result[1]

							new_lines.append(new_line)				
					
			new_code.append(new_lines)
			
		count = 0
		diff = 0
		init_len = len(code)
		for token in tokens:
			
			code[token[2]-1+diff:token[3]+diff] = new_code[count]
			diff = len(code) - init_len
			count+=1
		
		return code

		
#-----------------------------------------------------------------------

	#This function looks for the different generator's commands and applies
	#the changes

	def applyCommand(self, line, arg):

		changed = False
		comm = None
		comm_start = -1
		comm_end = -1
		
		comm_start = line.find("<[ARG_NAME]")
		if comm_start > -1 and changed == False:
			comm_end = line.find(">", comm_start)
			comm = line[comm_start:comm_end+1]
			mod = self.searchMods(comm)
			com_res = self.applyMods(arg[2], mod)
			changed = True

		if comm_start == -1:
			comm_start = line.find("<[ARG_TYPE]")
		if comm_start > -1 and changed == False:
			comm_end = line.find(">", comm_start)
			comm = line[comm_start:comm_end+1]
			mod = self.searchMods(comm)
			com_res = arg[1]
			changed = True

		if comm_start == -1:
			comm_start = line.find("<[ARG_DEF]")
		if comm_start > -1 and changed == False:
			comm_end = line.find(">", comm_start)
			comm = line[comm_start:comm_end+1]
			mod = self.searchMods(comm)
			com_res = arg[1] + " " + self.applyMods(arg[2], mod)
			changed = True

		if comm_start == -1:
			comm_start = line.find("<[ARG_INIT]")
		if comm_start > -1 and changed == False:
			comm_end = line.find(">", comm_start)
			comm = line[comm_start:comm_end+1]
			mod = self.searchMods(comm)
			if arg[1] == "bool":
				com_res = "false"
			elif arg[1] == "int":
				com_res = "-1"
			elif arg[1] == "double":
				com_res = "-1.0"
			elif arg[1] == "string":
				com_res = "\"\""
			elif arg[1] == "Uint8":
				com_res = "0"
			elif arg[1] == "Uint16":
				com_res = "0"
			elif arg[1] == "Uint32":
				com_res = "0"
			else:
				com_res = "nullptr"
			changed = True

		if not comm == None:
			line = line.replace(comm, com_res)

		return [changed, line]


#-----------------------------------------------------------------------

	#This function looks for modifiers inside of the code commands.
	def searchMods(self, comm):
		
		mods = []
		mod_init = 0
		mod_end = 0
		
		while mod_init > -1:
			
			mod_init = comm.find("{", mod_end)
			mod_end = comm.find("}", mod_init)
			
			if mod_init > -1 and mod_end > -1:
				mods.append(comm[mod_init+1:mod_end])
		
		
		return mods
		

#-----------------------------------------------------------------------

	#This function looks for ingnore modifiers inside a loop.
	def searchIgnores(self, comm):

		ignores = []
		ign_init = 0
		ing_end = 0
		
		for mod in comm:

			ign_init = mod.find("ignore:")

			if ign_init > -1:
				ignores.append(mod[ign_init+len("ignore:"):])
		
		return ignores
		

#-----------------------------------------------------------------------

	#This functions applies the modifications
	def applyMods(self, value, mods):
		
		for mod in mods:
			
			if mod == "capital":
				value = value.upper()

			elif mod == "first":
				value = value.capitalize()
				
			elif mod == "low":
				value = value.lower()
				
		return value


#-----------------------------------------------------------------------

	#This function is used to save all the generated code
	def saveFile(self, path, code):
		
		f = open(path, "w")
		
		if not code == None:
			for line in code:
				f.write(line)
		
		f.close()


#-----------------------------------------------------------------------

	#This function is used to create a table with the exceptions for the
	#FULLLIST_ARGS base command.
	def processExceptions(self, tokens):

		exceptions = [[], []]
		
		for token in tokens:

			if token.find("except:") > -1:
				exceptions[0].append(token[token.find(":")+1:])

			else:
				exceptions[1].append(token)

		return exceptions


#-----------------------------------------------------------------------


