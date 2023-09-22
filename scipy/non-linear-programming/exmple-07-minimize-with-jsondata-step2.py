# https://www.jianshu.com/p/94817f7cc89b

# 将 scipy.optimize.minimize 限制为整数值
# https://segmentfault.com/q/1010000043287541

# 根据自己的理解，自己实现一个简单的非线性规划问题

# Example: 将表示离散模型的json数据使用其中
#       step1: 先实现   一个x的非线性求最值
#       step2: 然后实现 多个x的非线性求最值(比如4个)


from scipy.optimize import minimize
import numpy as np
import json
import math

module_frmwrk_file = 'trans_fit_parameters.json'

# 读取json文件
def wys_get_fitfitparameter(file_name):
    fitparameter_file = open(file_name, "r")
    data = json.load(fitparameter_file)
    return data

# json 转 list
def get_list_form_josn(data):
    list_data = []
    for item in data:
        # list_data.append(item)
        list_data.append(data[item])
    list_res = [999] + list_data
    return list_res

# def get_list_form_josn(data):
#     list_data = []
#     for key,val in data:     // not OK
#         # list_data.append(item)
#         list_data.append(val)
#     return list_data
    


# 测试代码
modle_data = wys_get_fitfitparameter(module_frmwrk_file)
print(modle_data['atm']['3'])

list_data = get_list_form_josn(modle_data['atm'])
print(list_data[0:10])
print(list_data[-10:])
print(list_data[1])
print(list_data[-1])
print(len(list_data))

# 求模型区间最值[200， 300]

def func(args): # 接受 模型list
    model_list = args
    # return lambda x : model_list[math.ceil(x)]
    return lambda x : model_list[math.floor(x)]

#   File "/home/tmpDevDir/ecnu-tpf/scipy/non-linear-programming/exmple-06-jsondata-step1.py", line 55, in <lambda>
#     return lambda x : model_list[x]
# TypeError: only integer scalar arrays can be converted to a scalar index


# def func(args):
#     a = args
#     return lambda x : a / x[0] + x[1]


# # (cons: x >= 200, x <= 300) == > (x - 200 >= 0, 300 - x >= 0)

def cons(args):
    sign, val = args
    return lambda x : sign * x - sign * val


# # 设置初始猜测值
# x = np.asarray((1.5, 0.5))

# 结果 和 这个初始值有关 （200， 300）
# x = np.asarray(150)
# x = np.asarray(250)
x = np.asarray(250)

# #设置限制条件
# cons_arg1 = (1, 0.5)
# cons_arg2 = (-1, 2)

cons_arg1 = (1, 200)
cons_arg2 = (-1, 300)

# # ineq >=, eq ==
# my_cons = ( {'type': 'ineq', 'fun': cons(cons_arg1)},
#             {'type': 'ineq', 'fun': cons(cons_arg2)},
#             {'type': 'eq', 'fun': lambda x : x[0] - x[1] - 1},      # x1 - x2 = 1
#             {'type': 'eq', 'fun': lambda x : x[1] - x[0] - 1}       # x2 - x1 = 1 (上面两个约束条件，表示两个x之间的距离相差1)
#         )

# ineq >=, eq ==
my_cons = ( #{'type': 'ineq', 'fun': cons(cons_arg1)},
            #{'type': 'ineq', 'fun': cons(cons_arg2)},
            {'type': 'ineq', 'fun': lambda x : x[0] - 200},
            {'type': 'ineq', 'fun': lambda x : -x[0] + 300},
            # {'type':'eq','fun': lambda x : max([x[i]-int(x[i]) for i in range(len(x))])} 
            {'type': 'eq', 'fun': lambda x : math.ceil(x) - x},
            {'type': 'eq', 'fun': lambda x : math.floor(x) - x}
        )

# res = minimize(func(2), x, constraints=my_cons)
# # res = minimize(func(2), x, method='SLSQP', constraints=my_cons)

aim_model = get_list_form_josn(modle_data['atm'])

res = minimize(func(aim_model), x, method='SLSQP', constraints=my_cons)


print('================================')
print(res.fun)
print(res.success)
print(res.x)
print(math.floor(res.x)) # 前面运算向上取整，后面去结果向下取整
print('================================')

# print(aim_model[res.x])
#     print(aim_model[res.x])
# TypeError: only integer scalar arrays can be converted to a scalar index
# print(math.floor(res.x))
# print(aim_model[math.floor(res.x)])
# print(aim_model[300])