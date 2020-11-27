#include <iostream>
#include <string>
using namespace std;

#ifndef ASSIGN_INPUT_TO_OUTPUT_H_
#define ASSIGN_INPUT_TO_OUTPUT_H_

//will have 7 arrays of size 12 
class Day_of_week
{
private:
	string name, info;
public:
	//constructo
	Day_of_week(){}
	//setters
	void set_activity_name(string);
	void set_activity_info(string);
	//getters
	string get_activity_name();
	string get_activity_info();



	virtual ~Day_of_week(){}

};

#endif /*ASSIGN_INPUT_TO_OUTPUT*/
