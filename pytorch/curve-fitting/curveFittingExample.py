#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed

batch_size = 10000
input_size = 1
output_size = 1
num_epochs = 2000
learning_rate = 0.1

x = torch.linspace(0, 1, batch_size).reshape(-1, 1)
y = x ** 2 + 1

print('x.shape:', x.shape)
print('y.shape:', y.shape)

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
    y_pred = model.forward(x)
    print('x.shape: ', x.shape, ' y_pred.shape: ', y_pred.shape)
    loss = loss_func(y_pred, y)
    optimizer.zero_grad()

    loss.backward()
    optimizer.step()
    if i % 100 == 0:
        print(f"epoch: {i}, loss: {loss}")

plt.plot(x.data, y.data, "g*")
plt.plot(x.data, model.forward(x).data, "r-")
plt.show()

