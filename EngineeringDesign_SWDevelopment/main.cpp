//
//  main.cpp
//  c++finally
//
//  Created by 吕鸷 on 27/02/2018.
//  Copyright © 2018 Jiayi Zhang. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <new>
#include "Undefined_time_activities.hpp"
#include "Defined_time_activities.hpp"
#include "Inputdata.hpp"
#include "otherfunctions.hpp"
#include "slot_in_function.hpp"

using namespace std;

int main(int argc, const char * argv[]) {

    Time_defined_activities de_activity[18];
    //creat 18 time defined activities to be first defined places in a week
    
    Time_undefined_activities un_activity[10];
    //and then creat another 10 time undefind activities to slot in
    
    defineallactivities(de_activity, un_activity);
	//input all the data from the input file, and give value to the defined activities and undefined activities
    
    Day_of_week Monday[12], Tuesday[12], Wednesday[12], Thursday[12], Friday[12], Saturday[12], Sunday[12];
    //creat 7 days for a week, in a new class called "Day_of_week", in the file "assign_input_to_output"
    
    set_each_day(de_activity, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday);
    //first set the time defined activities, in the file "other functions"
   
    time_undefined_activities_slot_in( un_activity, Monday,Tuesday,Wednesday, Thursday, Friday, Saturday, Sunday);
    //then to set other time undifined activities
    
    Print_output_file(Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday);
    //print them to the output file.
    
    return 0;
}


    
    
    


