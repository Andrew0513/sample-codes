import pandas as pd
import numpy as np
import scipy as sp
import os
import pdb
import gc
from multiprocessing import Pool
import copy
import re

#factors储存方法
#factor_today_temp.to_csv("/mnt/usc1/zhixin/1min_data/factors_data/"+j+"/"+str(k)+".csv",mode='a')
#j 是指数名称 ["50","300","500"]

#数据是从2015-01至2019-04
#factors数据会夹杂factors的因子表达式


path = "/mnt/usc1/zhixin/1min_data/"
index_close=pd.read_csv(path+"index_data.csv")#读入内存

#index_close清洗
drop_index=index_close[index_close[index_close.columns[1]]==index_close.columns[1]].index
index_close=index_close.drop(index=drop_index)
index_close.index=index_close[index_close.columns[0]]
index_close=index_close.drop(columns=index_close.columns[0])
index_close=index_close.astype('float64')
#########################
index_close_return=pd.read_csv(path+"index_close_return.csv")#读入内存
index_close_return.index=index_close_return[index_close_return.columns[0]]
index_close_return=index_close_return.drop(columns=index_close_return.columns[0])

def factors_filter(info):    #info: index name+ list of factors
    index_dic={"50":"上证50","300":"沪深300","500":"中证500"}


#样本内数据 的时间2015-01~2017-07
# len(periods)>=2
#periods=["2015-01","2015-07","2016-01","2016-07","2017-01","2017-07"]
    periods=["2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07"]
    #######################

    drop_time_list=["14:46","14:47","14:48","14:49","14:50","14:51","14:52","14:53","14:54","14:55","14:56","14:57","14:58","14:59","15:00"]
    periods_columns=["2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-01~2015-06"]

#分时间段的单因子IC值
#因子IC值，尝试计算单个因子

    i=info[0]#index name
    pd.DataFrame(columns=periods_columns).to_csv("/mnt/usc1/zhixin/1min_data/factors_data/" + i + "_" + str(info[2])+"_IC.csv",mode='a')
    for j in info[1]: #factors' list  #factor_list存储 因子序号.csv，因子表达式会存在index factor数据里
        IC_in_sample = pd.DataFrame(index=[j], columns=periods_columns)
        factor_df=pd.read_csv("/mnt/usc1/zhixin/1min_data/factors_data/"+i+"/"+j,sep="\n",header=None)

        #把因子数据洗成标准格式 index：时间戳  第一列：因子值
        factor_df.index=factor_df[factor_df.columns[0]].apply(lambda x:(str.split(x,sep=","))[0])
        factor_df[factor_df.columns[0]]=factor_df[factor_df.columns[0]].apply(lambda x:(str.split(x,sep=","))[1])
        drop_index=[k for k in factor_df.index if k[-5:] in drop_time_list]#交易日最后15分钟的数据，避免开盘跳空等造成的误差
        factor_df=factor_df.drop(index=drop_index)
        factor_df.columns=[str.split(j,sep='.')[0]]
        factor_df=factor_df.sort_index(ascending=True)
        factor_df=factor_df.astype('float64')
        index_temp = factor_df.index
        index_temp = index_temp[index_temp >= periods[0]]
        index_temp = index_temp[index_temp < periods[-1]]
        index_close_return_temp = index_close_return[index_dic[i]][index_temp]
        IC_in_sample[periods_columns[-1]][j] = factor_df.corrwith(index_close_return_temp,drop=True).values[0]
        for k in range(len(periods)-1):#长度不同的字符串比较，是从字符串左边开始比较
            index_temp=factor_df.index
            index_temp=index_temp[index_temp>=periods[k]]
            index_temp=index_temp[index_temp<periods[k+1]]
            index_close_return_temp=index_close_return[index_dic[i]][index_temp]
            IC_in_sample[periods_columns[k]][j] = factor_df.corrwith(index_close_return_temp,drop=True).values[0]
        IC_in_sample.to_csv("/mnt/usc1/zhixin/1min_data/factors_data/" + i + "_" + str(info[2])+"_IC.csv",mode='a',header=None)
        del IC_in_sample
        del index_close_return_temp
        del factor_df
        gc.collect()

if __name__=="__main__":
    n=10
    pool=Pool(processes=n)
    #用list保存日期表格
    path="/mnt/usc1/zhixin/1min_data/factors_data/"

    #index_list=['50','300','500']
    index_list = ['50']
    for i in index_list:
        factors_list=os.listdir(path+i)
        factors_list=[j for j in factors_list if j[0:5]!=".fuse"]
        step=int(len(factors_list)/n)
        list_of_factors_lists=[]
        for j in range(n-1):
            list_of_factors_lists.append(factors_list[j*step:(j+1)*step])
        list_of_factors_lists.append(factors_list[(n-1)*step:len(factors_list)])
        print(len(list_of_factors_lists))
        for j in list_of_factors_lists:  #factors_list是list of lists，将一个指数所有因子分成20组
            k=[i,j,list_of_factors_lists.index(j)]
            pool.apply_async(factors_filter,args=(k,))
    pool.close()
    pool.join()