#****************************************************************************
# Created for: SDLApi v1
# Dev line: SDLApi v1
# Creation day: 05/08/2015
# Last change: 27/08/2015
#
# Reserved words: id, tag, pointer, available, element, index, data
#***************************************************************************/


import time


#############################################################################


class generator:
	
	def __init__(self):
		self.version = "1.0.8"
		self.datos = []
		self.variables = []

	def __del__(self):
		q=0


#----------------------------------------------------------------------------

	def load(self):
		
		f = open("clistgenerator.vim")

		for x in f:
			self.datos.append(x[:-1])

		f.close()
		
		temp = ["int id"] + ["string tag"] + ["bool available"] + [self.datos[2] + "Element* next"] + self.datos[3:]
		
		for x in temp:
			self.variables.append([x[:x.find(" ")], x[x.find(" ")+1:], x])
				
		for x in self.variables:
			print x

		

#----------------------------------------------------------------------------

	def createIndexH(self):
		
		src = self.datos[2] + "Index.h"		
		f = open(src, "w")
		
		f.write("/****************************************************************************\n")
		f.write("* Created for: " + self.datos[0] + "\n")
		f.write("* Dev line: " + self.datos[1] + "\n")
		f.write("* Creation day: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Last change: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Autogen: CListGen " + self.version + "\n")
		f.write("****************************************************************************/\n")
		f.write("\n\n")

		f.write("#include \"" + self.datos[2] + "Element.h\"")
		f.write("\n\n\n")		
		f.write("#include <iostream>")
		f.write("\n\n\n")		
		f.write("using namespace std;\n")
		f.write("\n\n")	
		
		f.write("#ifndef " + self.datos[2].upper() + "INDEX_H\n")
		f.write("#define " + self.datos[2].upper() + "INDEX_H\n")
		f.write("\n\n")
		
		f.write("class " + self.datos[2] + "Index\n");
		f.write("{\n");
		f.write("	public:\n");
		f.write("		" + self.datos[2] + "Index();\n");
		f.write("		virtual ~" + self.datos[2] + "Index();\n");
		f.write("\n");
		f.write("		int createRegister(string tag);\n");
		f.write("		int freeList();\n");
		
		for x in self.variables:
			f.write("		" + x[0] + " get" + x[1].capitalize() + "(int id);\n");
		
		for x in self.variables:
			f.write("		int searchBy" + x[1].capitalize() + "(" + x[2] + ");\n");
		
		text = ""
		for x in self.variables:
			if not (x[1] == "id" or x[1] == "available" or x[1] == "next"):
				text += x[2] + ", "
		f.write("		int setElementData(int id, " + text[:-2] + ");\n")

		text = ""
		for x in self.variables:
			if not (x[1] == "id" or x[1] == "available" or x[1] == "next" or x[1] == "tag"):
				text += x[2] + ", "
		f.write("		int setElementData(int id, " + text[:-2] + ");\n")
		
		for x in self.variables:
			if not x[1] == "id":
				f.write("		int set" + x[1].capitalize() + "(int id, " + x[2] + ");\n");
		
		f.write("\n");
		f.write("\n");
		f.write("	protected:\n");
		f.write("\n");
		f.write("\n");
		f.write("\n");
		
		f.write("	private:\n");
		f.write("		int counter;\n");
		f.write("		" + self.datos[2] + "Element* first;\n");
		f.write("		" + self.datos[2] + "Element* last;\n");
		f.write("\n");
		f.write("		" + self.datos[2] + "Element* getElementById(int id);\n");
		f.write("		int searchAvailable();\n");
		f.write("\n");
		f.write("};\n");
		f.write("\n");
		f.write("\n");
		f.write("#endif // " + self.datos[2].upper() + "INDEX_H\n");
		f.write("\n");
		f.write("\n");



		f.close()

#----------------------------------------------------------------------------

	def createIndexCpp(self):
		
		src = self.datos[2] + "Index.cpp"		
		f = open(src, "w")
		
		f.write("/****************************************************************************\n")
		f.write("* Created for: " + self.datos[0] + "\n")
		f.write("* Dev line: " + self.datos[1] + "\n")
		f.write("* Creation day: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Last change: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Autogen: CListGen " + self.version + "\n")
		f.write("****************************************************************************/\n")
		f.write("\n\n")

		f.write("#include \"" + self.datos[2] + "Index.h\"")
		f.write("\n\n\n")	
		
		f.write("//---------------------------------------------------------------------------\n\n")	
		f.write(self.datos[2] + "Index::" + self.datos[2] + "Index()\n")
		f.write("{\n")
		f.write("\n")
		f.write("	this->counter = 0;\n")
		f.write("	this->first = nullptr;\n")
		f.write("	this->last = nullptr;\n")		
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write(self.datos[2] + "Index::~" + self.datos[2] + "Index()\n")
		f.write("{\n\n")
		f.write("	this->freeList();\n")
		f.write("\n}\n")
		f.write("\n")
		f.write("\n")
		
		
		f.write("//---------------------------------------------------------------------------\n\n")	
		f.write("int " + self.datos[2] + "Index::createRegister(string tag){\n\n")		
		f.write("	" + self.datos[2] + "Element* pointer = new " + self.datos[2] + "Element();\n")
		f.write("	pointer->setTag(tag);\n")
		f.write("\n")
		f.write("	if (this->counter == 0){\n")
		f.write("\n")
		f.write("		this->counter = 1;\n")
		f.write("		pointer->setId(0);\n")
		f.write("		this->first = pointer;\n")
		f.write("		this->last = pointer;\n")
		f.write("\n")
		f.write("	}else{\n")
		f.write("\n")
		f.write("		this->counter++;\n")
		f.write("		pointer->setId(this->counter-1);\n")
		f.write("		this->last->setNext(pointer);\n")
		f.write("		this->last = pointer;\n")
		f.write("\n")
		f.write("	}\n")
		f.write("\n")
		f.write("	return pointer->getId();\n")
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write("\n")


		f.write("//---------------------------------------------------------------------------\n\n")	
		f.write("int " + self.datos[2] + "Index::freeList(){\n\n")		
		f.write("	" + self.datos[2] + "Element* pointer;\n")
		f.write("	" + self.datos[2] + "Element* next;\n")
		f.write("	int result= 0;\n")
		f.write("\n")
		f.write("    if(this->first != nullptr){\n")
		f.write("\n")
		f.write("        pointer = this->first;\n")
		f.write("\n")
		f.write("        while(pointer != nullptr){\n")
		f.write("\n")
		f.write("            next = pointer->getNext();\n")
		f.write("            counter++;\n")
		f.write("            delete pointer;\n")
		f.write("            pointer = next;\n")
		f.write("\n")
		f.write("        }\n")
		f.write("\n")
		f.write("    }\n")
		f.write("\n")
		f.write("    return result;\n")
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write("\n")
		

		for x in self.variables:
			f.write("//---------------------------------------------------------------------------\n")	
			f.write("\n")
			f.write(x[0] + " " + self.datos[2] + "Index::get" + x[1].capitalize() + "(int id){\n")
			f.write("\n")
			f.write("	" + x[0] + " result = ")
			f.write(self.varInitializer(x[0]))
			f.write("	" + self.datos[2] + "Element* pointer;\n")
			f.write("\n")
			f.write("	pointer = this->getElementById(id);\n")
			f.write("\n")
			f.write("	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){\n")
			f.write("		result = ")
			f.write(self.varInitializer(x[0]))
			f.write(";\n")
			f.write("\n")
			f.write("	}else{\n")
			f.write("		result = pointer->get" + x[1].capitalize() + "();\n")
			f.write("\n")
			f.write("	}\n")
			f.write("\n")
			f.write("	return result;\n")
			f.write("\n")
			f.write("}\n")
			f.write("\n")
			f.write("\n")

		for x in self.variables:
			f.write("//---------------------------------------------------------------------------\n")	
			f.write("\n")
			f.write("int " + self.datos[2] + "Index::searchBy" + x[1].capitalize() + "(" + x[2] + "){\n")
			f.write("\n")
			f.write("	int result = -1;\n")
			f.write("	bool found = false;\n")
			f.write("	" + self.datos[2] + "Element* pointer;\n")
			f.write("\n")
			f.write("	if (this->counter == 0){\n")
			f.write("		result = -1;\n")
			f.write("\n")
			f.write("	}else{\n")
			f.write("\n")
			f.write("		pointer = this->first;\n")
			f.write("\n")
			f.write("		while (not ((pointer == nullptr) or (found))){\n")
			f.write("\n")
			f.write("			if (" + x[1] + " == pointer->get" + x[1].capitalize() + "()){\n")
			f.write("\n")
			f.write("				result = pointer->getId();\n")
			f.write("				found = true;\n")
			f.write("\n")
			f.write("			}\n")
			f.write("\n")
			f.write("			pointer = pointer->getNext();\n")
			f.write("\n")
			f.write("		}\n")
			f.write("\n")
			f.write("	}\n")
			f.write("\n")
			f.write("	return result;\n")
			f.write("\n")
			f.write("}\n")
			f.write("\n")
			f.write("\n")
			f.write("\n")

		text = ""
		text2 = ""
		for x in self.variables:
			if not (x[1] == "id" or x[1] == "available" or x[1] == "next"):
				text += x[2] + ", "
				text2 += "		pointer->set" + x[1].capitalize() + "(" + x[1] + ");\n"
		f.write("//---------------------------------------------------------------------------\n")	
		f.write("\n")
		f.write("int " + self.datos[2] + "Index::setElementData(int id, " + text[:-2] + "){\n")
		f.write("\n")
		f.write("	" + self.datos[2] + "Element* pointer;\n")
		f.write("	int result = -1;\n")
		f.write("\n")
		f.write("	pointer = this->getElementById(id);\n")
		f.write("\n")
		f.write("	if (pointer != nullptr){\n")
		f.write("\n")
		f.write(text2)
		f.write("		result = pointer->getId();\n")
		f.write("\n")
		f.write("	}\n")
		f.write("\n")
		f.write("	return result;\n")
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write("\n")

		text = ""
		text2 = ""
		for x in self.variables:
			if not (x[1] == "id" or x[1] == "available" or x[1] == "next" or x[1] == "tag"):
				text += x[2] + ", "
				text2 += "		pointer->set" + x[1].capitalize() + "(" + x[1] + ");\n"
		f.write("//---------------------------------------------------------------------------\n")	
		f.write("\n")
		f.write("int " + self.datos[2] + "Index::setElementData(int id, " + text[:-2] + "){\n")
		f.write("\n")
		f.write("	" + self.datos[2] + "Element* pointer;\n")
		f.write("	int result = -1;\n")
		f.write("\n")
		f.write("	pointer = this->getElementById(id);\n")
		f.write("\n")
		f.write("	if (pointer != nullptr){\n")
		f.write("\n")
		f.write(text2)
		f.write("		result = pointer->getId();\n")
		f.write("\n")
		f.write("	}\n")
		f.write("\n")
		f.write("	return result;\n")
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write("\n")


		for x in self.variables:
			if not x[1] == "id":	
				f.write("//---------------------------------------------------------------------------\n")	
				f.write("\n")
				f.write("int " + self.datos[2] + "Index::set" + x[1].capitalize() + "(int id, " + x[2] + "){\n")
				f.write("\n")
				f.write("	" + self.datos[2] + "Element* pointer;\n")
				f.write("	int result = -1;\n")
				f.write("\n")
				f.write("	pointer = this->getElementById(id);\n")
				f.write("\n")
				f.write("	if (pointer != nullptr){\n")
				f.write("\n")
				f.write("		pointer->set" + x[1].capitalize() + "(" + x[1] + ");\n")
				f.write("		result = pointer->getId();\n")
				f.write("\n")
				f.write("	}\n")
				f.write("\n")
				f.write("	return result;\n")
				f.write("\n")
				f.write("}\n")
				f.write("\n")
				f.write("\n")

		f.write("//---------------------------------------------------------------------------\n")	
		f.write("\n")
		f.write(self.datos[2] + "Element* " + self.datos[2] + "Index::getElementById(int id){\n")
		f.write("	" + self.datos[2] + "Element* result;\n")
		f.write("	" + self.datos[2] + "Element* pointer;\n")
		f.write("	" + "\n")
		f.write("	" + "if (this->counter == 0){\n")
		f.write("	" + "	result = nullptr;\n")
		f.write("	" + "\n")
		f.write("	" + "}else{\n")
		f.write("	" + "\n")
		f.write("	" + "	pointer = this->first;\n")
		f.write("	" + "	\n")
		f.write("	" + "	while (pointer != nullptr){\n")
		f.write("	" + "		if (id == pointer->getId()){\n")
		f.write("	" + "			result = pointer;\n")
		f.write("	" + "	\n")
		f.write("	" + "		}\n")
		f.write("	" + "	\n")
		f.write("	" + "	pointer = pointer->getNext();\n")
		f.write("	" + "	}\n")
		f.write("	}" + "\n")
		f.write("	" + "\n")
		f.write("	return result;" + "\n")
		f.write("	" + "\n")
		f.write("}\n\n\n")

		f.write("//---------------------------------------------------------------------------\n")	
		f.write("\n")
		f.write("int " + self.datos[2] + "Index::searchAvailable(){\n")
		f.write("\n")
		f.write("	int result = -1;\n")
		f.write("	int counter = 0;\n")
		f.write("	bool found = false;\n")
		f.write("	" + self.datos[2] + "Element* pointer;\n")
		f.write("	\n")
		f.write("	while((counter < this->counter) && (found == false)){\n")
		f.write("	\n")
		f.write("		pointer = this->getElementById(counter);\n")
		f.write("		if (pointer->getAvailable() == true){\n")
		f.write("	\n")
		f.write("			result = pointer->getId();\n")
		f.write("			found = true;\n")
		f.write("	\n")
		f.write("		}\n")
		f.write("	\n")
		f.write("		counter++;\n")
		f.write("	\n")
		f.write("	}\n")
		f.write("	\n")
		f.write("	return result;\n")
		f.write("	\n")
		f.write("}\n\n\n")

	
		f.write("//---------------------------------------------------------------------------\n")	
		f.write("//---------------------------------------------------------------------------\n")	
		f.write("//---------------------------------------------------------------------------\n\n\n")	
		
		
		f.close()
		
		
		
#----------------------------------------------------------------------------

	def createElementH(self):
		src = self.datos[2] + "Element.h"		
		f = open(src, "w")
		
		f.write("/****************************************************************************\n")
		f.write("* Created for: " + self.datos[0] + "\n")
		f.write("* Dev line: " + self.datos[1] + "\n")
		f.write("* Creation day: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Last change: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Autogen: CListGen " + self.version + "\n")
		f.write("****************************************************************************/\n")
		f.write("\n\n")

		f.write("#include <iostream>")
		f.write("\n\n\n")		
		f.write("using namespace std;\n")
		f.write("\n\n")	
		
		f.write("#ifndef " + self.datos[2].upper() + "ELEMENT_H\n")
		f.write("#define " + self.datos[2].upper() + "ELEMENT_H\n")
		f.write("\n\n")
		
		f.write("class " + self.datos[2] + "Element\n");
		f.write("{\n");
		f.write("	public:\n");
		f.write("		" + self.datos[2] + "Element();\n");
		f.write("		virtual ~" + self.datos[2] + "Element();\n");
		f.write("\n");

		for x in self.variables:
			f.write("		" + x[0] + " get" + x[1].capitalize() + "();\n");
		
		for x in self.variables:
			f.write("		void set" + x[1].capitalize() + "(" + x[2] + ");\n");
		
		f.write("\n");
		f.write("\n");
		f.write("	protected:\n");

		f.write("\n");
		f.write("\n");
		f.write("	private:\n");

		for x in self.variables:
			f.write("		" + x[2] + ";\n");

		f.write("\n");
		f.write("};\n");
		f.write("\n");
		f.write("\n");
		f.write("#endif // " + self.datos[2].upper() + "ELEMENT_H\n");
		f.write("\n");
		f.write("\n");


#----------------------------------------------------------------------------

	def createElementCpp(self):

		src = self.datos[2] + "Element.cpp"		
		f = open(src, "w")

		f.write("/****************************************************************************\n")
		f.write("* Created for: " + self.datos[0] + "\n")
		f.write("* Dev line: " + self.datos[1] + "\n")
		f.write("* Creation day: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Last change: " + time.strftime("%d/%m/%Y") + "\n")
		f.write("* Autogen: CListGen " + self.version + "\n")
		f.write("****************************************************************************/\n")
		f.write("\n\n")

		f.write("#include \"" + self.datos[2] + "Element.h\"")
		f.write("\n\n\n")	

		f.write("//---------------------------------------------------------------------------\n\n")	
		f.write(self.datos[2] + "Element::" + self.datos[2] + "Element()\n")
		f.write("{\n")
		f.write("\n")
		for x in self.variables:
			f.write("	this->" + x[1] + " = ")
			f.write(self.varInitializer(x[0]))
		f.write("\n")
		f.write("}\n")
		f.write("\n")
		f.write(self.datos[2] + "Element::~" + self.datos[2] + "Element()\n")
		f.write("{\n")
		f.write("	//dtor\n")
		f.write("}\n")
		f.write("\n")
		f.write("\n")


		for x in self.variables:

			f.write("//---------------------------------------------------------------------------\n")	
			f.write("\n")
			f.write(x[0] + " " + self.datos[2] + "Element::get" + x[1].capitalize() + "(){\n")
			f.write("\n")
			f.write("	return this->" + x[1] + ";\n")
			f.write("\n")
			f.write("}\n\n\n")

			f.write("//---------------------------------------------------------------------------\n")	
			f.write("\n")
			f.write("void " + self.datos[2] + "Element::set" + x[1].capitalize() + "(" + x[2] + "){\n")
			f.write("\n")
			f.write("	this->" + x[1] + " = " + x[1] + ";\n")
			f.write("\n")
			f.write("}\n\n\n")		

		f.write("//---------------------------------------------------------------------------\n")	
		f.write("//---------------------------------------------------------------------------\n")	
		f.write("//---------------------------------------------------------------------------\n")	

		f.close()

#----------------------------------------------------------------------------

	def varInitializer(self, var):

		result = "";

		if var == "int":
			result = "0;\n"
		
		elif var == "string":
			result = "\"\";\n"
				
		elif var == "bool":
			result = "false;\n"
		
		elif var == "Uint8":
			result = "0;\n"
		
		elif var == "Uint16":
			result = "0;\n"
		
		elif var == "Uint32":
			result = "0;\n"
		
		elif var == "Uint64":
			result = "0;\n"
		
		else:
			result = "nullptr;\n"
			
		return result
		

#############################################################################

if __name__ == "__main__":
	
	app = generator()
	app.load()
	app.createIndexH()
	app.createIndexCpp()
	app.createElementH()
	app.createElementCpp()
	raw_input(">")


#############################################################################



