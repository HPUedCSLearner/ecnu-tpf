import numpy as np 
from matplotlib import pyplot as plt 
 
x = np.linspace(0, 10, 50) 
y =  1/x + x
y1 = 1/x
y2 = x
plt.title("Matplotlib demo") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 
plt.plot(x,y) 
# plt.plot(x,y1) 
# plt.plot(x,y2) 
plt.show()