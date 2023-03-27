#!/usr/bin/python

# https://zhuanlan.zhihu.com/p/146762139
# https://blog.csdn.net/Strive_For_Future/article/details/107564274

# 写入Json文件
# with open(save_path,'w') as file:
#   json.dump(data,file)

# 读取Json文件
# with open(file_path,'r') as file:
#   data = json.load(file)

import json
 
def save_json(save_path,data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path,'w') as file:
        json.dump(data,file)
 
def load_json(file_path):
    assert file_path.split('.')[-1] == 'json'
    with open(file_path,'r') as file:
        data = json.load(file)
    return data
 
# 测试
data = {'name':'0.jpg','weight':50,'height':50}
 
# 保存为json文件
save_json("./data.json",data)
# 从json 文件加载数据
data_load = load_json("./config.json")
 
# 打印保存与加载的数据
# print(data)
# print(data_load)


print(data_load['certifications'][0]['name'])