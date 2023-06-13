import time

def task():
    out = 1
    for i in range(1,100000000):
        out = out + i
    return out

startTime = time.time()
out = task()
endTime = time.time()
print(f"1到1亿相加结果：{out}")
print(f"执行task()函数用时：{endTime - startTime}")
