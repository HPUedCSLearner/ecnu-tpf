# https://www.jianshu.com/p/94817f7cc89b

# 根据自己的理解，自己实现一个简单的非线性规划问题

# Example: 求 minimize(2 / x + x), (cons: x >= 0.5, x <= 2)
#          Expect: minimize val 1.5, x1 = 2, x2 = 0.5


from scipy.optimize import minimize
import numpy as np


def func(args):
    a = args
    return lambda x : a / x[0] + x[1]


# (cons: x >= 0.5, x <= 2) == > (x - 0.5 >= 0, 2 - x >= 0)

def cons(args):
    sign, val = args
    return lambda x : sign * x - sign * val


# 设置初始猜测值
x = np.asarray((1.5, 0.5))

#设置限制条件
cons_arg1 = (1, 0.5)
cons_arg2 = (-1, 2)

# ineq >=, eq ==
my_cons = ( {'type': 'ineq', 'fun': cons(cons_arg1)},
            {'type': 'ineq', 'fun': cons(cons_arg2)},
            {'type': 'eq', 'fun': lambda x : x[0] - x[1] - 1},      # x1 - x2 = 1
            {'type': 'eq', 'fun': lambda x : x[1] - x[0] - 1}       # x2 - x1 = 1 (上面两个约束条件，表示两个x之间的距离相差1)
        )

res = minimize(func(2), x, constraints=my_cons)
# res = minimize(func(2), x, method='SLSQP', constraints=my_cons)

print(res.fun)
print(res.success)
print(res.x)