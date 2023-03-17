**1、首先，我们的利用objdump导出符号**表

objdump -d cesm.exe > cesm.exe.signalTable.txt

**2、然后，我们过滤出符号表中地址和函数名的内容**

grep -rin ">:"  cesm.exe.signalTable.txt > addrFuncName.txt

数据的部分内容，可能长这样

```bash
7418504:000000000249b2f0 <__intel_memset>:
7420446:000000000249c4d0 <__intel_ssse3_memcpy>:
7423051:000000000249eea0 <__intel_ssse3_rep_memcpy>:
7425432:00000000024a1960 <__intel_ssse3_memmove>:
7428140:00000000024a44e0 <__intel_ssse3_rep_memmove>:
7430533:00000000024a6fe0 <__libirc_get_msg>:
7430678:00000000024a7260 <__libirc_print>:
7430861:00000000024a7560 <__cacheSize>:
7431196:00000000024a7a30 <__sti__$E>:
7431684:00000000024a8160 <__intel_proc_init_ftzdazule>:
7431752:00000000024a8250 <__libc_csu_init>:
7431792:00000000024a82c0 <__libc_csu_fini>:
7431797:00000000024a82c4 <_fini>:
```

3、后处理addrFuncName.txt

先用sed命令，干掉 ":", "<", ">";

sed "s\:\ \g" addFuncName.txt | sed "s\<\ \g" | sed "s\>\ \g"

```bash
7420446 000000000249c4d0  __intel_ssse3_memcpy  
7423051 000000000249eea0  __intel_ssse3_rep_memcpy  
7425432 00000000024a1960  __intel_ssse3_memmove  
7428140 00000000024a44e0  __intel_ssse3_rep_memmove  
7430533 00000000024a6fe0  __libirc_get_msg  
7430678 00000000024a7260  __libirc_print  
7430861 00000000024a7560  __cacheSize  
7431196 00000000024a7a30  __sti__$E  
7431684 00000000024a8160  __intel_proc_init_ftzdazule  
7431752 00000000024a8250  __libc_csu_init  
7431792 00000000024a82c0  __libc_csu_fini  
7431797 00000000024a82c4  _fini
```

再使用awk命令，取第2、3列

awk '{print $2, $3}' 

sed "s\:\ \g" addFuncName.txt | sed "s\<\ \g" | sed "s\>\ \g"  | awk '{print $2, $3}'

```bash
00000000024a1960 __intel_ssse3_memmove
00000000024a44e0 __intel_ssse3_rep_memmove
00000000024a6fe0 __libirc_get_msg
00000000024a7260 __libirc_print
00000000024a7560 __cacheSize
00000000024a7a30 __sti__$E
00000000024a8160 _ _intel_proc_init_ftzdazule
00000000024a8250 __libc_csu_init
00000000024a82c0 __libc_csu_fini
00000000024a82c4 _fini
```

最后再用sed 结合正则表达式替换到全零的部分

sed "s\00*00\ \g"

sed "s\:\ \g" addFuncName.txt | sed "s\<\ \g" | sed "s\>\ \g" | awk '{print $2, $3}'| sed "s\00*00\ \g"

```bash
 2499b40 __intel_memcpy
 249b2f0 __intel_memset
 249c4d0 __intel_ssse3_memcpy
 249eea0 __intel_ssse3_rep_memcpy
 24a1960 __intel_ssse3_memmove
 24a44e0 __intel_ssse3_rep_memmove
 24a6fe0 __libirc_get_msg
 24a7260 __libirc_print
 24a7560 __cacheSize
 24a7a30 __sti__$E
 24a8160 __intel_proc_init_ftzdazule
 24a8250 __libc_csu_init
 24a82c0 __libc_csu_fini
 24a82c4 _fini
```
