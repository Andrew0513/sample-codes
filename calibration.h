#pragma once
#ifndef _CALIBRATION_H_
#define _CALIBRATION_H_
#include <vector>
using namespace std;
bool Get_parameters_for_OU_process(vector<double>& data, vector<double>& parameter, double delta_t);
#endif // !__CALIBRATION_H__
