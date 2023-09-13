# -*- coding: UTF-8 -*-
import optimize_model
from scipy.optimize import minimize
import numpy as np

def sig(x,down,up):
    if x >= down and x < up :
        return 1
    else:
        return 0

# WYS:相当于把模型加起来
def module_fit(xi, fitparameter):
    print('WYS Debug:\t come to module_fit')
    print('wyswys fitparameter:', fitparameter)
    result = []
    for i in fitparameter:
        tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + {6}*{x}**0.5*np.log({x}) + {7}*{x}*np.log({x}) + {8}*{x}**2*np.log({x}) + {9}*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        print('WYS Debug:\t i->', i)
        print('WYS Debug:\t tmp_str->', tmp_str)
        print()
        result.append(tmp_str)
        print('WYS Debug:\t result->', result)
        # print('WYS Debug:\t result->', result)
        # print('WYS Debug:\t result->', result)
        # print('WYS Debug:\t result->', result)
        print()
    return '+'.join(result) # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串

# WYS:相当于把模型加起来
def wys_module_fit(xi,  moduledata):
    result = []
    for i in fitparameter:
        # tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + {6}*{x}**0.5*np.log({x}) + {7}*{x}*np.log({x}) + {8}*{x}**2*np.log({x}) + {9}*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        tmp_str = "moduledata[{x}]".format(x = xi)
        result.append(tmp_str)
    return '+'.join(result) # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串

def conduct_pattern(pattern):
    pattern_len = []
    for i in range(0,len(pattern)):
        pattern[i] = list(pattern[i])
        pattern[i].reverse()
        pattern_len.append(len(pattern[i]))
    tmp_len = pattern_len.copy()
    tmp_len.sort()
    while(tmp_len[0] != tmp_len[-1]):
        index = pattern_len.index(tmp_len[0]) #最小索引
        pattern_len[index] += 1
        pattern[index].insert(0, pattern[index][0])
        tmp_len = pattern_len.copy()
        tmp_len.sort()

def remove_same(pattern):
    if len(pattern) == 1:
        return False
    flag=True
    tmp1=pattern[0][0]
    for p in pattern:
        if p[0] != tmp1:
            flag = False
            break
    return flag

def max_prime(x):
    i = 1
    max_i = 1
    while i < x:
        i += 1
        if x % i == 0:
            x = x / i
            if max_i < i:
                max_i = i
            i  = 1
    return max_i

#机时最省容差
allowance = 0.00
class atmocnlndice0(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2,), (1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': natm+nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice1(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3), (1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': natm}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice2(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice3(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice4(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2,), (3,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice5(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 2), (4, 1, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[2])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nice, 'ocn': nice, 'lnd': nice+natm, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice6(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice7(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice8(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3), (1,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice9(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 4, 3), (1, 4, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[1])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm+nice, 'lnd': natm+nice, 'ice': natm}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice10(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2, 4), (3,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nocn}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice11(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2,), (3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice12(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 2, 3), (4, 1)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nice, 'ocn': nice, 'lnd': nice+nocn, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice13(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice14(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3, 4), (2, 1)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[0])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nocn, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice15(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 3), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nocn}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice16(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice17(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 4), (1, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': nocn}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice18(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3, 4), (3, 1, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[0] + x[1])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nlnd, 'ocn': nlnd+natm, 'lnd': 0, 'ice': nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice19(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3,), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': natm+nocn}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice20(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3, 4, 1), (3, 4, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[1])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nlnd+nice, 'ocn': nlnd+nice, 'lnd': 0, 'ice': nlnd}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice21(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (3,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice22(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2,), (1, 3), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice23(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndice24(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
            
    def optimize(self):

        print('WYS Debug:\t come to templte optimize')

        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 1, 2), (4, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        print('WYS Debug: optimize::len(tmp_pattern)\t ', len(tmp_pattern))
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        print('WYS Debug: optimize::tmp_pattern\t ', tmp_pattern)

        tmp_strlist = []
        wys_strlist = []
        #atm
        #wys_strlist.append(wys_module_fit("x[0]", self.wys_models['atm'.upper()]))
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times1\t ', tmp_strlist)
        print()

        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
        print('WYS Debug: optimize::tmp_strlist::times2\t ', tmp_strlist)
        print()


        #判断是否存在ice与lnd
        #yeeland
        flag1 = 0
        if  'lnd'.upper() == 'LND' and  'ice'.upper() == "ICE":
            flag1 = 1
        flag2 = 0
        for tmp_list in tmp_pattern:
            #若存在ice与lnd，判断 lnd ice是否并行
            if 3 in tmp_list and 4 in tmp_list and flag1 == 1:
                flag2 = 1
        # WYS: 根据Flag判断，ice与lnd 的模块是否使用max()
        if flag2 == 1:
            print('WYS Debug:\t come to flag2 == 1')
            print()
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            print('WYS Debug:\t come to flag2 == 2')
            print()
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        
        print('WYS Debug: optimize::tmp_strlist::times3\t ', tmp_strlist)
        print()

        # 也就是说，eval_str是所有模式加起来; 
        # 进程用x[0]\x[1]\x[2]...代替; 
        # 每个模式的不同段也是加起来，通过符号sig(x[0],1,30)筛选进程
        eval_str = '+'.join(tmp_strlist)#规划主函数

        print('WYS Debug:\t tmp_strlist::after "+".join():->eval_str\t', eval_str, '\n')
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        print('WYS Debug:\t tmp_models\t', tmp_models, '\n')

        # 设置不同模块的进程边界（mintasks, maxtasks）
        bnds = []
        for tmp_model in tmp_models:
            # WYS: 如果是LDN模块，并且最大进程数>128
            if tmp_model== 'LND' and self.maxtasks > 128:
                print('WYS Debug:\t tmp_model== LND\t''\n')
                bnd =  (self.mintasks, 128) # WYS：也就是说，这里LDN的最大进程数最大可以设置为128
            else:
                print('WYS Debug:\t else: tmp_model == LND\t''\n')
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
            print('WYS Debug:\t bnds\t', bnds, '\n')
        bnds = tuple(bnds)
        print('WYS Debug:\t tuple(bnds)\t', bnds, '\n')



        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[2])})

        print('WYS Debug:\tconstraints\t', constraints, '\n')
        
        time_func = lambda x: eval(eval_str)
        print('WYS Debug:\t time_func\t', time_func, '\n')
        
        x0 = [self.mintasks]*4 # WYS：[4] * 4 ->  [4, 4, 4, 4]
        print('WYS Debug:\t x0\t', x0, '\n')
        
        #运行时间最少方案
        # WYS：SLSQP非线性求解 （非线性规划是指目标函数或约束条件中包含非线性函数的规划问题，实际就是非线性最优化问题）
        solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        print('WYS Debug:\t solution\t', solution, '\n')
        
        if not solution.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        self.X = {}
        ntasks = solution.x
        print('WYS Debug:\t ntasks\t', ntasks, '\n')

        for i in range(len(ntasks)):
            ntasks[i] = int(ntasks[i])
        self.X['mintime'] = time_func(ntasks)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice}
        ice_procs = self.ice_procs
        if 'ice' in ntasks:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks['ice']
            if ice_proc_pre not in ice_procs:
                ice_proc_result = -1
                if ice_procs[0] > ice_proc_pre:
                    ice_proc_result = ice_procs[0]
                elif ice_procs[-1] < ice_proc_pre:
                    ice_proc_result = ice_procs[-1]
                else:
                    for i in range(1, len(ice_procs)):
                        if ice_procs[i-1] <= ice_proc_pre and ice_procs[i] > ice_proc_pre:
                            ice_proc_result = ice_procs[i-1]
                            break
                ntasks['ice'] = int(ice_proc_result)
                nice = ntasks['ice']
        # print(solution.success)
        roots = {'cpl':0 , 'atm': nice, 'ocn': nice+natm, 'lnd': nice, 'ice': 0}
        self.X['ntasks']  = ntasks
        self.X['roots'] = roots
        
        self.solution = {}
        if solution.success:
            self.solution['mintime'] = self.X
        
        self.set_state(solution.success)
        return  self.state
    
    def get_solution(self):
        # assert self.state == self.STATE_SOLVED_OK,\
               # "solver failed, no solution available"
        # return self.X
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False

