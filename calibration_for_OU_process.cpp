#include <vector>
#include <iostream>
#include <cmath>
#include "calibration.h"
using namespace std;

/* 
	OU process: dS(t)=lambda*(u-S(t))dt+sigma*dW(t)
	函数参数data是S(t)在不同时刻的取值，以分钟作为计时单位
	delta_t是数据之间的时间间隔，计算alpha会用到。
	假设三个参数是常数，用MLE估计参数
	返回向量地址 parameter是三维向量，（u，lambda,sigma）
*/

bool Get_parameters_for_OU_process(vector<double> &data, vector<double> &parameter,double delta_t)
{
	double Sx=0,Sy=0,Sxx=0,Sxy=0,Syy=0,alpha=0;
	for (auto iter = data.cbegin(); iter != data.cend(); ++iter)
	{
		Sx = Sx + *iter;
		Sxx = Sxx + (*iter) * (*iter);
	}
	Sy = Sx - data[0];
	Sx = Sx - data[data.size() - 1];
	Syy = Sxx - data[0] * data[0];
	Sxx = Sxx - data[data.size() - 1] * data[data.size() - 1];
	for (int i = 0; i < data.size() - 1; ++i)
	{
		Sxy = Sxy + data[i] * data[i + 1];
	}
	parameter[0] = (Sy * Sxx - Sx * Sxy) / (data.size() * (Sxx - Sxy) - Sx * (Sx - Sy));
	parameter[1] = (log(Sxx - 2 * parameter[0] * Sx + data.size() * parameter[0] * parameter[0])  - log(Sxy - parameter[0] * (Sx + Sy) + data.size() * parameter[0] * parameter[0]) )/ 8;
	alpha = exp(-parameter[1] * delta_t);
	parameter[2] = (Syy - 2 * alpha * Sxy + alpha * alpha * Sxx - 2 * parameter[0] * (1 - alpha) * (Sy - alpha * Sx) + data.size() * parameter[0] * parameter[0] * (1 - alpha) * (1 - alpha)) * 2 * parameter[1] / (data.size() * (1 - alpha * alpha));
	return 1;

}