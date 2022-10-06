# -*- coding: UTF-8 -*-
import numpy as np
from scipy.optimize import curve_fit
import csv 
import re
import json
from sklearn import metrics
# import math
import os
# import pandas as pd
# import statsmodels.formula.api as sm
# import matplotlib.pyplot as plt
# plt.switch_backend("agg")

#设置mse阈值
mse_max = 1e-6
mses = []

def get_mse(records_real, records_predict):
    records_real_min = min(records_real)
    records_real_max = max(records_real)
    records_predict_min = min(records_predict)
    records_predict_max = max(records_predict)
    if records_real_max == records_real_min :#标准均一化
        normal_real = [ xi / sum(records_real) for xi in records_real]
        normal_predoct = [xi / sum(records_predict) for xi in records_predict]
    else:#最大最小均一化
        normal_real = [ (xi -records_real_min) / (records_real_max - records_real_min) for xi in records_real]
        normal_predoct = [ (xi -records_predict_min) / (records_predict_max - records_predict_min) for xi in records_predict]
    # mean = sum(records_real) / len(records_real)
    if len(records_real) == len(records_predict):
        mse = sum([(x - y) ** 2 for x, y in zip(normal_real, normal_predoct)]) / len(records_real)
        #R^2
        # R2 =  1 - sum([(x - y) ** 2  / (x - mean)**2 for x, y in zip(records_real, records_predict)]) 
        # R2 = metrics.r2_score(records_real, records_predict)
        mses.append(mse)
        return mse
    else:
        return None

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

#定义你自己想要拟合的函数

def func_serial(x,a,b,c,d):
    return a/x+(b*x**0.5 + c*x) *np.log(x) + d
    #return a/x+(b*x + c*x**0.75) *np.log(x) + e
def func_coll(x,a,b,c,d,e):
    return a*np.log(x) + b*x + c*x**2 + d*x**3+e

def func_coll_nn(x,a,b,c,d,e):
    return a*x**0.5 + (b*x**0.5 + c*x + d)*np.log(x) + e

def func_coll_n1(x,a,b,c,d):
    return (a*x**0.5 + b*x +c) * np.log(x) + d


def func_block(x,a,b,c,d):
    return  a*x + b*x**2 + c*x**3 + d

def func_nonblock(x,a,b,c,d,e):
    return a/x+b*x + c*x**2 + d*x**3 + e

def func_wait(x,a,b,c,d):
    return a/(x**2) + b/x+ c *x **2*np.log(x) + d

def func_test(x,a,b):
    return a*x + b
    
    
#module
def module_fit(x, a,b,c,d,e,f,g,h,i,j,k):
    return a/(x**2) + b / x +c*x**0.5 +  d*x + e*x**2 + f*x**3 + (g*x**0.5 + h*x + i*x**2 + j)*np.log(x) + k
# a/(x**2) + b / x +c*x**0.5 +  d*x + e*x**2 + f*x**3 + g*x**0.5*np.log(x) + h*x*np.log(x) + i*x**2*np.log(x) + j*np.log(x) + k
#定义好自己需要的函数之后就是拟合

def write_result(begin,end, parameter,result):
#将结果写入result
    for i in result:
        if result[i]['down'] >= begin and result[i]['up'] < end:
            result[i]['parameter'] += parameter


def sig(x,down,up):
    if x >= down and x < up :
        return 1
    else:
        return 0

def search_id(xi,x):
    for i in range(len(x)-1):
        down = x[i]
        up = x[i+1]
        sign = sig(xi,down,up)
        if sign == 1:
            return [down,up]
    return None


def module_pre(xi, fitparameter):
    result = []
    for i in fitparameter:
        tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + ({6}*{x}**0.5 + {7}*{x} + {8}*{x}**2 + {9})*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        result.append(tmp_str)
    return '+'.join(result)


def write_parameter(popt, funcname):
    tmp_parameter = np.zeros(11)
    if funcname == "func_coll_nn":
        tmp_parameter[2] += popt[0]
        tmp_parameter[6] += popt[1]
        tmp_parameter[7] += popt[2]
        tmp_parameter[9] += popt[3]
        tmp_parameter[10] += popt[4]
    elif funcname == "func_coll_n1":
        tmp_parameter[6] += popt[0]
        tmp_parameter[7] += popt[1]
        tmp_parameter[9] += popt[2]
        tmp_parameter[10] += popt[3]
    elif funcname == "func_wait":
        tmp_parameter[0] += popt[0]
        tmp_parameter[1] += popt[1]
        tmp_parameter[8] += popt[2]
        tmp_parameter[10] += popt[3]
    elif funcname == "func_block":
        tmp_parameter[3] += popt[0]
        tmp_parameter[4] += popt[1]
        tmp_parameter[5] += popt[2]
        tmp_parameter[10] += popt[3]
    elif funcname == "func_serial":
        tmp_parameter[1] += popt[0]
        tmp_parameter[6] += popt[1]
        tmp_parameter[7] += popt[2]
        tmp_parameter[10] += popt[3]
    elif funcname == "func_nonblock":
        tmp_parameter[1] += popt[0]
        tmp_parameter[3] += popt[1]
        tmp_parameter[4] += popt[2]
        tmp_parameter[5] += popt[3]
        tmp_parameter[10] += popt[4]
    
    return tmp_parameter
    

def piecewise_fit(x,y,mse_max,result,dividenodes,fit_func, funcname):
    size = x.size
    x_ver = np.arange(x[0],x[-1])
    y_liner = []
    for i in range(size-1):
        k = (y[i] - y[i+1])/(x[i]-x[i+1])
        b = y[i] - x[i]*k
        tmp_x = np.arange(x[i],x[i+1])
        tmp_time = func_test(tmp_x,k,b)
        y_liner += list(tmp_time)
    if size == 2:
        popt,pcov = curve_fit(fit_func,x, y, method = "trf", maxfev=50000)
        tmp_parameter = write_parameter(popt, funcname)
        write_result(x[0],x[1]+1,tmp_parameter,result)
    else:
        mse_result = np.zeros((size-2, 4))
        fit_parameter = []
        #找出分段点，分段点筛选: mse 左或右小于mse_max，另一个mse最小。
        for i in range(1,size-1):
            popt = []
            popt_l,pcov_l = curve_fit(fit_func,x[:i+1], y[:i+1], method = "trf", maxfev=50000)
            popt_r,pcov_r = curve_fit(fit_func,x[i:], y[i:], method = "trf", maxfev=50000)
            index = np.where(x_ver == x[i])
            index = list(index[0])
            index = index[0]
            popt_size = len(popt_l)
            if popt_size == 4:
                y_pre_l = fit_func(x_ver[:index+1],popt_l[0],popt_l[1],popt_l[2],popt_l[3])
                y_pre_r = fit_func(x_ver[index:],popt_r[0],popt_r[1],popt_r[2],popt_r[3])
            elif popt_size == 5:
                y_pre_l = fit_func(x_ver[:index+1],popt_l[0],popt_l[1],popt_l[2],popt_l[3],popt_l[4])
                y_pre_r = fit_func(x_ver[index:],popt_r[0],popt_r[1],popt_r[2],popt_r[3],popt_r[4])

            tmp_parameter = write_parameter(popt_l, funcname)
            popt.append(tmp_parameter)
            tmp_parameter = write_parameter(popt_r, funcname)
            popt.append(tmp_parameter)
            fit_parameter.append(popt)
            mse_l = get_mse(y_liner[:index+1], y_pre_l)
            mse_r = get_mse(y_liner[index:], y_pre_r)
            mse_result[i-1][0] = mse_l #分段点左侧mse
            mse_result[i-1][1] = mse_r #分段点右侧mse
            mse_result[i-1][2] = abs(mse_r - mse_l) #两侧mse之差
            mse_result[i-1][3] = x[i] #分段点

        #归类： 1. 左右mse均小于mse_max 2. 有一侧大于mse_max 3. 两侧均大于mse_max

        class1=[]
        class2=[]
        class3=[]
        for i in range(size-2):
            if mse_result[i][0] < mse_max and mse_result[i][1] < mse_max:
                class1.append(i)
            elif mse_result[i][0] < mse_max or mse_result[i][1] < mse_max:
                class2.append(i)
            else:
                class3.append(i)

        if class1:
        #若存在多对均符合要求的分段点，则选择两侧mse差值最小的
            min_id = 0
            min_value = 1e9
            for i in class1:
                if mse_result[i][2] < min_value:
                    min_value = mse_result[i][2]
                    min_id = i
            # begin = x[0] end = x[-1]  piecewise = mse_result[min_id][3]  parameter = fit_parameter[min_id]
            #若end = x[-1] ， 加1 以使最后一段(x[-2] ~ x[-1])可以写入
            dividenodes.append(mse_result[min_id][3])
            write_result(x[0],mse_result[min_id][3]+1,fit_parameter[min_id][0],result)
            write_result(mse_result[min_id][3],x[-1]+1,fit_parameter[min_id][1],result)
        elif class2:
        #对大于MSE_MAX的一侧进行排序，选出最小的MSE
            tmp_list = []
            for i in class2:
                tmp_mse = max(mse_result[i][0], mse_result[i][1])
                tmp_list.append([i,tmp_mse])
            tmp_list = sorted(tmp_list, key = lambda x: x[1])
            tmp_id = tmp_list[0][0]
            index = np.where(x == mse_result[tmp_id][3])
            index = list(index[0])
            index = index[0]
            if mse_result[tmp_id][0] < mse_max:
                dividenodes.append(mse_result[tmp_id][3])
                # begin = x[0] end = piecewise  parameter = fit_parameter[tmp_id][0]
                write_result(x[0],mse_result[tmp_id][3]+1, fit_parameter[tmp_id][0], result)
                #处理大于MSE_MAX一侧的数据
                piecewise_fit(x[index:], y[index:],mse_max,result,dividenodes,fit_func, funcname)
            else:
                dividenodes.append(mse_result[tmp_id][3])
                write_result(mse_result[tmp_id][3], x[-1]+1,fit_parameter[tmp_id][1], result)
                piecewise_fit(x[:index+1], y[:index+1],mse_max,result,dividenodes,fit_func, funcname)
        elif class3:
            #两边均不满足
            tmp_list = []
            for i in class3:
                tmp_list.append([i,mse_result[i][2]])
            tmp_list = sorted(tmp_list, key = lambda x: x[1])
            tmp_id = tmp_list[0][0]
            index = np.where(x == mse_result[tmp_id][3])
            index = list(index[0])
            index = index[0]
            dividenodes.append(mse_result[tmp_id][3])
            piecewise_fit(x[:index+1], y[:index+1],mse_max,result,dividenodes,fit_func, funcname)
            piecewise_fit(x[index:], y[index:],mse_max,result,dividenodes,fit_func, funcname)


def divide_processing(x,y,x_ver,y_liner,tmpresult,result, dividenodes,fit_func, funcname):
    pres = []
    size = x.size
    for xi in x_ver:
        eval_str = module_pre(xi, tmpresult )
        tmp_tuple = [xi]
        pre_time = eval(eval_str)
        tmp_tuple.append(pre_time)
        scope = search_id(xi,x)
        if pre_time < -0.01 or pre_time > eval(module_pre(scope[0],tmpresult))*2 or pre_time > eval(module_pre(scope[1],tmpresult))*2 or pre_time < eval(module_pre(scope[0],tmpresult))*0.5 or pre_time < eval(module_pre(scope[1],tmpresult))*0.5:
            tmp_tuple.append(scope[0])
            tmp_tuple.append(scope[1])
        if len(tmp_tuple) > 2:
            pres.append(tmp_tuple)
    if dividenodes and pres:
        tmp_com = []
        y_mse = []
        popts = []
        for i in range(size-2):
            for j in range(i+1,size-2):
                tmp_com.append([i+1,j+1])
        
        for i in range(len(tmp_com)):
            popt1, pcov1 = curve_fit(fit_func,x[:tmp_com[i][0]+1],y[:tmp_com[i][0]+1],method="trf",maxfev=50000)
            popt2, pcov2 = curve_fit(fit_func,x[tmp_com[i][0]:tmp_com[i][1]+1],y[tmp_com[i][0]:tmp_com[i][1]+1],method="trf",maxfev=50000)
            popt3, pcov3 = curve_fit(fit_func,x[tmp_com[i][1]:],y[tmp_com[i][1]:],method="trf",maxfev=50000)
            
            tmp_parameter1 = write_parameter(popt1, funcname)
            tmp_parameter2 =  write_parameter(popt2, funcname)
            tmp_parameter3 =  write_parameter(popt3, funcname)
            
            popts.append([tmp_parameter1,tmp_parameter2,tmp_parameter3])
            
            index1 = list(np.where(x_ver == x[tmp_com[i][0]])[0])[0]
            index2 = list(np.where(x_ver == x[tmp_com[i][1]])[0])[0]
            
            if len(popt1) == 4:
                y_pre1 = fit_func(x_ver[:index1],popt1[0],popt1[1],popt1[2],popt1[3])
                y_pre2 = fit_func(x_ver[index1:index2],popt2[0],popt2[1],popt2[2],popt2[3])
                y_pre3 = fit_func(x_ver[index2:],popt3[0],popt3[1],popt3[2],popt3[3])
            elif len(popt1) == 5:
                y_pre1 = fit_func(x_ver[:index1],popt1[0],popt1[1],popt1[2],popt1[3],popt1[4])
                y_pre2 = fit_func(x_ver[index1:index2],popt2[0],popt2[1],popt2[2],popt2[3],popt2[4])
                y_pre3 = fit_func(x_ver[index2:],popt3[0],popt3[1],popt3[2],popt3[3],popt3[4])
            
            y_pre = list(y_pre1) + list(y_pre2) + list(y_pre3)
            y_mse.append(get_mse(y_liner,y_pre))
        min_mse = min(y_mse)
        min_index = y_mse.index(min_mse)
        min_popt = popts[min_index]
        write_result(x[0],x[tmp_com[min_index][0]+1],min_popt[0],result)
        write_result(x[tmp_com[min_index][0]],x[tmp_com[min_index][1]+1],min_popt[1],result)
        write_result(x[tmp_com[min_index][1]],x[-1]+1,min_popt[2],result)



comm_coll_nn = 'MPI_Allreduce  MPI_Allgather mpi_allgatherv MPI_Alltoall MPI_Allreduce_ MPI_Allgather_ mpi_allgatherv_ MPI_Alltoall_'

comm_coll_n1 = 'MPI_Bcast MPI_Barrier MPI_Scatter MPI_Gather MPI_Gatherv MPI_Bcast_ MPI_Scatter_ MPI_Gather_ MPI_Reduce MPI_Reduce_ MPI_Scan MPI_Scan_ MPI_Reduce_Scatter MPI_Scatterv MPI_Reduce_Scatter_ MPI_Barrier_ MPI_Gatherv_ MPI_Scatterv_'

comm_block = 'MPI_Send MPI_Ssend MPI_Bsend MPI_Rsend MPI_Recv MPI_Sendrecv MPI_Send_ MPI_Ssend_ MPI_Bsend_ MPI_Rsend_ MPI_Recv_ MPI_Sendrecv_'

comm_nonblock = 'MPI_Isend MPI_Ibsend MPI_Irecv MPI_Issend MPI_Irsend MPI_Isend_ MPI_Ibsend_ MPI_Irecv_ MPI_Issend_ MPI_Irsend_'

comm_wait = 'MPI_Wait MPI_Waitall MPI_Waitany MPI_Wait_ MPI_Waitall_ MPI_Waitany_ MPI_Test_ MPI_Test MPI_Testany MPI_Testany_ MPI_Testsome MPI_Testsome_ MPI_Testall MPI_Testall_ MPI_Waitsome MPI_Waitsome_'

ignore_func = "constituents_cnst_get_type_byind_ wv_saturation_vqsatd_ wv_saturation_fqsatd_ uwshcu_compute_uwshcu_ uwshcu_conden_ wv_saturation_estblf_ mod_comm_mp_recvirr_"
# modules = ["cpl","atm","lnd","ice","ocn","glc","wrf","gea","cplatm","cpllnd","cplice","cplocn","cplglc","cplwrf","cplgea","none"]


if not os.path.exists("./fit_result"):
    os.mkdir("./fit_result")

fit_parameter =open("./fit_result/fit_parameters.json", "w")
fit_fail = open("./fit_result/fit_fail_functions.log", "w")



results = {}
x_pre = np.arange(16,120, 8)
x_str = [str(i) for i in x_pre]
pre_total = np.zeros(x_pre.size)
# for module in modules:
inputfile = "./fit_data"+".csv"
input=open(inputfile,"r")
f = csv.reader(input)
head = next(f)

fit_pre = open("./fit_result"+".csv",'w')

x = np.array([int(str_i) for str_i in head])
num_procs = x.size
x_index = np.argsort(x)
x = x[x_index]

fit_pre.write('func,' + ','.join(x_str))
fit_pre.write('\n')
tmp = next(f)
print(tmp)
# param_bounds_coll_nn=([-np.inf, -np.inf,0,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,30,np.inf,np.inf,np.inf])
# param_bounds_coll_n1=([0, 0,0,-np.inf,-np.inf,0],[1e5,np.inf,30,np.inf,np.inf,1000])
# param_bounds_serial = ([-np.inf,-np.inf,0,-np.inf],[np.inf,np.inf,30,np.inf])
# param_bounds_block = ([-np.inf,-np.inf,0,-np.inf,-np.inf],[np.inf,np.inf,30,np.inf,np.inf])


result = {}
for i in range(num_procs-1):
    result[i] = {}
    result[i]['down'] = x[i]
    result[i]['up'] = x[i+1]
    result[i]['parameter'] = np.zeros(11)

x_ver = np.arange(x[0],x[-1])

for line in f:
    funcname = line[1]
    # if re.search(funcname, ignore_func):
        # continue
    y = [int(line[i])/1e9 for i in range(2,num_procs + 2)]
    y = np.array(y)
    y = y[x_index]
    
    y_liner = []
    for i in range(num_procs-1):
        k = (y[i] - y[i+1])/(x[i]-x[i+1])
        b = y[i] - x[i]*k
        tmp_x = np.arange(x[i],x[i+1])
        tmp_time = func_test(tmp_x,k,b)
        y_liner += list(tmp_time)
    #对在部分进程上不运行的函数的处理
    begin_index = 0
    for i in range(num_procs):
        if y[i] == 0:
            begin_index += 1
        else:
            break
    # if begin_index != 0:
        # print(funcname)
    tmpresult = {}
    for i in range(num_procs-1):
        tmpresult[i] = {}
        tmpresult[i]['down'] = x[i]
        tmpresult[i]['up'] = x[i+1]
        tmpresult[i]['parameter'] = np.zeros(11)
    dividenodes = []
    
    try:
        if re.search(funcname,comm_block,re.IGNORECASE):
            popt,pcov=curve_fit(func_block,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_block(x_ver, popt[0], popt[1], popt[2], popt[3])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index, num_procs-1):
                    result[i]['parameter'][3] += popt[0]
                    result[i]['parameter'][4] += popt[1]
                    result[i]['parameter'][5] += popt[2]
                    result[i]['parameter'][10] += popt[3]
            else:
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult,dividenodes,func_block,'func_block' )
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_block,'func_block' )
        elif re.search(funcname,comm_coll_nn,re.IGNORECASE):
            popt,pcov=curve_fit(func_coll_nn,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_coll_nn(x_ver, popt[0], popt[1], popt[2], popt[3], popt[4])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index,num_procs-1):
                    result[i]['parameter'][2] += popt[0]
                    result[i]['parameter'][6] += popt[1]
                    result[i]['parameter'][7] += popt[2]
                    result[i]['parameter'][9] += popt[3]
                    result[i]['parameter'][10] += popt[4]
            else:
                # print(module,funcname, 'nn')
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult,dividenodes,func_coll_nn,'func_coll_nn' )
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_coll_nn,'func_coll_nn' )
        elif re.search(funcname,comm_coll_n1,re.IGNORECASE):
            popt,pcov=curve_fit(func_coll_n1,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_coll_n1(x_ver, popt[0], popt[1], popt[2], popt[3])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index,num_procs-1):
                    result[i]['parameter'][6] += popt[0]
                    result[i]['parameter'][7] += popt[1]
                    result[i]['parameter'][9] += popt[2]
                    result[i]['parameter'][10] += popt[3]
            else:
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult,dividenodes,func_coll_n1,'func_coll_n1' )
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_coll_n1,'func_coll_n1' )
        elif re.search(funcname,comm_nonblock,re.IGNORECASE):
            popt,pcov=curve_fit(func_nonblock,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_nonblock(x_ver, popt[0], popt[1], popt[2], popt[3], popt[4])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index,num_procs-1):
                    result[i]['parameter'][1] += popt[0]
                    result[i]['parameter'][3] += popt[1]
                    result[i]['parameter'][4] += popt[2]
                    result[i]['parameter'][5] += popt[3]
                    result[i]['parameter'][10] += popt[4]
            else:
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult,dividenodes,func_nonblock,'func_nonblock' )
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_nonblock,'func_nonblock' )
        elif re.search(funcname,comm_wait,re.IGNORECASE):
            popt,pcov=curve_fit(func_wait,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_wait(x_ver, popt[0],popt[1],popt[2],popt[3])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index, num_procs-1):
                    result[i]['parameter'][0] += popt[0]
                    result[i]['parameter'][1] += popt[1]
                    result[i]['parameter'][8] += popt[2]
                    result[i]['parameter'][10] += popt[3]
            else:
                # print(module,funcname,'wait')
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult, dividenodes,func_wait,'func_wait')
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_wait,'func_wait' )             
        else:
            print('fit func_serial')
            popt,pcov=curve_fit(func_serial,x[begin_index:],y[begin_index:],method="trf",maxfev=50000)
            y_pre_ini = func_serial(x_ver,popt[0],popt[1],popt[2],popt[3])
            mse_ini = get_mse(y_liner,y_pre_ini)
            if mse_ini < mse_max:
                for i in range(begin_index,num_procs-1):
                    result[i]['parameter'][1] += popt[0]
                    result[i]['parameter'][6] += popt[1]
                    result[i]['parameter'][7] += popt[2]
                    result[i]['parameter'][10] += popt[3]
            else:
                # print(module, funcname, mse_ini)
                # print(x)
                # print(y)
                piecewise_fit(x[begin_index:],y[begin_index:],mse_max,tmpresult, dividenodes,func_serial,'func_serial')
                tmpresult[0]['down'] = 1
                tmpresult[num_procs-2]['up'] = 9999999
                index = list(np.where(x_ver == x[begin_index])[0])[0]
                divide_processing(x[begin_index:],y[begin_index:],x_ver[index:],y_liner[index:],tmpresult,result, dividenodes,func_serial,'func_serial')
    except RuntimeError:
        fit_fail.write(funcname + "\n")

result[0]['down'] = 1
result[num_procs-2]['up'] = 9999999
fit_pre.write('total_pre')
for xi in range(x_pre.size):
    eval_str = module_pre(x_pre[xi], result )
    pre_time = eval(eval_str)
    pre_total[xi] += pre_time
    fit_pre.write(',' + str(pre_time))
fit_pre.write('\n')
fit_pre.close()
results = result


input.close()

# print(mses)
results_towrite = json.dumps(results, indent = 4,cls=NpEncoder)
fit_parameter.write(results_towrite)
fit_parameter.close()
fit_fail.close()


# for xi in range(x_pre.size):
    # print('procs:', x_pre[xi], 'pre_time: ', pre_total[xi])