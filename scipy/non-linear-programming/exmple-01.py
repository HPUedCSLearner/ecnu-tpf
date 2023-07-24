# https://www.jianshu.com/p/94817f7cc89b

# Example: 计算 1/x+x 的最小值


from scipy.optimize import minimize
import numpy as np

# 目标函数
def fun(args):
     a=args
     v=lambda x:a/x[0] +x[0]
     return v

args = (1)  #a

# 初始猜测值
x0 = np.asarray((2))  
res = minimize(fun(args), x0, method='SLSQP')

print(res)
print(res.fun)
print(res.success)
