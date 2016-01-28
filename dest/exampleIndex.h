/****************************************************************************
* Created for: EXAMPLE PROJECT
* Dev line: V2 LINE
* Creation day: 11/01/2016
* Last change: 28/01/16
* Autogen: 1.1.0
****************************************************************************/


#include "example.h"


#include <iostream>


using namespace std;


#ifndef EXAMPLEINDEX_H
#define EXAMPLEINDEX_H


class ExampleIndex
{
	public:
		ExampleIndex();
		virtual ~ExampleIndex();

		int createRegister();
		int createRegister(string tag);
		int freeList();
		int getId(int id);
		string getTag(int id);
		bool getAvailable(int id);
		Example* getExampleById(int id);
		Example* getNext(int id);
		string getstring_var(int id);
		int getint_var(int id);
		dobule getdouble_var(int id);
		int getlow_chars(int id);
		int getCAP_CHARS(int id);
		int searchBystring_var(string string_var);
		int searchByint_var(int int_var);
		int searchBydouble_var(dobule double_var);
		int searchBylow_chars(int low_chars);
		int searchByCAP_CHARS(int CAP_CHARS);
		int setData(int id, string string_var, int int_var, dobule double_var, int low_chars, int CAP_CHARS);
		int setString_var(int id, string_var);
		int setInt_var(int id, int_var);
		int setDouble_var(int id, double_var);
		int setLow_chars(int id, low_chars);
		int setCap_chars(int id, CAP_CHARS);


	protected:


	private:
		int count;
		Example* first;
		Example* last;

		int searchAvailable();

};


#endif // MODELOINDEX_H


