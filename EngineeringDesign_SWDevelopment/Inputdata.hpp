#ifndef INPUTDATA_H
#define INPUTDATA_H

#include <stdio.h>

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <new>
#include "Undefined_time_activities.hpp"
#include "Defined_time_activities.hpp"
using namespace std;



void gettime(string timestring,int time[]);

void defineallactivities(Time_defined_activities de_activity[],Time_undefined_activities un_activity[]);


#endif /* INPUTDATA_H */
