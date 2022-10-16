

/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi
@花 并行A6上用的MPI库


LLVM是一个**模块化的**、**可重复使用**的**编译器和工具的集合**，提供了与编译器相关的扩展支持，可以用做多用语言的编译器后台。Clang和Flang是支持C/C++和Fortran编译器，与LLVM一起构成完整的工具链，支持多种操作系统和硬件架构，可代替GCC编译系统。由于LLVM采用模块化的库架构设计，因此，它很容易嵌入到各种应用程序中。通过LLVM可以实现对程序中函数的插装。

由于LLVM采用模块化的库架构设计，因此，它**可以选择执行特定的优化方法**，而不像传统的编译器优化器，他们通常是由大量高度耦合的代码组成，很难拆分成容易理解和使用的小模块，而LLVM则可以通过库来自定义优化方法，而无需担心其他依赖该优化方法的组件，也无需知道整个系统是如何工作的。

**LLVM 的Pass框架**是LLVM系统的一个很重要的部分。Pass可以**对源代码进行分析、优化或者转化的工作**，它是**对编译器的补充**。所有LLVM Pass都是Pass类的子类，它们通过**重写从Pass继承的虚拟方法来实现功能**。根据编写的Pass的不同功能需求，我们应该从ModulePass，CallGraphSCCPass，FunctionPass或LoopPass或RegionPass类继承，这些类可以实现**对中间文件中各个模块的分析、优化和转化**。当实现了自定义Pass后，我们**通过特定的编译指令将Pass源文件编译成动态链接库，然后用优化器将Pass编译成的动态链接库运行在由源文件通过LLVM生成的中间文件上，实现对其进行分析、优化或者转化，产生新的中间文件**。这样，新的中间文件就是原来的中间文件经过分析、优化或者转化后的中间文件。

##### 想看探针里的printf有两种方法
1、还是之前的cp，但是不要复制在同一目录下，换到算例目录下，如：cp ./cesm.log.$LID ../test.log
2、在探针里直接将printf写入某文件里，文件名以进程号开头避免写冲突
这个方法也可以解决之前探针写文件因多进程导致的写冲突问题，中间所有计时都是插入红黑树中，最后0号进程写入文件里，如果你想看多个进程写文件，可以把文件名以进程号开头避免写冲突

### 进展汇报：


### 试验记录：
case001:  
1、证明了，自动采用脚本可以接受参数名字，创建不同的case，然后跑通;
（并且验证了，running log 在任务跑完之后，log会压缩归档到archive下面一份，还有logs下面一份）

2、验证，删除archive, timing, 然后cleanBuild, Build, submit任务，的可行性；

case002: 
1、验证一下插装打印log,是否可以找到 - ERROR

case003:
1、验证只加上编译选项，其他什么也不改，是否会跑成功 - ERROR
2、验证只加上编译选项，同时加上链接库的选项-L 

case004:
1、通过case003 、 case004分别给FFlags ，CFlags添加编译选项  -finstrument-functions

===>>   验证了，`只要是在CFlags 后加入-finstrument-functions` ，就会导致算例不行不成功，出现很多killed

case005:
1、验证过，编译选项加在前面，其他什么都没有该，还是不行


case006: 又出现了  Makefile.conf 的问题

case007: 一切就是那么正常，但是就是没有生成trace文件

case008: 
只改了模式天数，其他什么也没有改,的基础上，进行添加编译选项，插装 - 未找到文件

case009:

1、尝试统一工具链，全部采用 inter的工具链`（使用inter的编译器，编译插装静态库）`


2、修改文件产位置 为./

方向：
1、单个C文件，编译

2、放弃C

3、两个方向，插装C； 不插装C，解决问题
 
4、形成一个手册



all 没有trance文件

case010:
还是没有生成文件。。

为什么没有生成trace文件:
1、难道产生到其他机器上了吗，找不到路径？
2、产生静态库的方法有问题吗？

```c
Thu Oct 6 22:05:33 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case006/bld/mct/mct.bldlog.221006-220528
Copying source to CCSM EXEROOT...
mkdir: cannot create directory ‘mct’: File exists
mkdir: cannot create directory ‘mpeu’: File exists
mkdir: cannot create directory ‘mpi-serial’: File exists
MCT already built. Checking machine type
Same machine.
cp: cannot stat ‘Makefile.conf.old’: No such file or directory
cp: cannot stat ‘Makefile.conf’: No such file or directory
Makefile:4: Makefile.conf: No such file or directory
gmake: *** No rule to make target `Makefile.conf'.  Stop.
```



============================================================================
### 设计实验、从编译角度探索一下问题：
#### （1、探索编译选项插入行为；2、为什么CFLAGS添加编译选项，导致模式无法运行；3、如何正确插装）：
* case012：单给CFLAGS添加 -finstrument-functions ；
* case013：单给FFLAGS添加 -finstrument-functions ；
* case014：同时给CFLAGS、FFLAGS添加 -finstrument-functions ；
  
* case015：单给FFLAGS添加 -finstrument-functions； 并且链接探针实现；
  
------> （NOTE：与case013对照，可以探究是否真正插入探针实现）

* case016:（ 什么编译选项都不加，也不链接额外的库，跟以上case做对照）

#### 结果：

<1>、CFLAGS添加编译选项，导致模式无法运行的原因是，gptl库上有探针实现函数，并且此函数前面没有不插装的属性，所以导致探针函数无穷递归下去，函数栈溢出，被srun kill;

<2>、只给FFLAGS添加编译选项，模式可以正常运行，但是插装探针的实现是GPTL库的实现；

<3>、同时添加编译选项，因为CFLAGS的原因（第一个结果），导致模式无法正常正常运行；

<4>、单给FFLAGS添加 -finstrument-functions； 并且链接探针实现；---- >   从反汇编代码可以看出来，探针的实现并不是我们自己的实现；

<5>、从（case16: 什么编译选项都不加，也不链接额外的库，跟以上case做对照） ---- > 
 从反汇编代码可以看出来，只是有GPTL库对探针的定义，但是没有插装；


#### 从上述结果，设计实验，如何正确插装：
* case017：首先先要验证自行插装可行性

    条件一：可以暂时不考虑gptl库,不把他编入模式中；
    
    条件二：为了分析结果简单起见，只给FFLGAS添加编译选项；

    条件三：为了保证插装成功行，只实现一个简单的探针实现，并且使用统一编译工具链；

如果验证成功，我们可以得到以下结论：

可以从汇编符号表角度出发，确定插装结果：

1、编译选项是否生效；（每个函数入口，都会有探针符号）
2、探针的实现是否是我们自己的探针实现；（通过对比`插装目标产物里面的探针实现的符号表`和`自己产生静态库的符号表`）
#### 以上相关试验记录：
* case012：单给CFLAGS添加 -finstrument-functions ；
  
```c
5828290 0000000001d64db0 <__cyg_profile_func_enter>:
5828291  1d64db0:   55                      push   %rbp
5828292  1d64db1:   48 89 fd                mov    %rdi,%rbp
5828293  1d64db4:   bf b0 4d d6 01          mov    $0x1d64db0,%edi
5828294  1d64db9:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5828295  1d64dbe:   e8 ed ff ff ff          callq  1d64db0 <__cyg_profile_func_enter>
5828296  1d64dc3:   48 89 ef                mov    %rbp,%rdi
5828297  1d64dc6:   e8 15 00 00 00          callq  1d64de0 <GPTLstart_instr>
5828298  1d64dcb:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5828299  1d64dd0:   bf b0 4d d6 01          mov    $0x1d64db0,%edi
5828300  1d64dd5:   5d                      pop    %rbp
5828301  1d64dd6:   e9 b5 64 00 00          jmpq   1d6b290 <__cyg_profile_func_exit>
5828302  1d64ddb:   0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
5828303 
5828304 0000000001d64de0 <GPTLstart_instr>:
5828305  1d64de0:   41 54                   push   %r12
5828306  1d64de2:   41 57                   push   %r15
5828307  1d64de4:   56                      push   %rsi
5828308  1d64de5:   49 89 ff                mov    %rdi,%r15
5828309  1d64de8:   bf e0 4d d6 01          mov    $0x1d64de0,%edi
5828310  1d64ded:   48 8b 74 24 18          mov    0x18(%rsp),%rsi
5828311  1d64df2:   e8 b9 ff ff ff          callq  1d64db0 <__cyg_profile_func_enter>


[fio_climate_model@ln131%bscc-a6 bld]$ grep -rin "__cyg_profile_func_enter" case012Assmble.txt | wc -l
116

```

* case013：单给FFLAGS添加 -finstrument-functions ；
```c
5539462 0000000001c1ce00 <__cyg_profile_func_enter>:
5539463  1c1ce00:   41 55                   push   %r13
5539464  1c1ce02:   41 56                   push   %r14
5539465  1c1ce04:   41 57                   push   %r15
5539466  1c1ce06:   53                      push   %rbx
5539467  1c1ce07:   55                      push   %rbp
5539468  1c1ce08:   48 89 fb                mov    %rdi,%rbx
5539469  1c1ce0b:   8b 05 af 9f 5d 06       mov    0x65d9faf(%rip),%eax        # 81f6dc0 <disabled>
5539470  1c1ce11:   85 c0                   test   %eax,%eax
5539471  1c1ce13:   0f 85 8e 01 00 00       jne    1c1cfa7 <__cyg_profile_func_enter+0x1a7>
5539472  1c1ce19:   8b 05 91 9f 5d 06       mov    0x65d9f91(%rip),%eax        # 81f6db0 <initialized>
5539473  1c1ce1f:   85 c0                   test   %eax,%eax
5539474  1c1ce21:   0f 84 6a 03 00 00       je     1c1d191 <__cyg_profile_func_enter+0x391>
5539475  1c1ce27:   4c 8b 05 4a 9f 5d 06    mov    0x65d9f4a(%rip),%r8        # 81f6d78 <stackidx>


[fio_climate_model@ln131%bscc-a6 bld]$ grep -rin "__cyg_profile_func_enter" case013Assmble.txt | wc -l
6546
```

* case014：同时给CFLAGS、FFLAGS添加 -finstrument-functions ；
```c
5531178 0000000001c15280 <__cyg_profile_func_enter>:
5531179  1c15280:   55                      push   %rbp
5531180  1c15281:   48 89 fd                mov    %rdi,%rbp
5531181  1c15284:   bf 80 52 c1 01          mov    $0x1c15280,%edi
5531182  1c15289:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5531183  1c1528e:   e8 ed ff ff ff          callq  1c15280 <__cyg_profile_func_enter>
5531184  1c15293:   48 89 ef                mov    %rbp,%rdi
5531185  1c15296:   e8 15 00 00 00          callq  1c152b0 <GPTLstart_instr>
5531186  1c1529b:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5531187  1c152a0:   bf 80 52 c1 01          mov    $0x1c15280,%edi
5531188  1c152a5:   5d                      pop    %rbp
5531189  1c152a6:   e9 b5 64 00 00          jmpq   1c1b760 <__cyg_profile_func_exit>
5531190  1c152ab:   0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
5531191 
5531192 0000000001c152b0 <GPTLstart_instr>:
5531193  1c152b0:   41 54                   push   %r12



[fio_climate_model@ln131%bscc-a6 bld]$ grep -rin "__cyg_profile_func_enter" case014Assmble.txt | wc -l
6631



```
  
* case015：单给FFLAGS添加 -finstrument-functions； 并且链接探针实现；
```c
5531178 0000000001c15280 <__cyg_profile_func_enter>:
5531179  1c15280:   55                      push   %rbp
5531180  1c15281:   48 89 fd                mov    %rdi,%rbp
5531181  1c15284:   bf 80 52 c1 01          mov    $0x1c15280,%edi
5531182  1c15289:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5531183  1c1528e:   e8 ed ff ff ff          callq  1c15280 <__cyg_profile_func_enter>
5531184  1c15293:   48 89 ef                mov    %rbp,%rdi
5531185  1c15296:   e8 15 00 00 00          callq  1c152b0 <GPTLstart_instr>
5531186  1c1529b:   48 8b 74 24 08          mov    0x8(%rsp),%rsi
5531187  1c152a0:   bf 80 52 c1 01          mov    $0x1c15280,%edi
5531188  1c152a5:   5d                      pop    %rbp
5531189  1c152a6:   e9 b5 64 00 00          jmpq   1c1b760 <__cyg_profile_func_exit>
5531190  1c152ab:   0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
5531191 
5531192 0000000001c152b0 <GPTLstart_instr>:
5531193  1c152b0:   41 54                   push   %r12


[fio_climate_model@ln131%bscc-a6 bld]$  grep -rin "__cyg_profile_func_enter" case015Assmble.txt | wc -l
6546

```
  
------> （NOTE：与case013对照，可以探究是否真正插入探针实现）

* case016:（ 什么编译选项都不加，也不链接额外的库，跟以上case做对照）

```c
5841843 0000000001d71e60 <__cyg_profile_func_enter>:
5841844  1d71e60:   41 55                   push   %r13
5841845  1d71e62:   41 56                   push   %r14
5841846  1d71e64:   41 57                   push   %r15
5841847  1d71e66:   53                      push   %rbx
5841848  1d71e67:   55                      push   %rbp
5841849  1d71e68:   48 89 fb                mov    %rdi,%rbx
5841850  1d71e6b:   8b 05 0f f4 5c 06       mov    0x65cf40f(%rip),%eax        # 8341280 <disabled>
5841851  1d71e71:   85 c0                   test   %eax,%eax
5841852  1d71e73:   0f 85 8e 01 00 00       jne    1d72007 <__cyg_profile_func_enter+0x1a7>
5841853  1d71e79:   8b 05 f1 f3 5c 06       mov    0x65cf3f1(%rip),%eax        # 8341270 <initialized>
5841854  1d71e7f:   85 c0                   test   %eax,%eax
5841855  1d71e81:   0f 84 6a 03 00 00       je     1d721f1 <__cyg_profile_func_enter+0x391>
5841856  1d71e87:   4c 8b 05 aa f3 5c 06    mov    0x65cf3aa(%rip),%r8        # 8341238 <stackidx>
5841857  1d71e8e:   c7 05 28 cb bd 04 01    movl   $0x1,0x4bdcb28(%rip)        # 694e9c0 <nthreads>
5841858  1d71e95:   00 00 00
5841859  1d71e98:   45 8b 08                mov    (%r8),%r9d
5841860  1d71e9b:   44 3b 0d 16 cb bd 04    cmp    0x4bdcb16(%rip),%r9d        # 694e9b8 <depthlimit>
5841861  1d71ea2:   7c 0f                   jl     1d71eb3 <__cyg_profile_func_enter+0x53>
5841862  1d71ea4:   41 ff c1                inc    %r9d
5841863  1d71ea7:   45 89 08                mov    %r9d,(%r8)
5841864  1d71eaa:   5d                      pop    %rbp
5841865  1d71eab:   5b                      pop    %rbx



[fio_climate_model@ln131%bscc-a6 bld]$ grep -rin "__cyg_profile_func_enter" case016Assmble.txt | wc -l
31

```


##### 关键符号：
```c
nm -e file(符号表符号):
0000000000402e10 T __cyg_profile_func_enter
0000000000402e7f T __cyg_profile_func_exit

objdump -d file(汇编符号):
objdump -d cesm.exe > case016Assmble.txt
grep -rin __cyg_profile_func_enter case016Assmble.txt

addr2line -e **** (地址到函数名转换):

```
### 怀疑点记录：
* 1、编译工具链不一致，导致最后连接的时候，没有真正链接成功？
* 2、生成探针实现静态库的方法，难道不正确，是不是生成静态库的命令缺少什么参数？从而导致生成的静态库导致最后无法链接成功？

##### GPTL

GPTL: GPTL is the "`General Purpose Timing Library`"
```c

gtplBuildLog

 1 Sat Oct 15 20:46:59 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/case016/bld/gptl/gptl.bldlog.221015-204608
  2 Copying source to CESM EXEROOT...
  3 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/gptl.c
  4 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/GPTLutil.c
  5 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/GPTLget_memusage.c
  6 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/GPTLprint_memusage.c
  7 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/gptl_papi.c
  8 mpiicc   -c   -fp-model precise  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing/f_wrappers.c
  9 mpiifort  -c   -fp-model source -convert big_endian -assume byterecl -ftz -traceback  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI -free   /public1/home/fio_climate_model/FIO-ESM/fi    oesm/fioesm2_0/models/utils/timing/perf_utils.F90
 10 mpiifort  -c   -fp-model source -convert big_endian -assume byterecl -ftz -traceback  -DFORTRANUNDERSCORE -DNO_R16 -DLINUX -DCPRINTEL  -DHAVE_MPI -free   /public1/home/fio_climate_model/FIO-ESM/fi    oesm/fioesm2_0/models/utils/timing/perf_mod.F90
 11 ar ruv libgptl.a gptl.o GPTLutil.o GPTLget_memusage.o GPTLprint_memusage.o gptl_papi.o f_wrappers.o perf_mod.o perf_utils.o
 12 ar: creating libgptl.a
 13 a - gptl.o
 14 a - GPTLutil.o
 15 a - GPTLget_memusage.o
 16 a - GPTLprint_memusage.o
 17 a - gptl_papi.o
 18 a - f_wrappers.o
 19 a - perf_mod.o
 20 a - perf_utils.o
 21 cp -p *.mod /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/case016/bld/lib/include
 22 cp -p libgptl.a /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/case016/bld/lib


[fio_climate_model@ln132%bscc-a6 timing]$ grep -rin __cyg_profile_func_enter
gptl.c:3590:void __cyg_profile_func_enter (void *this_fn,
private.h:123:extern void __cyg_profile_func_enter (void *, void *);
README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,

[fio_climate_model@ln132%bscc-a6 timing]$ ls
ChangeLog       COPYING       gptl.c              gptl.h    gptl_papi.c           GPTLutil.c  perf_mod.F90    private.h
CMakeLists.txt  f_wrappers.c  GPTLget_memusage.c  gptl.inc  GPTLprint_memusage.c  Makefile    perf_utils.F90  README

/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/utils/timing

vim +3590 gptl.c

3590 void __cyg_profile_func_enter (void *this_fn,
3591                                void *call_site)
3592 {
3593   (void) GPTLstart_instr (this_fn);
3594 }
3595 
3596 void __cyg_profile_func_exit (void *this_fn,
3597                               void *call_site)
3598 {
3599   (void) GPTLstop_instr (this_fn);
3600 }


尝试去使用GPTL库：
feng@wangfeng:~/ecnu/ecnu-wys/ecasm/GPTL/timing$ gcc -c *.c
feng@wangfeng:~/ecnu/ecnu-wys/ecasm/GPTL/timing$ mpifort -c *.F90
feng@wangfeng:~/ecnu/ecnu-wys/ecasm/GPTL/timing$ ar -r libgptl.a *.o
feng@wangfeng:~/ecnu/ecnu-wys/ecasm/GPTL$ gcc test.c -finstrument-functions -Ltiming -lgptl


feng@wangfeng:~/ecnu/ecnu-wys/ecasm/GPTL$ ./a.out 
GPTLstart_instr self=0x55fc0d35d531: GPTLinitialize has not been called
GPTLstart_instr self=0x55fc0d35d4d9: GPTLinitialize has not been called
GPTLstart_instr self=0x55fc0d35d489: GPTLinitialize has not been called
GPTLstop_instr: GPTLinitialize has not been called
GPTLstop_instr: GPTLinitialize has not been called
result: 20
GPTLstop_instr: GPTLinitialize has not been called

```

<__cyg_profile_func_enter>:

grep -rin "<__cyg_profile_func_enter>:" case014Assmble.txt

============================================================================
### 编译时间记录：

```c
Thu Oct 6 19:06:48 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/mct/mct.bldlog.221006-190640
Thu Oct 6 19:07:30 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/gptl/gptl.bldlog.221006-190640
Thu Oct 6 19:07:32 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/pio/pio.bldlog.221006-190640
Thu Oct 6 19:08:10 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/csm_share/csm_share.bldlog.221006-190640
Thu Oct 6 19:08:26 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/atm.bldlog.221006-190640
Thu Oct 6 19:09:29 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/lnd.bldlog.221006-190640
Thu Oct 6 19:11:32 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/ice.bldlog.221006-190640
Thu Oct 6 19:16:41 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/ocn.bldlog.221006-190640
Thu Oct 6 19:18:19 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/glc.bldlog.221006-190640
Thu Oct 6 19:18:20 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/wav.bldlog.221006-190640
Thu Oct 6 19:18:20 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/rof.bldlog.221006-190640
Thu Oct 6 19:18:27 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/case001/bld/cesm.bldlog.221006-190640
```
1、编译共用时12min左右

2、其中ocn大约5min

===>> 编译的时候，可以并行编译，加速编译时间

gcc test2.c -finstrument-functions -L. -lfinstrument