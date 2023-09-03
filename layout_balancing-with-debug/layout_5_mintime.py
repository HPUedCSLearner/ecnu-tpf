# -*- coding: UTF-8 -*-
import optimize_model
from scipy.optimize import minimize
import numpy as np

def sig(x,down,up):
    if x >= down and x < up :
        return 1
    else:
        return 0

def module_fit(xi, fitparameter):
    result = []
    for i in fitparameter:
        tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + {6}*{x}**0.5*np.log({x}) + {7}*{x}*np.log({x}) + {8}*{x}**2*np.log({x}) + {9}*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        result.append(tmp_str)
    return '+'.join(result)

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
class atmocnlndicecpl0(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 5), (2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd, 'cpl': natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl1(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3, 2, 5), (3, 1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[1] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[0] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nlnd, 'ocn': nlnd, 'lnd': 0, 'ice': nlnd+natm, 'cpl': nlnd+nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl2(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3, 4, 5), (2,), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nlnd, 'cpl': nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl3(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3, 5), (1,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': 0, 'cpl': nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl4(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (3,), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': natm+nocn, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl5(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3, 4, 5), (3, 1, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[0] + x[1])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nlnd, 'ocn': nlnd+natm, 'lnd': 0, 'ice': nlnd, 'cpl': nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl6(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 3), (1, 2, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nocn, 'cpl': natm+nocn+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl7(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 4), (1,), (3, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nocn, 'cpl': nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl8(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 2), (5, 1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl, 'lnd': ncpl+natm, 'ice': ncpl+natm+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl9(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 4), (3, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': natm+nocn, 'cpl': nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl10(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 2, 4), (5, 1, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl, 'lnd': ncpl+natm, 'ice': ncpl+nocn, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl11(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (1, 2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl12(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd, 'cpl': natm+nocn+nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl13(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2,), (3, 5), (1,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 0, 'cpl': nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl14(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (2, 3), (1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': natm, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl15(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (1,), (2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl16(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 4, 5, 3), (1, 4, 5, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[4] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[4] + x[1])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm+nice+ncpl, 'lnd': natm+nice+ncpl, 'ice': natm, 'cpl': natm+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl17(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 5), (1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nlnd, 'cpl': natm+nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl18(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 5), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn, 'cpl': natm+nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl19(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 5), (1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm, 'cpl': natm+nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl20(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 1, 5), (4, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nice, 'ocn': nice, 'lnd': nice+nocn, 'ice': 0, 'cpl': nice+natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl21(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (5,), (3,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': 0, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl22(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (1, 3, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nlnd, 'cpl': natm+nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl23(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 3, 5), (1, 2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm, 'ice': natm+nocn, 'cpl': natm+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl24(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3, 4), (2, 1, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[0] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nocn, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd, 'cpl': nocn+natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl25(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 3, 5), (2,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': 0, 'cpl': natm+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl26(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 5, 4), (1, 5, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm+ncpl, 'lnd': natm+ncpl+nocn, 'ice': natm+ncpl, 'cpl': natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl27(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (3, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': nlnd, 'cpl': nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl28(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 5, 4), (1, 2, 5, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[4] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[4] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn+ncpl, 'ice': natm+nocn+ncpl, 'cpl': natm+nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl29(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5, 1), (4, 5, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nice+ncpl, 'ocn': nice+ncpl, 'lnd': nice+ncpl+nocn, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl30(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3, 4, 5), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd, 'cpl': nocn+nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl31(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 1, 2, 4), (5, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[1] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl+natm, 'lnd': ncpl, 'ice': ncpl+natm+nocn, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl32(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3), (1, 2, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn, 'cpl': natm+nocn+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl33(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5), (2,), (3,), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl34(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 5), (3, 4), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nlnd, 'cpl': nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl35(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (1,), (2,), (3,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 0, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl36(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 3), (2, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': nocn, 'cpl': nocn+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl37(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (2, 3), (1,), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': 0, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl38(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4,), (5,), (1, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': 0, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl39(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2,), (5,), (3, 4), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl40(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 5), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': 0, 'cpl': natm+nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl41(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5,), (1, 3), (2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': nocn, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl42(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5, 1, 3), (4, 5, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[1])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nice+ncpl, 'ocn': nice+ncpl, 'lnd': nice+ncpl+natm, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl43(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 5, 2), (1, 5, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm+ncpl, 'lnd': natm+ncpl, 'ice': natm+ncpl+nlnd, 'cpl': natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl44(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 5), (3,), (2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nocn, 'cpl': natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl45(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 5), (1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': natm+nlnd, 'cpl': nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl46(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (4,), (3, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': 0, 'cpl': nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl47(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 2, 3, 4), (5, 1)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[1] + x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl, 'lnd': ncpl+nocn, 'ice': ncpl+nocn+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl48(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 1, 4), (5, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl, 'lnd': ncpl+nocn, 'ice': ncpl+natm, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl49(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1,), (3,), (2, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': nocn, 'cpl': nocn+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl50(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2,), (5,), (1, 3), (4,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': 0, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl51(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 3, 5), (2, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': nocn, 'cpl': natm+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl52(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5), (2, 3), (1,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl53(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (5,), (3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl54(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5), (1, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl55(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 5), (1, 2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd, 'cpl': natm}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl56(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3, 5), (1, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': natm, 'cpl': nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl57(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3, 4, 5), (2, 1)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[2] + x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1] + x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nocn, 'ocn': 0, 'lnd': nocn, 'ice': nocn+nlnd, 'cpl': nocn+nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl58(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3), (1, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm, 'cpl': natm+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl59(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5, 1, 2), (4, 5, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[0] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nice+ncpl, 'ocn': nice+ncpl+natm, 'lnd': nice+ncpl, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl60(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2,), (5,), (1, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': natm+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl61(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 3, 4), (5, 1, 2)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[2] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[1])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl+natm, 'lnd': ncpl, 'ice': ncpl+nlnd, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl62(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 4), (1, 2, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd, 'cpl': natm+nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl63(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3, 4, 5, 2), (3, 4, 5, 1)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[4] + x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2] + x[3] + x[4] + x[0])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nlnd+nice+ncpl, 'ocn': nlnd+nice+ncpl, 'lnd': 0, 'ice': nlnd, 'cpl': nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl64(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2, 3, 5), (1, 2, 3, 4)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[2] + x[3])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': natm+nocn, 'ice': natm+nocn+nlnd, 'cpl': natm+nocn+nlnd}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl65(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5), (4, 1, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[0] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': nice, 'ocn': nice+natm, 'lnd': nice+natm+nocn, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl66(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2, 3), (1, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': nocn, 'ice': natm, 'cpl': natm+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl67(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(2,), (1, 3, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': natm+nlnd, 'cpl': natm+nlnd+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl68(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3,), (1, 2, 4, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[3] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': natm+nocn, 'cpl': natm+nocn+nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl69(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(4, 5), (2,), (1, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[1])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': 0, 'lnd': natm, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl70(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(3, 4), (1, 2, 5)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[0] + x[1] + x[4])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': nlnd, 'cpl': natm+nocn}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl71(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(1, 2), (4, 5), (3,)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
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
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[3] + x[4])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': 0, 'ocn': natm, 'lnd': 0, 'ice': 0, 'cpl': nice}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False


class atmocnlndicecpl72(optimize_model.OptimizeModel):
    
    def get_required_components(self):
        return ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
            
    def optimize(self):
        """
        Run the optimization.
        set solution in self.X
        set state STATE_SOLVED_OK if solved,
        otherwise STATE_SOLVED_BAD
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before optimize()!"
        

        pattern = [(5, 4), (5, 1, 2, 3)]
        
        strlist = []
        tmp_pattern=pattern.copy()
        for i in range(len(tmp_pattern)):
            tmp_pattern[i] = list(tmp_pattern[i])
        
        tmp_strlist = []
        #atm
        tmp_strlist.append(module_fit("x[0]",self.models['atm'.upper()].fitparameter))
        #ocn
        tmp_strlist.append(module_fit("x[1]",self.models['ocn'.upper()].fitparameter))
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
        tmp_strlist.append(module_fit("x[4]",self.models['cpl'.upper()].fitparameter))
        
        eval_str = '+'.join(tmp_strlist)#规划主函数
        tmp_models = ['atm'.upper(),'ocn'.upper(), 'lnd'.upper(),'ice'.upper(), 'cpl'.upper()]
        bnds = []
        for tmp_model in tmp_models:
            if tmp_model== 'LND' and self.maxtasks > 128:
                bnd =  (self.mintasks, 128)
            else:
                bnd = (self.mintasks, self.maxtasks)
            bnds.append(bnd)
        bnds = tuple(bnds)
        constraints = []
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[3])})
        constraints.append({'type': 'ineq', 'fun': lambda x : self.maxtasks - (x[4] + x[0] + x[1] + x[2])})

        
        time_func = lambda x: eval(eval_str)
        
        x0 = [self.mintasks]*5
        
        ##运行时间最少方案
        solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        if not solution1.success:
            for constraint in constraints:
                constraint['type'] = 'eq'
            solution1 = minimize(time_func, x0, method = 'SLSQP', bounds = bnds, constraints = constraints)
        
        self.X = {}
        ntasks1 = solution1.x
        for i in range(len(ntasks1)):
            ntasks1[i] = round(ntasks1[i])
        self.X['Totaltime'] = time_func(ntasks1)
        natm = int(ntasks[0])
        nocn = int(ntasks[1])
        nlnd = int(ntasks[2])
        nice = int(ntasks[3])
        ncpl = int(ntasks[4])
        self.X['submoduletime'] = {}
        self.X['submoduletime']['atm']  = eval(module_fit(str(natm),self.models['atm'.upper()].fitparameter))
        self.X['submoduletime']['ocn']  = eval(module_fit(str(nocn),self.models['ocn'.upper()].fitparameter))
        self.X['submoduletime']['lnd']  = eval(module_fit(str(nlnd),self.models['lnd'.upper()].fitparameter))
        self.X['submoduletime']['ice']  = eval(module_fit(str(nice),self.models['ice'.upper()].fitparameter))
        self.X['submoduletime']['cpl']  = eval(module_fit(str(nice),self.models['cpl'.upper()].fitparameter))
        self.X['maxtasks'] = self.maxtasks
        self.X['pattern'] = str(pattern)
        ntasks1 = {'atm':natm,'ocn':nocn,'lnd':nlnd,'ice':nice, 'cpl':ncpl}
        ice_procs = self.ice_procs
        if 'ice' in ntasks1:
        #检查ice进程是否合乎规范
            ice_proc_pre = ntasks1['ice']
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
        roots1 = {'cpl':0 , 'atm': ncpl, 'ocn': ncpl+natm, 'lnd': ncpl+natm+nocn, 'ice': ncpl, 'cpl': 0}
        self.X['ntasks']  = ntasks1
        self.X['roots'] = roots1
        
        
        self.solution = {}
        if solution1.success:
            self.solution['mintime'] = self.X

        
        self.set_state(solution1.success)
        # print(self.state)
        return  self.state
    
    def get_solution(self):
        if self.state == self.STATE_SOLVED_OK:
            return self.solution
        else:
            return False

