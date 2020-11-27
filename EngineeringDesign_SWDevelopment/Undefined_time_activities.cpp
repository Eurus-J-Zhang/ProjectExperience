#include <iostream>
#include <string>
#include "Undefined_time_activities.hpp"
using namespace std;


//setters
void Time_undefined_activities::set_undefined_activity_name(string activity)
{
	undefined_activity_name = activity;
}

void Time_undefined_activities::set_activity_duration(int duration)
{
	activity_duration = duration;
}

void Time_undefined_activities::set_activity_times_per_week(int times_week)
{
	times_per_week = times_week;
}

//getters
string Time_undefined_activities::get_undefined_activity_name()
{
	return undefined_activity_name;
}

int Time_undefined_activities::get_activity_duration()
{
	return activity_duration;
}

int Time_undefined_activities::get_activity_times_per_week()
{
	return times_per_week;
}
