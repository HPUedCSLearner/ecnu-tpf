import os
import sys
#密码强度稍微强一点的算法by bilibili:崩析
key = [0x23,0x33,0x66,0x99,0x66] #256*256*256*256*256=1,099,511,627,776bit=128GB 种密码
key_len = len(key)
f_p= sys.argv[1]
ft = open(f_p,'rb')
fs = open(f_p.replace('.','[x].'),'wb')
size_f=os.path.getsize(f_p)
count_c=0
for i in ft.readlines():
    byte_c = b''
    for ix in i:
        xe=ix^key[count_c%key_len]
        byte_c=byte_c+xe.to_bytes(1,byteorder='big')
        count_c=count_c+1
    fs.write(byte_c)
    print('\r进度:{}%...'.format(int(100*count_c/size_f)),end='')
if count_c!=size_f:
    print("\n{}:{}".format(count_c,size_f))
    input("输入任意键。。。")

ft.close()
fs.close()