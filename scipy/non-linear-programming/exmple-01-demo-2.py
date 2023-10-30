# https://www.jianshu.com/p/94817f7cc89b

# Example: 计算 1/x+x 的最小值


from scipy.optimize import minimize
import numpy as np

# 目标函数
def fun():
     return lambda x : 1 / x[0] + 1 / x[1]


my_cons = (
            {'type': 'ineq', 'fun': lambda x : x[0] - 200},
            {'type': 'ineq', 'fun': lambda x : -x[0] + 300},
            {'type': 'ineq', 'fun': lambda x : x[1] - 200},
            {'type': 'ineq', 'fun': lambda x : -x[1] + 300},
          )

# 初始猜测值
# x0 = np.asarray((1e-5, 1e-5))  
# x0 = np.asarray((5, 5))  
# x0 = np.asarray((350, 350))  
x0 = np.asarray((250, 250))  

# 非线性规划结果：最值->fun、x的位置->x
# fun: 2.0000000815356342
# x: [ 1.000e+00]
res = minimize(fun(), x0, method='SLSQP', constraints=my_cons)


print('================================')
print('x0:', ' ', x0)
print(res.fun)
print(res.success)
print(res.x)
print('================================')