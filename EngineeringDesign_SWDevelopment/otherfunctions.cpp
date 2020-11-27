#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "otherfunctions.h"
#include "Defined_time_activities.hpp"
using namespace std;

void Print_output_file(Time_defined_activities de_activity[])
{
	Day_of_week Monday[12], Tuesday[12], Wednesday[12], Thursday[12], Friday[12], Saturday[12], Sunday[12];
	string Row[13];

	set_each_day(de_activity, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday);

	string name, Output_File_Name;
	cout << endl << "enter output file: ";
	cin >> Output_File_Name;

	ofstream Output_File;
	Output_File.open(Output_File_Name);

	//if cant open file return ERROR
	if (!Output_File.is_open())
		cout << "ERROR: File Open" << endl;

	//clear output file before writing to it 
	Output_File.clear();


	//print empty cell at top left
	Output_File << ",";

	//print top line of times 
	for (int i = 9; i < 22; i++)
	{
		Output_File << i << ":00" << " - " << i + 1 << ":00" << ",";
	}
	Output_File << endl;


	////////////// PRINT MONDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Monday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Monday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Monday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;


	////////////// PRINT TUESDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Tuesday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Tuesday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Tuesday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;

	

	////////////// PRINT WEDNESDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Wednesday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Wednesday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Wednesday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;


	////////////// PRINT THURSDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Thursday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Thursday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Thursday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;


	////////////// PRINT FRIDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Friday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Friday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Friday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;

	////////////// PRINT SATURDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Saturday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Saturday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Saturday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;

	////////////// PRINT SUNDAYS SCHEDULE AND AN EMPTY ROW TO INCREASE READIBILITY BENEATH
	Output_File << "Sunday" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Sunday[i].get_activity_name() << ",";
	}
	Output_File << endl;

	Output_File << "information" << ",";
	for (int i = 0; i < 12; i++)
	{
		Output_File << Sunday[i].get_activity_info() << ",";
	}
	Output_File << endl;

	for (int i = 0; i < 12; i++)
	{
		Output_File << Row[i] << ",";
	}
	Output_File << endl;

	Output_File.close();

	for (int a = 0; a < 12; a++)
	{
		cout << "Monday" << Monday[a].get_activity_name() << endl;
	}
	cout << endl;
	for (int b = 0; b < 18; b++)
	{
		cout << "days: " << de_activity[b].get_start_time_hour() << endl;
	}
}

////////////////////////////SET EACH DAY

void set_each_day(Time_defined_activities de_activity[], Day_of_week Monday[], Day_of_week Tuesday[], Day_of_week Wednesday[], Day_of_week Thursday[], Day_of_week Friday[], Day_of_week Saturday[], Day_of_week Sunday[])
{
	
	int a;
	int b; 
	for (int i = 0; i < 18; i++)
	{
		if (de_activity[i].get_weekday() == "Monday" )
		{
			a = de_activity[i].get_start_time_hour();
			b = de_activity[i].get_end_time_hour(); 
			if (b - a == 1)
			{
				Monday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 9].set_activity_info(de_activity[i].get_information());
			}
			else if (b - a == 2)
			{
				Monday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 9].set_activity_info(de_activity[i].get_information());
				Monday[a - 8].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 8].set_activity_info(de_activity[i].get_information());
			}
			else if (b-a == 3)
			{
				Monday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 9].set_activity_info(de_activity[i].get_information());
				Monday[a - 8].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 8].set_activity_info(de_activity[i].get_information());
				Monday[a - 7].set_activity_name(de_activity[i].get_defined_activity_name());
				Monday[a - 7].set_activity_info(de_activity[i].get_information());
			}
			
		}
		else if (de_activity[i].get_weekday() == "Tuesday")
		{
			a = de_activity[i].get_start_time_hour();
			Tuesday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Tuesday[a - 9].set_activity_info(de_activity[i].get_information());
		}
		else if (de_activity[i].get_weekday() == "Wednesday")
		{
			a = de_activity[i].get_start_time_hour();
			Wednesday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Wednesday[a - 9].set_activity_info(de_activity[i].get_information());
		}
		else if (de_activity[i].get_weekday() == "Thursday")
		{
			a = de_activity[i].get_start_time_hour();
			Thursday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Thursday[a - 9].set_activity_info(de_activity[i].get_information());
		}
		else if (de_activity[i].get_weekday() == "Friday")
		{
			a = de_activity[i].get_start_time_hour();
			Friday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Friday[a - 9].set_activity_info(de_activity[i].get_information());
		}
		else if (de_activity[i].get_weekday() == "Saturday")
		{
			a = de_activity[i].get_start_time_hour();
			Saturday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Saturday[a - 9].set_activity_info(de_activity[i].get_information());
		}
		else if (de_activity[i].get_weekday() == "Sunday")
		{
			a = de_activity[i].get_start_time_hour();
			Sunday[a - 9].set_activity_name(de_activity[i].get_defined_activity_name());
			Sunday[a - 9].set_activity_info(de_activity[i].get_information());
		}

	}




}
