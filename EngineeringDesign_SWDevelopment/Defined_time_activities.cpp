#include <iostream>
#include <string>
#include "Defined_time_activities.hpp"
using namespace std;


//setters
void Time_defined_activities::set_defined_activity_name(string activity)
{
	defined_activity_name = activity;
}

void Time_defined_activities::set_weekday(string day)
{
	weekday = day;
}

void Time_defined_activities::set_information(string inf)
{
    information=inf;
}

void Time_defined_activities::set_start_time_hour(int time_hour)
{
	start_time_hour = time_hour;
}

void Time_defined_activities::set_start_time_minute(int time_minute)
{
	start_time_minute = time_minute;
}

void Time_defined_activities::set_end_time_hour(int time_hour)
{
	end_time_hour = time_hour;
}

void Time_defined_activities::set_end_time_minute(int time_minute)
{
	end_time_minute = time_minute;
}


//getters

string Time_defined_activities::get_defined_activity_name()
{
	return defined_activity_name;
}

string Time_defined_activities::get_weekday()
{
	return weekday;
}

string Time_defined_activities::get_information()
{
    return information;
}

int Time_defined_activities::get_start_time_hour()
{
	return start_time_hour;
}

int Time_defined_activities::get_start_time_minute()
{
	return start_time_minute;
}

int Time_defined_activities::get_end_time_hour()
{
	return end_time_hour;
}

int Time_defined_activities::get_end_time_minute()
{
	return end_time_minute;
}
