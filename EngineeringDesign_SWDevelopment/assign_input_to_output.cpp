#include "assign_input_to_output.h"
#include "Defined_time_activities.hpp"
#include <string>
using namespace std;

//setters
void Day_of_week::set_activity_name(string n)
{
	name = n;
}

void Day_of_week::set_activity_info(string i)
{
	info = i;
}

//getters
string Day_of_week::get_activity_name()
{
	return name;
}

string Day_of_week::get_activity_info()
{
	return info;
}
