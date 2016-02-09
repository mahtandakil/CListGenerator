/****************************************************************************
* Created for: DevSecPac
* Dev line: V2 LINE
* Creation date: 11/01/2016
* Last change: 02/02/16
* Autogen: 1.1.0
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

		int getId();
		string getTag();
		bool getAvailable();
		Local* getNext();
		string getName();
		string getType();
		string getS_value();
		int getI_value();
		double getD_value();
		int setId(int id);
		int setTag(string tag);
		int setAvailable(bool available);
		int setNext(Local* next);
		int setName(string name);
		int setType(string type);
		int setS_value(string s_value);
		int setI_value(int i_value);
		int setD_value(double d_value);
		


	protected:


	private:
		int id;
		string tag;
		bool available;
		Local* next;
		string name;
		string type;
		string s_value;
		int i_value;
		double d_value;

};


#endif // LOCAL_H



