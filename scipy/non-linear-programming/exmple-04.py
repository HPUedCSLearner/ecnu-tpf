# https://www.jianshu.com/p/94817f7cc89b

# 根据自己的理解，自己实现一个简单的非线性规划问题

# Example: 求 minimize(2 / x), (cons: x >= 0.5, x <= 2)
#          Expect: minimize val 0.5, x = 2


from scipy.optimize import minimize
import numpy as np


def func(args):
    a = args
    # return lambda x : a / x
    return lambda x : 1 / (a / x) # (最小值 转 换成 求 最大值)


# (cons: x >= 0.5, x <= 2) == > (x - 0.5 >= 0, 2 - x >= 0)

def cons(args):
    sign, val = args
    return lambda x : sign * x - sign * val


# 设置初始猜测值
x0 = np.asarray(1.5)

#设置限制条件
cons_arg1 = (1, 0.5)
cons_arg2 = (-1, 2)

my_cons = ( {'type': 'ineq', 'fun': cons(cons_arg1)},
            {'type': 'ineq', 'fun': cons(cons_arg2)},
        )

res = minimize(func(2), x0, constraints=my_cons)

print(res.fun)
print(res.success)
print(res.x)