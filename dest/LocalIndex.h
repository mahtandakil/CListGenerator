/****************************************************************************
* Created for: DevSecPac
* Dev line: V2 LINE
* Creation date: 11/01/2016
* Last change: 02/02/16
* Autogen: 1.1.0
****************************************************************************/


#include "LOCAL.h"


#include <iostream>


using namespace std;


#ifndef LOCALINDEX_H
#define LOCALINDEX_H


class LocalIndex
{
	public:
		LocalIndex();
		virtual ~LocalIndex();

		int createRegister(string tag="");
		int searchAvailable();
		int freeNode(int id);
		int freeList();
		int deleteNode(int id);
		int deleteList();
		int purge();
		int getId(int id);
		string getTag(int id);
		bool getAvailable(int id);
		Local* getNext(int id);
		string getName(int id);
		string getType(int id);
		string getS_value(int id);
		int getI_value(int id);
		double getD_value(int id);
		int setTag(int id, string tag)
		int setAvailable(int id, bool available)
		int setNext(int id, Local* next)
		int setName(int id, string name)
		int setType(int id, string type)
		int setS_value(int id, string s_value)
		int setI_value(int id, int i_value)
		int setD_value(int id, double d_value)
		int searchById(int id);
		int searchByTag(string tag);
		int searchByAvailable(bool available);
		int searchByNext(Local* next);
		int searchByName(string name);
		int searchByType(string type);
		int searchByS_value(string s_value);
		int searchByI_value(int i_value);
		int searchByD_value(double d_value);


	protected:



	private:
		int counter;
		int id_base;
		Local* first;
		Local* last;


};


#endif // LOCALINDEX_H

