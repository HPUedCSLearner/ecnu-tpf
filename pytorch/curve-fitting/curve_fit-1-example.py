import numpy as np
import matplotlib.pyplot as plt
import torch as t
from torch.autograd import Variable as var


def get_data(x,w,b,d):
    c,r = x.shape
    y = (w * x * x + b*x + d)+ (0.1*(2*np.random.rand(c,r)-1))
    return(y)

xs = np.arange(0, 1, 0.1).reshape(-1,1)
ys = get_data(xs,1,-2,3)
ys = xs

xs = var(t.Tensor(xs))
ys = var(t.Tensor(ys))

# x = t.tensor([8, 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
# y = t.tensor([8, 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
# xs = var(x)
# ys = var(y)

# x = np.array([8, 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024]).reshape(-1, 1)
# y = np.array([8, 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024]).reshape(-1, 1)
# xs = var(t.Tensor(x))
# ys = var(t.Tensor(y))

class Fit_model(t.nn.Module):
    def __init__(self):
        super(Fit_model,self).__init__()
        self.linear1 = t.nn.Linear(1,16)
        self.relu = t.nn.ReLU()
        self.linear2 = t.nn.Linear(16,1)

        self.criterion = t.nn.MSELoss()
        self.opt = t.optim.SGD(self.parameters(),lr=0.0005)
    def forward(self, input):
        y = self.linear1(input)
        y = self.relu(y)
        y = self.linear2(y)
        return y
        
model = Fit_model()
for e in range(8001):
    y_pre = model(xs)

    loss = model.criterion(y_pre,ys)
    if(e%2000==0):
        print(e,loss.data)
    
    # Zero gradients
    model.opt.zero_grad()
    # perform backward pass
    loss.backward()
    # update weights
    model.opt.step()

ys_pre = model(xs)

plt.title("curve")
plt.scatter(xs.data.numpy(),ys.data.numpy())
plt.plot(xs.data.numpy(),ys.data.numpy())
plt.plot(xs.data.numpy(),ys_pre.data.numpy())
plt.legend("ys","ys_pre")
plt.show()

# 作者：小宋是呢
# 链接：https://juejin.cn/post/7000404151809081351
# 来源：稀土掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。