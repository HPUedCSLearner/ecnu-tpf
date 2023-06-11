import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable as var

def get_data(x,w,b,d):
    c,r = x.shape
    y = (w * x * x + b*x + d)+ (0.1*(2*np.random.rand(c,r)-1))
    return(y)

xs = np.arange(0,3,0.01).reshape(-1,1)
ys = get_data(xs,1,-2,3)

xs = var(torch.Tensor(xs))
ys = var(torch.Tensor(ys))

print('xs.shape: ', xs.shape)
print('xs.type: ', xs.type)
print('xs: ', xs)

x = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
y = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
# y = torch.tensor([26208396035170., 14125095233571, 9499624724564, 7332661699610, 4969123787708, 3922271353408, 2678558663290, 
#                         2128286801327, 1447494492105, 1119992491206,  815502882802, 788519722917,  495173769367, 408134497783])


# print('in_x.shape: ', in_x.shape)
# print('in_x.reshape(-1, 1).shape: ', in_x.reshape(-1, 1).shape)
y = y * 2
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)


plt.title("curve")
plt.plot(xs.data.numpy(),ys.data.numpy())
plt.legend("ys","ys_pre")
plt.show()



class Fit_model(torch.nn.Module):
    def __init__(self):
        super(Fit_model,self).__init__()
        self.linear1 = torch.nn.Linear(1,8)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(8,1)

        self.criterion = torch.nn.MSELoss()
        self.opt = torch.optim.SGD(self.parameters(),lr=0.1)
    def forward(self, input):
        y = self.linear1(input)
        y = self.relu(y)
        y = self.linear2(y)
        return y



model = Fit_model()
for e in range(80000):
    y_pre = model(x)

    loss = model.criterion(y_pre,y)
    if(e%10000==0):
        print(e,loss.data)
    
    # Zero gradients
    model.opt.zero_grad()
    # perform backward pass
    loss.backward()
    # update weights
    model.opt.step()


y_pre = model(x)
print(x)
print(y)
print(y_pre)

plt.title("curve")
plt.scatter(x.data.numpy(),y.data.numpy())
plt.plot(x.data.numpy(),y_pre.data.numpy())
plt.plot(x.data.numpy(),y_pre.data.numpy())
plt.legend("ys","ys_pre")
plt.show()
