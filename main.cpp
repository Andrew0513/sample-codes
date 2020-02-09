#include <iostream>
#include <complex>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <stdio.h>
#include "calibration.h"
using namespace std;

template <class Type>
Type stringToNum(const string& str)
{
	istringstream iss(str);
	Type num;
	iss >> num;
	return num;
}

int main()
{
	//get names of csv files
	string list;
	ifstream file_list("D:/file_list.txt");
	file_list >> list;
	file_list.close();

	string::size_type indicator;
	string file_name;
	int pos = 0;
	pos = list.find(",");

	//read files
	vector<double> data;
	data.resize(30000);
	vector<double> parameter = { 0,0,0 };
	double b = 0;
	string temp;
	int count = 0;


	stringstream ss;
	fstream file;
	ofstream fout("D:/parameters.txt");
	fout.close();

	indicator = list.find(",");
	while (indicator != string::npos)
	{
		pos = list.find(",");
		file_name = list.substr(0, pos);
		list = list.substr(pos + 1, -1);
		indicator = list.find(",");
		file.open("D:/FutureIndexDiffs/"+file_name, ios::in);
		while (file >> temp and count <= 20000)
		{
			temp = temp.substr(1 + temp.rfind(","), temp.length() - 1 - temp.rfind(","));
			b = stringToNum<double>(temp);
			data.push_back(b);
			++count;
		}
		file.close();
		Get_parameters_for_OU_process(data, parameter, 1);
		count = 0;
		data.clear();
		fout.open("D:/parameters.txt", ios::app);
		fout << file_name << "," << parameter[0] << "," << parameter[1] << "," << parameter[2] << "\n";
		fout.close();
	}
	file.open("D:/FutureIndexDiffs/" + list, ios::in);
	while (file >> temp and count <= 20000)
	{
		temp = temp.substr(1 + temp.rfind(","), temp.length() - 1 - temp.rfind(","));
		b = stringToNum<double>(temp);
		data.push_back(b);
		++count;
	}
	file.close();
	Get_parameters_for_OU_process(data, parameter, 1);
	count = 0;
	data.clear();
	fout.open("D:/parameters.txt", ios::app);
	fout << file_name << "," << parameter[0] << "," << parameter[1] << "," << parameter[2] << "\n";
	fout.close();

}