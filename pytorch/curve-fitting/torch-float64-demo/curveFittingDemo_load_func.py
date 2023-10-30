#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed

torch.set_default_dtype(torch.float64)


def normalization(y):
    min_y = torch.min(y)
    max_y = torch.max(y)
    return min_y, max_y, (y - min_y) / (max_y - min_y)

def de_normalization(y, min_y, max_y):
    return (max_y - min_y) * y + min_y
    
################################################################
#                                                              #
# 对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致   #
#                                                              #
################################################################


# ==============这个在使用模型的时候，不是必要的=====================
# num_epochs = 500
# learning_rate = 0.01


# ==============这个在使用模型的时候，这个必须对应上保存的模型数据=====================
net = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

# ==============这个在使用模型的时候，不是必要的=====================
# loss_func = torch.nn.MSELoss()
# optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)


#=#=#==#=#==#=#==#=#=对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致=#=#==#=#==#=#==#=#==#=#==#=#=
# 加载模型 
net.load_state_dict(torch.load('model.pt'))

# 测试一个数据
# x = torch.tensor([300])
# x = torch.tensor([300.])
# x = x.reshape(-1, 1)
# print(net.forward(x).data)
# print('===============================================')

# 保存模型
# print('======================Test Save Model=========================')
# # print(model.state_dict())
# torch.save(model.state_dict(), 'model.pt')


# #=#=#==#=#==#=#==#=#=对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致=#=#==#=#==#=#==#=#==#=#==#=#=
# # 加载模型 
# net.load_state_dict(torch.load('model.pt'))

# # 使用模型
# print('======================Test Use Model=========================')
# print(net.forward(x).data) # tensor([[0.0259]])
# # print(new_net.forward(x).data) # error: -> '_IncompatibleKeys' object has no attribute 'forward'

def getNetVal(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net.forward(ten).data
    res = res.reshape(-1)
    print("In getNetVal: ", x, res.numpy()[0] * 10000)
    return res.numpy()[0] * 10000

# def func(net):
#     y = lambda x : getNetVal(x, net)
#     print("in func:", x, y(x))
#     return y
    # return lambda x : getNetVal(x, net)
    # return lambda x : -np.log(getNetVal(x, net))



# print('======================Test Use func=========================')
# print(getNetVal(200, net))
# print(getNetVal(200.0001, net))
# print(getNetVal(200.001, net))
# print(getNetVal(200.01, net))
# print(getNetVal(200.1, net))
# print(getNetVal(201, net))
# print(getNetVal(250, net))
# print(getNetVal(400, net))
# print(getNetVal(500, net))
# print(getNetVal(600, net))
# print(getNetVal(700, net))
# print(getNetVal(800, net))

# print('======================Test Use myfunc=========================')
# myfunc = func(net)
# print(myfunc(200))
# print(myfunc(250))
# print(myfunc(300))
# print()
# print(myfunc(250.1))
# print(myfunc(250.01))
# print(myfunc(250.001))

print('======================Test Use minimize with Net=========================')
from scipy.optimize import minimize
import numpy as np





# (cons: x >= 0.5, x <= 2) == > (x - 0.5 >= 0, 2 - x >= 0)

def cons(args):
    sign, val = args
    return lambda x : sign * x - sign * val


# 设置初始猜测值
# x0 = np.asarray(1.5)
# x0 = np.asarray(0.2)
# x0 = np.asarray(100)
x0 = np.asarray(400)
# x0 = np.asarray(250)

#设置限制条件
cons_arg1 = (1, 200)
cons_arg2 = (-1, 300)



my_bnds = [[200, 300]]

my_cons = ( {'type': 'ineq', 'fun': cons(cons_arg1)},
            {'type': 'ineq', 'fun': cons(cons_arg2)},
        )

# res = minimize(func(net), x0, method='SLSQP', constraints=my_cons)
res = minimize(getNetVal, x0, method='SLSQP', bounds=my_bnds)

print(res.fun)
print(res.success)
print(res.x)