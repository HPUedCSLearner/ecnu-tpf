import numpy as np
from scipy.optimize import curve_fit

x = np.asarray(range(20,401,20))
print(x)
y = np.random.rand(20)
print(y)
# params = np.array([1,1])
a = 1
b = 1

def funcinv(x, a, b):
    return b + a/x

res = curve_fit(funcinv, x, y, (a, b))
print(res)  #  ... array([ 6.89518618,  0.37118815]), ...
print(a)
print(b)