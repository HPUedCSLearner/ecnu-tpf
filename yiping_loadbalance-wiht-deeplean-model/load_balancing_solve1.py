##! 性能调优主文件
import bisect
import json
import os
import re
import string
import sys
import time
from ast import literal_eval
from xml.dom.minidom import parse

import numpy as np

import optimize


import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed

# 血的教训：必须要设置float64训练
torch.set_default_dtype(torch.float64)

# ==============这个在使用模型的时候，这个必须对应上保存的模型数据=====================
net1 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net2 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net3 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net4 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)


# 放大因子： amplify factor
amplification_factor = 1e4

def getNetVal(net, x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net.forward(ten).data
    res = res.reshape(-1)
    # print("In getNet1Val: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor

def load_deeplearn_model(models, modlepath):
    net1.load_state_dict(torch.load(modlepath + 'model-1.pt'))
    net2.load_state_dict(torch.load(modlepath + 'model-2.pt'))
    net3.load_state_dict(torch.load(modlepath + 'model-3.pt'))
    net4.load_state_dict(torch.load(modlepath + 'model-4.pt'))
    
    # print('===========================')
    # print(getNetVal(net1, 300))
    # print('===========================')
    
    tmp_data = {}
    
    tmp_data[models[0]] = net1
    tmp_data[models[1]] = net2
    tmp_data[models[2]] = net3
    tmp_data[models[3]] = net4
    
    return tmp_data
    
    
def sig(x,down,up):
    if x >= down and x < up :
        return 1 
    else:
        return 0

def module_fit(xi, fitparameter): 
    for i in fitparameter:
        if sig(xi,fitparameter[i]['down'],fitparameter[i]['up']) == 1: 	
            return fitparameter[i]['parameter'][0] / (xi**2) + fitparameter[i]['parameter'][1] / xi + fitparameter[i]['parameter'][2]*xi**0.5 + fitparameter[i]['parameter'][3]*xi + fitparameter[i]['parameter'][4]*xi**2 + fitparameter[i]['parameter'][5]*xi**3 + fitparameter[i]['parameter'][6]*xi**0.5*np.log(xi) + fitparameter[i]['parameter'][7]*xi*np.log(xi) + fitparameter[i]['parameter'][8]*xi**2*np.log(xi) + fitparameter[i]['parameter'][9]*np.log(xi) + fitparameter[i]['parameter'][10]
    print("error parameter!")

def get_fitparameter():

    curpath = os.path.split(os.path.realpath(__file__))[0]
    file_name = curpath + "/fit_parameters.json"
    # models = ['cpl','atm', 'lnd','ice', 'ocn', 'glc', 'wrf', 'gea','cplatm','cpllnd', 'cplice', 'cplocn', 'cplglc', 'cplwrf', 'cplgea', 'none']
    fitparameter_file = open(file_name, "r")
    data = json.load(fitparameter_file)
    fitparameter_file.close()

    return data

def get_data(fitparameters, models, totaltasks, mintasks, ice_procs, deeplearn_models): 
    data = {}
    data['description'] = 'Optimize using data available from original load balancing tool.'
    data['totaltasks'] = totaltasks
    data['models'] = models
    data['models_num'] = len(models)
    if mintasks % 2: 
        data['mintasks'] = mintasks + 1
    else:
        data['mintasks'] = mintasks
    
    ice_procs = sorted(ice_procs)
    if mintasks > ice_procs[0]:
        index = bisect.bisect_right(ice_procs, mintasks)
        ice_procs = ice_procs[index:]    
    data['ice_procs'] = ice_procs

    # 调试用
    # print('===========================')
    # print(getNetVal(deeplearn_models['ice'], 300))
    # print('===========================')
    
    #计算拟合数据
    for model in models:
        tmp_data = {}
        if model == 'ice':
            for i in ice_procs:
                # tmp_data[i] = module_fit(i, fitparameters['ice'])
                tmp_data[i] = getNetVal(deeplearn_models['ice'] ,i)
        else:
            i = mintasks
            while i <= totaltasks:
                # tmp_data[i] = module_fit(i, fitparameters[model])
                tmp_data[i] = getNetVal(deeplearn_models[model] ,i)
                i += 2
        data[model] = tmp_data     
    return data

def model_layout(totaltasks, models, mintasks, ice_procs, deeplearn_models): 
    all_solutions_time = {}
    all_solutions_cost = {}
    fitparameters = get_fitparameter()
    data = get_data(fitparameters, models, totaltasks, mintasks, ice_procs, deeplearn_models)
    
    # 获取某模块数下的布局
    curpath = os.path.split(os.path.realpath(__file__))[0]
    patterns_path = curpath + "/patterns/pattern_" + str(len(models)) + ".out"
    print(patterns_path)
    if not os.path.exists(patterns_path):
        from patterns import generate_patterns
        generate_patterns.get_patterns(model_num)
    patterns_file = open(patterns_path, 'r')
    
    # 获取最优方案
    mintime_best_pattern = []
    mintime_best_time = sys.maxsize
    mintime_best_individual = []
    mincost_best_pattern = []
    mincost_best_time = sys.maxsize
    mincost_best_individual = []
    
    while True:
        lines = patterns_file.readlines(20)
        if lines:
            for pattern in lines:
                pattern = eval(pattern.strip())
                tmp_mintime_best_individual ,tmp_mintime_best_time = optimize.optimize_mintime(pattern, data) 
                if tmp_mintime_best_time < mintime_best_time:
                    mintime_best_time = tmp_mintime_best_time
                    mintime_best_individual = tmp_mintime_best_individual
                    mintime_best_pattern = pattern
                tmp_mincost_best_individual ,tmp_mincost_best_time = optimize.optimize_mincost(pattern, data) 
                if tmp_mincost_best_time < mincost_best_time:
                    mincost_best_time = tmp_mincost_best_time
                    mincost_best_individual = tmp_mincost_best_individual
                    mincost_best_pattern = pattern    
        else: 
            break
        
    min_root = data['totaltasks']
    for i in range(len(mintime_best_individual)):
        if (i % 2 == 0) :
            min_root = min(min_root, mintime_best_individual[i])
    for i in range(len(mintime_best_individual)):
        if (i % 2 == 0) :
            mintime_best_individual[i] -= min_root
    print('best_mintime_pattern:',mintime_best_pattern)
    print('best_mintime_time:',mintime_best_time)
    print('best_mintime_individual:',mintime_best_individual)
    
    min_root = data['totaltasks']
    for i in range(len(mincost_best_individual)):
        if (i % 2 == 0) :
            min_root = min(min_root, mincost_best_individual[i])
    for i in range(len(mincost_best_individual)):
        if (i % 2 == 0) :
            mincost_best_individual[i] -= min_root
    print('best_mincost_pattern:',mincost_best_pattern)
    print('best_mincost_time:',mincost_best_time)
    print('best_mincost_individual:',mincost_best_individual)
        
    patterns_file.close()
    end_time = time.time()
    execution_time = end_time - start_time
    print("layout execution time:", execution_time, "seconds")
    
    return mintime_best_individual, mincost_best_individual



if __name__ == "__main__" :
    start_time = time.time()

    # totaltasks = int(sys.argv[1])
    # blocksize = int(sys.argv[2])
    totaltasks = 1024
    mintasks = 4
    # nthrds = 1

    # models = ['atm', 'ocn', 'ice', 'lnd', 'cpl', 'cplatm', 'cpllnd', 'cplocn']
    models = ['atm', 'ocn', 'ice', 'lnd']
    ice_procs = [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]
    # pefilename = './env_mach/env_mach_pes.xml'
    #### fitparameter = get_fitparameter()

    # 加载深度学习模型
    deeplearn_models = load_deeplearn_model(models, '/home/feng/wys/github/ecnu-tpf/yiping_loadbalance-wiht-deeplean-model/deeplearn-models/')
    
    best_solution = model_layout(totaltasks, models, mintasks, ice_procs, deeplearn_models)
    print(best_solution)
    run_time = time.time() - start_time
    print("run time: ", run_time, "s")

