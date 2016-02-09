/****************************************************************************
* Created for: DevSecPac
* Dev line: V2 LINE
* Creation date: 11/01/2016
* Last change: 02/02/16
* Autogen: 1.1.0
****************************************************************************/


#include "LocalIndex.h"


//---------------------------------------------------------------------------

LocalIndex::LocalIndex()
{

	this->counter = 0;
	this->id_base = 0;
	this->first = nullptr;
	this->last = nullptr;

}

LocalIndex::~LocalIndex()
{

	this->purge();

}


//---------------------------------------------------------------------------

int LocalIndex::createRegister(string tag=""){

	Local* pointer = new Local();
	pointer->setTag(tag);

	if (this->counter == 0){

		this->counter = 1;
		this->first = pointer;
		this->last = pointer;

	}else{

		this->counter++;
		pointer->setId(this->counter-1);
		this->last->setNext(pointer);

	}
	
	pointer->setId(this->id_base);
	this->id_base++;
	this->last = pointer;

	return pointer->getId();

}


//---------------------------------------------------------------------------

int LocalIndex::searchAvailable(){

	int result = -1;
	int counter = 0;
	bool found = false;
	Local* pointer;
	
	while((counter < this->counter) && (found == false)){
	
		pointer = this->getNode(counter);
		if (pointer->getAvailable() == true){
	
			result = pointer->getId();
			found = true;
	
		}
	
		counter++;
	
	}
	
	return result;
	
}


//---------------------------------------------------------------------------

int LocalIndex::freeNode(int id){

	int result= 0;

	result = this->setAvailable(id, true);

    return result;

}


//---------------------------------------------------------------------------

int LocalIndex::freeList(){

	Local* pointer;
	int result = 0;
	
	pointer = this->getNode(0);
	
	while(pointer != nullptr){
	
		if(pointer->getAvailable() == false){
		
			pointer->setAvailable(true);
			pointer = pointer->next;
			result++:
		
		}
	
	}
	
	return result;
	

}


//---------------------------------------------------------------------------

int LocalIndex::deleteNode(int id){

	Local* pointer;
	Local* previous;
	int result = -1;
	
	pointer = this->getNode(id);
	
	if(pointer != nullptr){
	
		if(id == 0){
		
			this->first = pointer->next;
		
		}else{
			
			previous = this->getNode(id-1);
			previous->next = pointer->next;
		
		}
		
		result = pointer->id;
		delete(pointer);
		this->counter--;
	
	}
	
	return result;
	
}


//---------------------------------------------------------------------------

int LocalIndex::deleteList(int id){

	int result = -1;

	this->freeList();
	result = this->purge();

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::purgue(int id){

	Local* pointer;
	Local* next;
	int result = 0;
	
	pointer = this->first;
	
	while(pointer != nullptr){

		next = pointer->next;
	
		if(pointer->getAvailable()){
		
			this->deleteNode(pointer);
			counter++;
		
		}
		
		pointer = next;
	
	}
	
	return counter;
	

}


//---------------------------------------------------------------------------

Local* LocalIndex::getNode(int id){

	Local* pointer;

	pointer = this->getElementById(id);

	return pointer;

}



string LocalIndex::getName(int id){

	string result = "";
	Local* pointer;

	pointer = this->getNode(id);

	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){
		result = "";

	}else{
		result = pointer->getName();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::setName(int id, string name){

	 Local* pointer;
	int result = -1;

	pointer = this->getNode(id);

	if (pointer != nullptr){

		pointer->setName(name);
		result = pointer->getId();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::searchByName(string name){

	int result = -1;
	bool found = false;
	Local* pointer;

	if (this->counter == 0){
		result = -1;

	}else{

		pointer = this->first;

		while (not ((pointer == nullptr) or (found))){

			if (name == pointer->getS_value()){

				result = pointer->getId();
				found = true;

			}

			pointer = pointer->getNext();

		}

	}

	return result;

}


//---------------------------------------------------------------------------

string LocalIndex::getType(int id){

	string result = "";
	Local* pointer;

	pointer = this->getNode(id);

	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){
		result = "";

	}else{
		result = pointer->getType();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::setType(int id, string type){

	 Local* pointer;
	int result = -1;

	pointer = this->getNode(id);

	if (pointer != nullptr){

		pointer->setType(type);
		result = pointer->getId();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::searchByType(string type){

	int result = -1;
	bool found = false;
	Local* pointer;

	if (this->counter == 0){
		result = -1;

	}else{

		pointer = this->first;

		while (not ((pointer == nullptr) or (found))){

			if (type == pointer->getS_value()){

				result = pointer->getId();
				found = true;

			}

			pointer = pointer->getNext();

		}

	}

	return result;

}


//---------------------------------------------------------------------------

string LocalIndex::getS_value(int id){

	string result = "";
	Local* pointer;

	pointer = this->getNode(id);

	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){
		result = "";

	}else{
		result = pointer->getS_value();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::setS_value(int id, string s_value){

	 Local* pointer;
	int result = -1;

	pointer = this->getNode(id);

	if (pointer != nullptr){

		pointer->setS_value(s_value);
		result = pointer->getId();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::searchByS_value(string s_value){

	int result = -1;
	bool found = false;
	Local* pointer;

	if (this->counter == 0){
		result = -1;

	}else{

		pointer = this->first;

		while (not ((pointer == nullptr) or (found))){

			if (s_value == pointer->getS_value()){

				result = pointer->getId();
				found = true;

			}

			pointer = pointer->getNext();

		}

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::getI_value(int id){

	int result = -1;
	Local* pointer;

	pointer = this->getNode(id);

	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){
		result = "";

	}else{
		result = pointer->getI_value();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::setI_value(int id, int i_value){

	 Local* pointer;
	int result = -1;

	pointer = this->getNode(id);

	if (pointer != nullptr){

		pointer->setI_value(i_value);
		result = pointer->getId();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::searchByI_value(int i_value){

	int result = -1;
	bool found = false;
	Local* pointer;

	if (this->counter == 0){
		result = -1;

	}else{

		pointer = this->first;

		while (not ((pointer == nullptr) or (found))){

			if (i_value == pointer->getS_value()){

				result = pointer->getId();
				found = true;

			}

			pointer = pointer->getNext();

		}

	}

	return result;

}


//---------------------------------------------------------------------------

double LocalIndex::getD_value(int id){

	double result = -1.0;
	Local* pointer;

	pointer = this->getNode(id);

	if ((pointer == nullptr) or (id < 0) or (id >= this->counter)){
		result = "";

	}else{
		result = pointer->getD_value();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::setD_value(int id, double d_value){

	 Local* pointer;
	int result = -1;

	pointer = this->getNode(id);

	if (pointer != nullptr){

		pointer->setD_value(d_value);
		result = pointer->getId();

	}

	return result;

}


//---------------------------------------------------------------------------

int LocalIndex::searchByD_value(double d_value){

	int result = -1;
	bool found = false;
	Local* pointer;

	if (this->counter == 0){
		result = -1;

	}else{

		pointer = this->first;

		while (not ((pointer == nullptr) or (found))){

			if (d_value == pointer->getS_value()){

				result = pointer->getId();
				found = true;

			}

			pointer = pointer->getNext();

		}

	}

	return result;

}


//---------------------------------------------------------------------------

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

