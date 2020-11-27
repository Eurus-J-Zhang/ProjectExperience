//
//  Defined_time_activities.hpp
//  c++finally
//
//  Created by 吕鸷 on 06/03/2018.
//  Copyright © 2018 Jiayi Zhang. All rights reserved.
//

#ifndef Defined_time_activities_hpp
#define Defined_time_activities_hpp

#include <stdio.h>
#include <string>
using namespace std;

//format of csv data being read in:
//activity name, day, start time, end time
class Time_defined_activities
{
private:
    string defined_activity_name, weekday, information;
    int start_time_hour, start_time_minute, end_time_hour, end_time_minute;
public:
    //constructor
    Time_defined_activities(){}
    //setters
    void set_defined_activity_name(string);
    void set_weekday(string);
    void set_information(string);
    void set_start_time_hour(int);
    void set_start_time_minute(int);
    void set_end_time_hour(int);
    void set_end_time_minute(int);
    //getters
    string get_defined_activity_name();
    string get_weekday();
    string get_information();
    int get_start_time_hour();
    int get_start_time_minute();
    int get_end_time_hour();
    int get_end_time_minute();
    //destructor
    virtual ~Time_defined_activities(){}
    
};


#endif /* Defined_time_activities_hpp */
