import re
import numpy as np
import json
import sys
import os
import logging
from ast import literal_eval
import optimize_model
import string
from xml.dom.minidom import parse


#logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #日志等级为DEBUG
logger.addHandler(logging.StreamHandler(sys.stderr))

curpath = os.path.split(os.path.realpath(__file__))[0]

def sig(x,down,up):
    if x >= down and x < up :
        return 1
    else:
        return 0

def module_fit(xi, fitparameter):
    # print('WYS Debug:\t come to module_fit')
    print('wyswys Debug:\t come to module_fit .....')
    result = []
    for i in fitparameter:
        tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + {6}*{x}**0.5*np.log({x}) + {7}*{x}*np.log({x}) + {8}*{x}**2*np.log({x}) + {9}*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        result.append(tmp_str)
    return '+'.join(result)

def generate_layout(models, option, mintime = None):
    tmp_models = []
    for model in models:
        tmp_models.append(model)
    
    num_models = len(tmp_models)
    #改为默认排布：atm : 1, ocn: 2, lnd : 3, ice : 4, 其他：5、6、......
    if 'ice' in tmp_models:
        tmp_models.remove('ice')
        tmp_models.insert(0,'ice')
    if 'lnd' in tmp_models:
        tmp_models.remove('lnd')
        tmp_models.insert(0,'lnd')
    if 'ocn' in tmp_models:
        tmp_models.remove('ocn')
        tmp_models.insert(0,'ocn')
    if 'atm' in tmp_models:
        tmp_models.remove('atm')
        tmp_models.insert(0,'atm')
    # print(tmp_models)
    #patterns
    patternpath = curpath + "/patterns/pattern_" + str(num_models)+".out"
    patterns = open(patternpath, 'r')
    patterns_list = patterns.read().split('\n')
    patterns.close

    #template
    templatepath = curpath + "/template/layout_"+ str(num_models) + '_'+ option +".template"
    template = string.Template(open(templatepath, 'r').read())
    
    #write to layout function
    funcpath = curpath + "/write_to_layout.py"
    function = open(funcpath, 'r').read()

    #layout class
    layoutclasspath = "/layout_" + str(num_models) + '_'+ option +".py"
    layoutclass = open(curpath + layoutclasspath, 'w')
    
    layoutclass.write(function)
    print('WYS Debug:\t function\t', function) 
    # print(patterns_list)
    
    layouts = {}
    for i in range(len(patterns_list)):
        pattern = literal_eval(patterns_list[i])
        tmp_dict = {}
        tmp_pattern = []
        for tmp_tuple in pattern:
            tmp_list = []
            tmp_list.append(tmp_models[tmp_tuple[0]-1])
            tmp_dict[tmp_models[tmp_tuple[0]-1]] = '0'
            for j in range(1, len(tmp_tuple)):
                tmp_list.append(tmp_models[tmp_tuple[j]-1])
                if tmp_dict[tmp_models[tmp_tuple[j-1]-1]] == '0':
                    tmp_dict[tmp_models[tmp_tuple[j]-1]] = 'n' + tmp_models[tmp_tuple[j-1]-1]
                else:
                    tmp_dict[tmp_models[tmp_tuple[j]-1]] = tmp_dict[tmp_models[tmp_tuple[j-1]-1]] + '+' + 'n' + tmp_models[tmp_tuple[j-1]-1]
            tmp_pattern.append(tmp_list)
        
        classname= ''.join(tmp_models) + str(i)
        layouts[layoutclasspath[1:-2] + classname] = tmp_pattern
        
        constraint = ''
        
        X_range = []
        for tmp_tuple in pattern:
            X_constraint = ""
            for j in range(len(tmp_tuple)):
                if j == 0:
                    X_constraint  += "x[%d]"%(tmp_tuple[j]-1)
                else:
                    X_constraint  += " +" + " x[%d]"%(tmp_tuple[j]-1)
            X_range.append(X_constraint)
            X_constraint  = "self.maxtasks - (" + X_constraint + ")"
            one_constraint =  ' '*8 + "constraints.append({'type': 'ineq', 'fun': lambda x : %s})\n"%(X_constraint)
            constraint += one_constraint
        tmp_roots = ''
        for j in range(num_models):
            tmp_roots += ", '%s': %s"%(tmp_models[j], tmp_dict[tmp_models[j]])
        roots = "{'cpl':0 %s}"%tmp_roots
        
        lines = []
        if mintime:
            if num_models == 2:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            elif num_models == 3:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            elif num_models == 4:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3],  ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            elif num_models == 5:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            #添加 模式分量为6/7/8的
            elif num_models == 6:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], MODEL6 = tmp_models[5], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            elif num_models == 7:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], MODEL6 = tmp_models[5], MODEL7 = tmp_models[6], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern, MINTIME=mintime, X_RANGE=X_range))
            layoutclass.writelines(lines)
        else:
            if num_models == 2:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            elif num_models == 3:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            elif num_models == 4:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3],  ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            elif num_models == 5:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            #添加 模式分量为6/7/8的
            elif num_models == 6:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], MODEL6 = tmp_models[5], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            elif num_models == 7:
                lines.append(template.substitute(CLASSNAME=classname, MODEL1=tmp_models[0], MODEL2 = tmp_models[1], MODEL3 = tmp_models[2],MODEL4= tmp_models[3], MODEL5 = tmp_models[4], MODEL6 = tmp_models[5], MODEL7 = tmp_models[6], ROOTS=roots, CONSTRAINT = constraint,  PATTERN = pattern))
            layoutclass.writelines(lines)
        
    # layoutnames.close
    layoutclass.close
    # print(layouts)
    return layouts
    
def get_fitfitparameter():#调试用
    #单机调试阶段, 使用文件输入
    file_name = curpath + "/fit_parameters.json"
    models = ['cpl','atm', 'lnd','ice', 'ocn', 'glc', 'wrf', 'gea','cplatm','cpllnd', 'cplice', 'cplocn', 'cplglc', 'cplwrf', 'cplgea', 'none']
    fitparameter_file = open(file_name, "r")
    data = json.load(fitparameter_file)
    # fitparameter_lines = fitparameter_file.readlines()
    # fitparameter_file.close()
    # for line in fitparameter_lines:
        # line_split = line.split(',')
        # data[models[int(line_split[0])]] = [float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4]), float(line_split[5]), float(line_split[6]), float(line_split[7]), float(line_split[8]), float(line_split[9]), float(line_split[10]), float(line_split[11])]
    return data

def wys_get_fitfitparameter(file_name):
    fitparameter_file = open(file_name, "r")
    data = json.load(fitparameter_file)
    return data

def get_data(fitparameters, models, totaltasks,mintasks,  layout, ice_procs):
    data = {}
    data['description'] = 'Optimize using data available from original load balancing tool.'
    data['layout'] = layout
    data['totaltasks'] = totaltasks
    data['mintasks'] = mintasks
    data['ice_procs'] = ice_procs
    #计算拟合数据
    for model in models:
        tmp_data = {}
        tmp_data['fitparameter'] = fitparameters[model]
        data[model.upper()] = tmp_data
        
    return data

def wys_get_data(wys_fitparameters, models, totaltasks,mintasks,  layout, ice_procs):
    data = {}
    data['description'] = 'Optimize using data available from original load balancing tool.'
    data['layout'] = layout
    data['totaltasks'] = totaltasks
    data['mintasks'] = mintasks
    data['ice_procs'] = ice_procs
    # print('wys model data', wys_fitparameters['ice']['3'])
    #计算拟合数据
    for model in models:
        data[model.upper()] = wys_fitparameters[model]
    return data
    
def write_pe_template(pefilename, ntasks, roots, totaltasks):
    #写入排布结果到env_mach_pes.xml, 暂时不用
    domTree = parse(curpath + "/template/env_mach_pes.template")
    
    rootNode = domTree.documentElement

    entrys = rootNode.getElementsByTagName('entry')
    for entry in entrys:
        id = entry.getAttribute('id')
        module = id[-3:].lower()
        if id[:6] == 'NTASKS':
            if module in ntasks: 
                entry.setAttribute('value', str(ntasks[module]))
            else:
                entry.setAttribute('value', str(totaltasks))
        if id[:4] == 'ROOT':
            if module in ntasks: 
                entry.setAttribute('value', str(roots[module]))
            else:
                entry.setAttribute('value', '0')

    pefile = open(pefilename, 'w')
    domTree.writexml(pefile, addindent='  ', encoding='utf-8')

def model_layout(totaltasks, models, mintasks,  fitparameters, wys_fitparameters, ice_procs):
    #针对所有布局的进程排布，例如ATMLNDICEOCN
    # fitfitparameter = get_fitfitparameter()
    
    all_solutions_time = {}
    all_solutions_cost = {}
    
    #时间最小方案
    layouts_mintime = generate_layout(models,option = 'mintime')
    # print('WYS Debug:layouts_mintime\t', layouts_mintime)
    for layout in layouts_mintime:
        # print('WYS Debug:\t layout:', layout)
        # print('WYS Debug:\t layouts_mintime[layout]: ', layouts_mintime[layout])
        # print()
        data = get_data(fitparameters, models, totaltasks, mintasks, layout,ice_procs)
        wys_data = wys_get_data(wys_fitparameters, models, totaltasks, mintasks, layout,ice_procs)
        # print('WYS Debug:\t data\t', data)
        print('wys:\t get_data\t', data)
        print('wys:\t wys_get_data\t', wys_data)
        # print()
        opt = optimize_model.solver_factory(data)
        wys_opt = optimize_model.wys_solver_factory(wys_data)
        print('WYS Debug:\t opt\t', opt) # <layout_4_mintime.atmocnlndice0 object at 0x2b8649108f50>
        print()
        
        print('WYS Debug:\t Before  opt.optimize()')
        status = opt.optimize()
        print('WYS Debug:\t End     opt.optimize()')
        
        solution = opt.get_solution()
        if solution != False:
            # print("solution: ",solution)
            if 'mintime' in solution:
                all_solutions_time[layout] = solution['mintime']
    if all_solutions_time:
        sort_allsolutions_mintime = sorted(all_solutions_time.items(), key = lambda x:x[1]['mintime'])
        best_solution_mintime = sort_allsolutions_mintime[0]
        print("mintime solution: ",best_solution_mintime[1])
    else:
        print("mintime solution fail")
        best_solution_mintime = None
    
    
    #机时最小方案
    orgin_time = 0 #原始串行运行时间估算
    for model in models:
        if model == 'lnd' and totaltasks > 128:
            tmp_str = module_fit('128', fitparameters[model])
        else:
            tmp_str = module_fit(str(totaltasks), fitparameters[model])
        orgin_time += eval(tmp_str)

    layouts_mincost = generate_layout(models, option= 'mincost', mintime = orgin_time)
    for layout in layouts_mincost:
        data = get_data(fitparameters,models, totaltasks, mintasks, layout,ice_procs)
        opt = optimize_model.solver_factory(data)
        status = opt.optimize()
        solution = opt.get_solution()
        if solution != False:
            # print("solution: ",solution)
            if 'mincost' in solution:
                all_solutions_cost[layout] = solution['mincost']
    if all_solutions_cost:
        sort_allsolutions_mincost = sorted(all_solutions_cost.items(), key = lambda x:x[1]['mincost'])
        best_solution_mincost = sort_allsolutions_mincost[0]
        print("mincost solution: ",best_solution_mincost[1])
        # write_pe_template(pefilename, best_solution[1]['ntasks'], best_solution[1]['roots'], totaltasks)
    else:
        print("mincost solution fail")
        best_solution_mincost = None
    
    return best_solution_mintime, best_solution_mincost


if __name__ == "__main__" :

    # totaltasks = int(sys.argv[1])
    # blocksize = int(sys.argv[2])
    mintask = 4
    nthrds = 1

    models = ['atm', 'lnd', 'ice', 'ocn']
    
    pefilename = './env_mach/env_mach_pes.xml'
    fitfitparameter = get_fitfitparameter()  # wys: json load fit_parameters.json
    wys_fitfitparameter = wys_get_fitfitparameter('./trans_fit_parameters.json')
    # print('WYS Debug:\t', fitfitparameter)
    # best_solution = model_layout(totaltasks, blocksize, models, mintask, pefilename,fitfitparameter)
    # model_layout(totaltasks, models, mintasks,  fitparameters, ice_procs):
    # model_layout(totaltasks, models, mintasks,  fitparameters, wys_fitparameters, ice_procs):
    model_layout(1024, models, 4,  fitparameters = fitfitparameter, wys_fitparameters = wys_fitfitparameter, ice_procs = [4, 16, 32, 64, 128])
    # print(best_solution)
    
    
    
    
