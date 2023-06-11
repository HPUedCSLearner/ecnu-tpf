#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed



x = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
# y = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
y = torch.tensor([26208396035170., 14125095233571, 9499624724564, 7332661699610, 4969123787708, 3922271353408, 2678558663290, 
                        2128286801327, 1447494492105, 1119992491206,  815502882802, 788519722917,  495173769367, 408134497783])


# print('in_x.shape: ', in_x.shape)
# print('in_x.reshape(-1, 1).shape: ', in_x.reshape(-1, 1).shape)
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
print('x:\n', x)
print('x.type:\n', x.type)
print('y:\n', y)

plt.plot(x, y, "y-")
plt.scatter(x, y, c='black')
plt.show()


# batch_size = 10
# input_size = 1
# output_size = 1
num_epochs = 5000
learning_rate = 0.01

# # x = torch.linspace(0, 1, batch_size).reshape(-1, 1)
# # print(x)
# # y = x ** 2 + 1
# # print(y)

model = nn.Sequential(
    nn.Linear(1, 1),
    nn.Sigmoid(),
    nn.Linear(1, 1),
    nn.Sigmoid(),
    nn.Linear(1, 1),
    nn.Sigmoid(),
    nn.Linear(1, 1),
    nn.Sigmoid(),
    nn.Linear(1, 1)
)

loss_func = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for i in range(num_epochs):
    # print('x:', x)
    # print('x.shape: ', x.shape)
    y_pred = model.forward(x)
    loss = loss_func(y_pred, y)
    optimizer.zero_grad()

    loss.backward()
    optimizer.step()
    if i % 100 == 0:
        print(f"epoch: {i}, loss: {loss}")

plt.plot(x.data, y.data, "g*")
plt.plot(x.data, model.forward(x).data, "r-")
# plt.plot(x, y, "g*")
# plt.plot(x, model.forward(x).data, "r-")
plt.show()
