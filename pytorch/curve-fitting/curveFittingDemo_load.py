#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed

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


# 测试一个数据
# x = torch.tensor([300])
x = torch.tensor([300.])
x = x.reshape(-1, 1)
print(net.forward(x).data)
print(de_normalization(net.forward(x).data, min_y, max_y))
print('===============================================')

# 保存模型
# print('======================Test Save Model=========================')
# # print(model.state_dict())
# torch.save(model.state_dict(), 'model.pt')


#=#=#==#=#==#=#==#=#=对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致=#=#==#=#==#=#==#=#==#=#==#=#=
# 加载模型 
net.load_state_dict(torch.load('model.pt'))

# # 使用模型
print('======================Test Use Model=========================')
print(net.forward(x).data)
# print(new_net.forward(x).data) # error: -> '_IncompatibleKeys' object has no attribute 'forward'