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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2,), (1, 3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1]', 'x[0] + x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': natm+nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3), (1, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1] + x[2]', 'x[0] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': natm}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2, 3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0]', 'x[1] + x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (1, 3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1]', 'x[0] + x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2,), (3,), (4,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0]', 'x[1]', 'x[2]', 'x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 2), (4, 1, 3)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[2])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[3] + x[1]', 'x[3] + x[0] + x[2]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nice, 'ocn': nice, 'lnd': nice+natm, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1]', 'x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1] + x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3), (1,), (4,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1] + x[2]', 'x[0]', 'x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 4, 3), (1, 4, 2)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[1])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[3] + x[2]', 'x[0] + x[3] + x[1]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm+nice, 'lnd': natm+nice, 'ice': natm}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2, 4), (3,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0]', 'x[1] + x[3]', 'x[2]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nocn}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1,), (2,), (3, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0]', 'x[1]', 'x[2] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 2, 3), (4, 1)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[3] + x[1] + x[2]', 'x[3] + x[0]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nice, 'ocn': nice, 'lnd': nice+nocn, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (1, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1] + x[2]', 'x[0] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 3, 4), (2, 1)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[0])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1] + x[2] + x[3]', 'x[1] + x[0]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nocn, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 3), (1, 2, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[2]', 'x[0] + x[1] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nocn}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (1, 2, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1] + x[2]', 'x[0] + x[1] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2, 4), (1, 3)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1] + x[3]', 'x[0] + x[2]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': nocn}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3, 4), (3, 1, 2)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[0] + x[1])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[2] + x[3]', 'x[2] + x[0] + x[1]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nlnd, 'ocn': nlnd+natm, 'lnd': 0, 'ice': nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3,), (1, 2, 4)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[2]', 'x[0] + x[1] + x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': natm+nocn}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(3, 4, 1), (3, 4, 2)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[1])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[2] + x[3] + x[0]', 'x[2] + x[3] + x[1]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nlnd+nice, 'ocn': nlnd+nice, 'lnd': 0, 'ice': nlnd}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2), (3,), (4,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1]', 'x[2]', 'x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(2,), (1, 3), (4,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[1]', 'x[0] + x[2]', 'x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(1, 2, 3), (4,)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[0] + x[1] + x[2]', 'x[3]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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
        """
        Run the optimization.
        set solution1 in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        
        pattern = [(4, 1, 2), (4, 3)]
        
        mintime = 836.0052561228435
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #wys
        print('wys tmp_strlist:', tmp_strlist)
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        if flag2 == 1:
            tmp_str = "max("  +module_fit("x[2]",self.models['lnd'.upper()].fitparameter) + ' , ' + module_fit("x[3]",self.models['ice'.upper()].fitparameter) + ")"
            tmp_strlist.append(tmp_str)
        else:
            tmp_strlist.append(module_fit("x[2]",self.models['lnd'.upper()].fitparameter))
            tmp_strlist.append(module_fit("x[3]",self.models['ice'.upper()].fitparameter))
            #yeeland
        eval_str = '+'.join(tmp_strlist)#规划主函数
        
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[2])})

        
        constraints.append({'type': 'ineq', 'fun' : lambda x : mintime* (1+allowance) -  (eval(eval_str)) })
        
        X_range = ['x[3] + x[0] + x[1]', 'x[3] + x[2]']
        if len(X_range) > 1 :
            max_x = 'max(' + ','.join(X_range) + ')'
        else:
            max_x = X_range[0]
        cost_func = lambda x : (eval(eval_str)) * eval(max_x)
        
        x0 = [self.mintasks]*4
        
        #机时最少方案
        solution = minimize(cost_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if solution.success:
            self.X = {}
            ntasks = solution.x
            for i in range(len(ntasks)):
                ntasks[i] = int(ntasks[i])
            self.X['mincost'] = cost_func(ntasks)
            natm = int(ntasks[0])
            nocn = int(ntasks[1])
            nlnd = int(ntasks[2])
            nice = int(ntasks[3])
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
            # print(solution1.success)
            roots = {'cpl':0 , 'atm': nice, 'ocn': nice+natm, 'lnd': nice, 'ice': 0}
            self.X['ntasks']  = ntasks
            self.X['roots'] = roots
        
        
        self.solution = {}
        if solution.success:
            self.solution['mincost'] = self.X
        
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

