import pandas as pd


print(pd.__version__)  # 查看版本

data = pd.read_csv('data.csv')
# print(data.to_string())


# pandas 遍历  https://www.jianshu.com/p/6c3802f8172f
df_data = pd.DataFrame(data)
# print(df_data)


for index, row in df_data.iterrows():
    print(index) # 输出每行的索引值
    if index == 0:
        print(row)
        
# 对于每一行，通过列名name访问对应的元素
for index, row in df_data.iterrows():
    if index == 0:
        print(row['func'], row['facter_func']) # 输出每一行
        
        
# pandas 分组操作
group = df_data.groupby('times')
print(group)
print(list(group))