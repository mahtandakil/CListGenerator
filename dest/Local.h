/****************************************************************************
* Created for: DevSecPac
* Dev line: V2 LINE
* Creation date: 11/01/2016
* Last change: 14/02/16
* Autogen: 1.1.3
****************************************************************************/


#include <iostream>


using namespace std;


#ifndef LOCAL_H
#define LOCAL_H


class Local
{
	public:
		Local();
		virtual ~Local();

		string getName();
		string getType();
		string getS_value();
		int getI_value();
		double getD_value();
		int getIdent();
		string getTag();
		bool getAvailable();
		Local* getNext();
		int setName(string name);
		int setType(string type);
		int setS_value(string s_value);
		int setI_value(int i_value);
		int setD_value(double d_value);
		int setIdent(int ident);
		int setTag(string tag);
		int setAvailable(bool available);
		int setNext(Local* next);
		int setIdent(int ident);
		int setTag(string tag);
		int setAvailable(bool available);
		int setNext(Local* next);
		


	protected:


	private:
		string name;
		string type;
		string s_value;
		int i_value;
		double d_value;
		int ident;
		string tag;
		bool available;
		Local* next;
		int ident;
		string tag;
		bool available;
		Local* next;
		int ident;
		string tag;
		bool available;
		Local* next;

};


#endif // LOCAL_H



