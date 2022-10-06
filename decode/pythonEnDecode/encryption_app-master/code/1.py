import os
import sys
# import time
f_p= sys.argv[1]
ft = open(f_p,'rb')
fs = open(f_p.replace('.','[x].'),'wb')
size_f=os.path.getsize(f_p)
count_c=0
for i in ft.readlines():
    # time.sleep(0.2)
    # print(i)
    byte_c = b''
    for ix in i:
        xe=ix^0x11
        # print(chr(xe))
        byte_c=byte_c+xe.to_bytes(1,byteorder='big')
        count_c=count_c+1
    fs.write(byte_c)
    print('\r进度:{}%...'.format(int(100*count_c/size_f)),end='')
if count_c!=size_f:
    print("\n{}:{}".format(count_c,size_f))
    input("输入任意键。。。")

ft.close()
fs.close()

# #include <fstream>
# #include <iostream>
# #include <atlstr.h>
# int main(int argc,char*argv[])
# {
#     CString xex(argv[1]);
#     std::ifstream rp;
#     std::ofstream sp;
#     char temp;
#     int f_size=0, f_deal=0,per=0;
#     rp.open(xex, std::ios::in|std::ios::binary);
#     rp.seekg(0, std::ios::end);
#     f_size = rp.tellg();
#     rp.seekg(0);
#     xex.Replace(".", "[x].");
#     sp.open(xex, std::ios::out | std::ios::binary|std::ios::trunc);
#     int count_temp = 0;
#     while (rp.read(&temp, 1))
#     {
#         temp ^= 0x21;
#         sp << temp;
#         f_deal++;
#             per = 100 * (float)f_deal / f_size;
#             if (count_temp < per) {
#                 count_temp = per;
#                 printf("\r进度:%d%%...", per);
#             }
#     }
#     rp.close();
#     sp.close();
# }