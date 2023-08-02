#!/usr/bin/env python
"""
Optimization algorithm for solving MILP from timing data.
"""

import sys
import copy
import logging
import operator
import importlib
import warnings
import numpy as np
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG) #日志等级为DEBUG

# logger.addHandler(logging.StreamHandler(sys.stderr))


class CESMError(SystemExit, Exception):
    pass

def expect(condition, error_msg, exc_type=CESMError, error_prefix="ERROR:"):
    """
    Similar to assert except doesn't generate an ugly stacktrace. Useful for
    checking user error, not programming error.

    >>> expect(True, "error1")
    >>> expect(False, "error2") # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    CESMError: ERROR: error2
    """
    # Without this line we get a futurewarning on the use of condition below
    warnings.filterwarnings("ignore")
    if not condition:
        if logger.isEnabledFor(logging.DEBUG):
            import pdb
            pdb.set_trace()

        msg = error_prefix + " " + error_msg
        raise exc_type(msg)
        
# try:
    # import pulp
# except ImportError as e:
    # sys.stderr.write("pulp library not installed or located. "
                     # "Try pip install [--user] pulp\n")
    # raise e


def solver_factory(data):
    """
    load data either from a json file or dictionary
    """
    expect('totaltasks' in data,"totaltasks not found in data")

    layout = data['layout']
    # print('WYS Debug:\t', layout)
    sp = layout.rsplit('.', 1) # rsplit 通过字符串分隔，返回一个列表
    print('WYS Debug:sp\t', sp)
    print()
    try:
        if len(sp) > 1:
            print('WYS Debug:sp0,1\t', sp[0], sp[1])
            layout_module = importlib.import_module(sp[0])
            layout = sp[1]
        else:
            import layouts
            layout_module = layouts
    except ImportError:
        expect(False,"cannot import %s\n")

    try:
        solverclass = getattr(layout_module, layout) # getattr(object, name[, default]) 获取object属性为name的值
        print('WYS Debug:solverclass\t', solverclass)
    except KeyError:
        expect(False, "layout class %s not found in %s\n",
               layout, layout_module)

    solver = solverclass()
    
    print('WYS Debug:\tsolver\t', solver)
    print('WYS Debug:\tsolver.get_required_components()\t', solver.get_required_components())
    print()

    for c in solver.get_required_components():
        assert c in data, "ERROR: component %s not found in data" % c

    solver.set_data(data)
    return solver

class   ModelData:
    """
    Convert dictionary data entry into usable object
    """
    def __init__(self, name, model_dict):
        self.name = name
        self.fitparameter = copy.deepcopy(model_dict['fitparameter']) 

class OptimizeModel(object):
    STATE_UNDEFINED = 0
    STATE_UNSOLVED = 1
    STATE_SOLVED_OK = 2
    STATE_SOLVED_BAD = 3
    states = ['Undefined', 'Unsolved', 'Solved', 'No Solution']

    def __init__(self):
        self.models = {}
        self.state = self.STATE_UNDEFINED
        self.X = {}
        self.constraints = []
        self.maxtasks = 0

    def set_data(self, data_dict):
        """
        Add data to the model.
        data_dict is dictionary of components with their data
        example: {'totaltasks':64
                  'ICE': {'ntasks': [2,4,8],
                          'costs':  [10.0,6.0,4.0],
                          'nthrds': [1,1,1],
                          'blocksize': 8}
                  'LND': {...}
                 }

        data is extrapolated as needed for n=1 and n=totaltasks
        sets state to STATE_UNSOLVED
        """
        # get deep copy
        self.maxtasks = data_dict['totaltasks']
        self.mintasks = data_dict['mintasks']
        self.ice_procs = data_dict['ice_procs']
        
        print('WYS Debug:set_data\t', self.maxtasks, '\t', self.mintasks, '\t', self.ice_procs)
        print('WYS Debug:data_dict\t', data_dict)
        print()
    
        # 这部分代码的作用就是 赋值模型（dict） self.models[key]
        # 通过if isinstance(data_dict[key], dict) and 'fitparameter' in data_dict[key]: 取出模型数据
        # 模型的数据就是 一串 字符串
        for key in data_dict:
            # isinstance() 函数来判断一个对象是否是一个已知的类型
            if isinstance(data_dict[key], dict) and 'fitparameter' in data_dict[key]:
                print('WYS Debug:data_dict->key\t', key)
                print('WYS Debug:data_dict[key]\t', data_dict[key])
                print()
                self.models[key] = ModelData(key, data_dict[key]) # 设置模型数据

        print('WYS Debug:self.models\t', self.models)
        print()
        
        self.check_requirements()
        self.state = self.STATE_UNSOLVED
        

    def get_required_components(self):
        """
        Should be overridden by derived class. Return a list of required
        components (capitalized) used in the layout.

        Example: return ['ATM', 'LND', 'ICE']
        """
        return []

    def check_requirements(self):
        """
        Check to make sure that each element of the subclass's list of
        required components has some data provided.
        """
        for r in self.get_required_components():
            if r not in self.models:
                logger.critical("Data for component %s not available", r)

    def write_timings(self, fd=sys.stdout, level=logging.DEBUG):
        """
        Print out the data used for the ntasks/cost models.
        Can be used to check that the data provided to the
        model is reasonable. Also see graph_costs()
        """
        assert self.state != self.STATE_UNDEFINED,\
               "set_data() must be called before write_timings()"
        for k in self.models:
            m = self.models[k]
            message = "***%s***" % k
            if fd is not None:
                fd.write("\n" + message + "\n")
            logger.log(level, message)

            for i in range(len(m.cost)):
                extra = ""
                if m.extrapolated[i]:
                    extra = " (extrapolated)"
                message = "%4d: %f%s" % \
                           (m.ntasks[i], m.cost[i], extra)
                if fd is not None:
                    fd.write(message + "\n")
                logger.log(level, message)

    def optimize(self):
        
        print('WYS Debug:\tcome to optimize')
        print()
        
        """
        Run the optimization.
        Must set self.state using LpStatus object:
              LpStatusOptimal    -> STATE_SOLVED_OK
              LpStatusNotSolved  -> STATE_UNSOLVED
              LpStatusInfeasible -> STATE_SOLVED_BAD
              LpStatusUnbounded  -> STATE_SOLVED_BAD
              LpStatusUndefined  -> STATE_UNDEFINED
              -- use self.set_state(lpstatus) --
        Returns state

        If solved, then solution will be stored in self.X dictionary, indexed
        by variable name. Suggested convention:
        'Tice', 'Tlnd', ... for cost per component
        'Nice', 'Nlnd', ... for ntasks per component
        'NBice', 'NBlnd', ... for number of blocks per component

        The default implementation of get_solution() returns a dictionary
        of these variable keys and their values.
        """
        raise NotImplementedError

    def get_solution(self):
        """
        Return a dictionary of the solution variables, can be overridden.
        Default implementation returns values in self.X
        """
        raise NotImplementedError

    def set_state(self, status):
        if status == True:
            self.state = self.STATE_SOLVED_OK
        else:
            self.state = self.STATE_SOLVED_BAD

    def get_state(self):
        return self.state

    def get_state_string(self, state):
        return self.states[state]

    def write_pe_file(self, pefilename):
        raise NotImplementedError

    def write_xml_changes(self, outfile):
        """
        Write out a list of xmlchange commands to implement
        the optimal layout
        """
        raise NotImplementedError



