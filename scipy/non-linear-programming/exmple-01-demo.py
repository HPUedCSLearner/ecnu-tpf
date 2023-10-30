# https://www.jianshu.com/p/94817f7cc89b

# Example: 计算 1/x+x 的最小值


from scipy.optimize import minimize
import numpy as np

# 目标函数
# def fun():
#      # return lambda x : 1 / x[0]
#      # return lambda x : 1 / (x + 1)
#      # return lambda x : (x+1)**(-1)
#      # return lambda x : x
#      # return lambda x :  x[0]
#      return lambda x :  -np.log(x)
#      # return lambda x :  x ** (-2)

def fun():
     return lambda x : -np.log(x).astype(np.float64)




my_cons = (
            {'type': 'ineq', 'fun': lambda x : x - 200},
            {'type': 'ineq', 'fun': lambda x : -x + 300},
          )

my_bnds = [[200, 300]]
# my_bnds = [200, 300]

# 初始猜测值
# x0 = np.asarray(250)  
# x0 = np.asarray(1)  
# x0 = np.asarray(350)  
# x0 = np.asarray(1e5)  
x0 = np.asarray(1e-5)  

# 非线性规划结果：最值->fun、x的位置->x
# fun: 2.0000000815356342
# x: [ 1.000e+00]
# res = minimize(fun(), x0, method='TNC', constraints=my_cons)    # not ok
# res = minimize(fun(), x0, method='SLSQP', constraints=my_cons)  # ok
# res = minimize(fun(), x0, method='dogleg', constraints=my_cons)   # not ok
res = minimize(fun(), x0, method='SLSQP', bounds = my_bnds)   # ok
# res = minimize(fun(), x0, method='TNC', bounds = my_bnds)
# res = minimize(fun(), x0, method='dogleg', bounds = my_bnds)


print('================================')
print(res.fun)
print(np.exp(res.fun))
print(1 / res.x)
print(res.success)
print(res.x)
print('================================')

# y = 1 / x
# log y = -log x
# y = 10 epx (log y)
# y = 10 epx (-logx)


x = np.log(np.e)
print(x)



y = fun()
print(y(200))
print(y(200.0001))
print(y(200.001))
print(y(200.1))
print(y(201))
print(type(y(201)))