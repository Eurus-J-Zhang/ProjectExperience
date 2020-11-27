//
//  Inputdata.cpp
//  c++finally
//
//  Created by +1 on 20/03/2018.
//  Copyright © 2018 Jiayi Zhang. All rights reserved.
//

#include "Inputdata.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <new>
#include "Undefined_time_activities.hpp"
#include "Defined_time_activities.hpp"
using namespace std;

void gettime(string timestring,int time[])
{
    char char_time[15];
    strcpy_s(char_time, timestring.c_str());
    
    char buf[20];
    
    int i = 0;
    while ( char_time[i] != '\0' )
    {
        if (isdigit(char_time[i]))
            buf[i] = char_time[i];
        else buf[i] = ' ';
        ++i;
    }
    buf[i] = '\0';
    
    sscanf_s (buf,"%d %d %d %d", &time[0], &time[1], &time[2],&time[3]);
}

void defineallactivities(Time_defined_activities de_activity[],Time_undefined_activities un_activity[])
{
    
    string myfile,mystring;
    myfile="H:/year2/coding/project/csv_file.csv";
    ifstream infile;
    infile.open(myfile.c_str());
    
    if(!infile.is_open()) cout<<"ERROR: File could not open"<<endl;
    string activity, day, information;
    string check, na,dua;
    int frequency,duration;
    
    int i=0;
    int k=0;
    int *p;
    
    getline(infile,check,'\n');
    size_t n = count(check.begin(), check.end(), ',');
    n=n/3;
    
    while (infile.good())
    {
        getline(infile,activity,',');
        getline(infile,check,',');
        if (check=="How many times per week?")
        {
            un_activity[i].set_undefined_activity_name(activity);
            getline(infile,check,',');
            frequency=atoi(check.c_str());
            un_activity[i].set_activity_times_per_week(frequency);
            getline(infile,na, ',');
            getline(infile,check,',');
            duration=atoi(check.c_str());
            un_activity[i].set_activity_duration(duration);
            getline(infile, na, '\n');
            i=i+1;
        }
        else
        {
            day=check;
            for(int j=0;j<n;j++)
            {
                de_activity[k].set_defined_activity_name(activity);
                de_activity[k].set_weekday(day);
                getline(infile,dua,',');
                p=new int[4];
                gettime(dua,p);
                
                de_activity[k].set_start_time_hour(p[0]);
                de_activity[k].set_start_time_minute(p[1]);
                de_activity[k].set_end_time_hour(p[2]);
                de_activity[k].set_end_time_minute(p[3]);
                delete[] p;
                
                if (j==2)
                {
                    getline(infile,information,'\n');
                    k=k+1;
                    break;
                }
                else
                {
                    getline(infile,information,',');
                }
                de_activity[k].set_information(information);
                getline(infile,day,',');
                k=k+1;
                if (day=="")
                {
                    getline(infile, na, '\n');
                    break;
                }
                
            }
        }
    }
}
