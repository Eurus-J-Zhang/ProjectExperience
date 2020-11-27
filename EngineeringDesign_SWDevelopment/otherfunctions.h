#include <iostream>
#include <string>
#include "Defined_time_activities.hpp"
#include "assign_input_to_output.h"
using namespace std;

#ifndef CREATE_TEMPLATE_TIMETABLE_H_
#define CREATE_TEMPLATE_TIMETABLE_H_

void Print_output_file(Time_defined_activities de_activity[]);
void set_each_day(Time_defined_activities de_activity[], Day_of_week Monday[], Day_of_week Tuesday[], Day_of_week Wednesday[], Day_of_week Thursday[], Day_of_week Friday[], Day_of_week Saturday[], Day_of_week Sunday[]);
#endif /*CREATE_TEMPLATE_TIMETABLE*/