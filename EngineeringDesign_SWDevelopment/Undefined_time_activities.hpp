#ifndef Undefined_time_activities_hpp
#define Undefined_time_activities_hpp

using namespace std;
#include <iostream>
#include <string>


//if the time is not defined format:
//activity name, number of times per week, duration of activity
class Time_undefined_activities
{
private:
	int activity_duration, times_per_week;
	string undefined_activity_name;
public:
	//constructor
	Time_undefined_activities(){}
	//setters
	void set_undefined_activity_name(string);
	void set_activity_duration(int);
	void set_activity_times_per_week(int);
	//getters
	string get_undefined_activity_name();
	int get_activity_duration();
	int get_activity_times_per_week();
	//destructor
	virtual ~Time_undefined_activities(){}
};

#endif /* Defined_time_activities_hpp */
