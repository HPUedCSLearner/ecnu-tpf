import os
import sys
f_p = sys.argv[1]
ft = open(f_p,'rb')
fs = open(f_p.replace('.','_bk.'),'wb')
size_f = os.path.getsize(f_p)
count_c = 0
for i in ft.readlines():
    for ix in i:
        count_c += 1
        ix = ix ^ 0x11
        fs.write(ix.to_bytes(1,byteorder='big'))
        print('\r进度:{}%...'.format(int(100*count_c/size_f)),end='')
print('\n')
ft.close()
fs.close()