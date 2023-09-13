# https://www.jianshu.com/p/94817f7cc89b

# Example: 

from scipy.optimize import minimize
import numpy as np

# 目标函数
#   log2(1 + x1 * 2 / 5 + log2(1 + x2 * 6 / 4))
#   con:
#       log2(1 + x1 * 2 / 5) >= 5
#       log2(1 + x2 * 4 / 6) >= 5

def fun(a,b,c,d):
    def v(x):
        # return np.log2(1+x[0]*a/b)+np.log2(1+x[1]*c/d)
        return np.log2(1+x[0]*a/b + np.log2(1+x[1]*c/d))
    return v
    
#限制条件函数
def con(a,b,i):
    def v(x):
        return np.log2(1 + x[i] * a / b)-5
    return v

# 定义常量值
args = [2, 1, 3, 4]  # a,b,c,d
args1 = [2, 5, 6, 4] 

# 设置初始猜测值
x0 = np.asarray((0.5, 0.5))

#设置限制条件
cons = ({'type': 'ineq', 'fun': con(args1[0],args1[1],0)},
        {'type': 'ineq', 'fun': con(args1[2],args1[3],1)},
        )

res = minimize(fun(args[0], args[1], args[2], args[3]), x0, constraints=cons)
print(res.fun)
print(res.success)
print(res.x)