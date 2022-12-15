

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
首先先要验证自行插装可行性

    条件一：可以暂时不考虑gptl库,不把他编入模式中；(尝试通过一下几种方法)
        
        1、给gptl库里面的探针改名（改实现和头文件，最小程度影响原模式的运行）
        2、直接删除timing,不知道是否会影响原模式的运行
    
    条件二：为了分析结果简单起见，只给FFLGAS添加编译选项；

    条件三：为了保证插装成功行，只实现一个简单的探针实现，并且使用统一编译工具链；

/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/esm_liuyao/timing_probe_1001/libprobeso/Mpiifortran

libfunctrace.a

* case017：给gptl库里面的探针改名（改实现和头文件，最小程度影响原模式的运行）

```c
[fio_climate_model@ln131%bscc-a6 timing]$ grep -rin __cyg_profile_func_enter
gptl.c:3590:void __cyg_profile_func_enter (void *this_fn,
private.h:123:extern void __cyg_profile_func_enter (void *, void *);
README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,
[fio_climate_model@ln131%bscc-a6 timing]$ vim +3590 gptl.c
[fio_climate_model@ln131%bscc-a6 timing]$ vim +123 private.h

[fio_climate_model@ln131%bscc-a6 timing]$ grep -rin wys
gptl.c:3590:void __wys__cyg_profile_func_enter (void *this_fn,
gptl.c:3596:void __wys__cyg_profile_func_exit (void *this_fn,
private.h:123:extern void __wys__cyg_profile_func_enter (void *, void *);
private.h:124:extern void __wys__cyg_profile_func_exit (void *, void *);
```


如果验证成功，我们可以得到以下结论：

可以从汇编符号表角度出发，确定插装结果：

1、编译选项是否生效；（每个函数入口，都会有探针符号）

2、探针的实现是否是我们自己的探针实现；（通过对比`插装目标产物里面的探针实现的符号表`和`自己产生静态库的符号表`）

==============================================================================

* case18:
完成简易的测量信息写入文件中：
简化实验条件：
    一：探针内容的简化；
    二：进程数修改为8；模式天为一天
    三：全模式穿行

修改gptl.c文件
cp  utils_timing/timing/gptl.c cases/case020/sampling/models/utils/timing/
* case19:
作为以上实验，不插装的对照（进程数修改为8；模式天为一天；全模式穿行；），看是否可以跑成功

```c

    Init Time   :      60.787 seconds 
    Run Time    :     707.964 seconds      707.964 seconds/day 
    Final Time  :       0.029 seconds 
```
* case20:
先不插装的对照（进程数修改为8；模式天为一秒钟；全模式穿行；）
```c
    Init Time   :      37.386 seconds 
    Run Time    :      14.590 seconds      700.320 seconds/day 
    Final Time  :       0.035 seconds 

```
然后，使用简单的探针进行插装：
```c
    Init Time   :      38.965 seconds 
    Run Time    :      18.170 seconds      872.160 seconds/day 
    Final Time  :       0.040 seconds 

```

* case21:
不插装的对照（进程数修改为8；模式天为一分钟；全模式穿行；）
```c
    Init Time   :      54.688 seconds 
    Run Time    :      14.788 seconds      709.824 seconds/day 
    Final Time  :       0.033 seconds
```
* case22:
不插装的对照（进程数修改为8；模式天为一小时；全模式穿行；）
```c
    Init Time   :      37.181 seconds 
    Run Time    :      28.718 seconds      689.232 seconds/day 
    Final Time  :       0.047 seconds 
```





#### 组会：2022/10/30记录
##### 问题：
* 1、插装小实验已经成功，但是对生成的trace文件有点疑惑？
##### 移植忆莲探针实现遇到的问题：
* 2、师姐探针的实现，看代码的话，写文件的操作是让一个进程完成，那其他进程记录在红黑树的采样信息是怎么写到文件上的？
* 3、将timer.c编成静态库，给test.c文件实验插装，从反汇编看，好像是没有插入成功，没有报错，好像是没有链接成功；
    从实际的运行看，也没有成功；
* 4、timer的实现中，tauutil.h的文件,是不是没有使用，如果使用的话 怎么使用
* 5、timer的实现中，comm.h 的作用是区分不同模块的吗？

#### 组会：2022/11/06记录
/public1/home/fio_climate_model/esm_liuyao/bin/cmake-3.24.3-linux-x86_64/bin/cmake
* 总体进展：
  * 1、trace文件生成按照 进程号（目前非mpi进程号）- 时间 命名
  * 2、使用师姐的探针实现，自测插装效果，能够生成文件
* 问题：
  * 1、使用MPI的进程号出现问题：
  Attempting to use an MPI routine (internal_Comm_size) before initializing or after finalizing MPICH

##### 一些现象：
* 1、当我把mpiwraper编进去以后，就出现奇怪的事情了,，(-lmylib 不能正常编译，mct模块编译就报错)
  * 此时，会报错,很奇怪的错
  * 表象的原因，在编译mct的时候，直接要去链接-lmylib，`这个是我没有想到的，`所以，我又把链接-lmylib的操作放到了Makefile里面,但是出现了如下情况；
* 2、如果不把gptl里面探针入口注释掉，同时加上编译选项在Macro里面，并且在Makefile里面链接探针的实现;
  * 此时，会报错GPTL_start() : has no initialiczed (说明，这种方法链接的是原来的库里面的探针入口函数)
  * 但是，把探针入口给就加上__wys__***， 就会出现模式无法成功运行；（`连接上自己的探针实现`，说明，自己的探针实现可能有问题）
* 3、从只打印一个进程的log看，只有4G左右，之前八个进程疯狂打印，有三四十个G，这个也算可以说通
* 4、加上 -no-pie 看是否可以对应上函数


##### 为什么插入探针，模式运行不成功？？
* 运行到一定程度什么也不输出，包括cesm本身的log，也包括探针里面的log?
* 模式陷入了死循环，导致其出不来



#### 组会：2022/11/13记录
从目前所作的一些实验看来，插装之后，模式应该是陷入了死循环

#### 设计实验：
* case025: 简单插装，只打印函数调用关系，只打印一个mpi进程
/public1/home/fio_climate_model/esm_liuyao/cases/case025/run/cesm.log.221113-090920

```c 86586 enter func: MPI_Allreduce father: mpi_allreduce_
 86587 exit func: MPI_Allreduce father: mpi_allreduce_
 86588 exit func: parutilitiesmodule_mp_parcollective1dint_ father: dyn_comp_mp_dyn_init_
 86589 enter func: parutilitiesmodule_mp_parcollective1dint_ father: dyn_comp_mp_dyn_init_
 86590 enter func: MPI_Allreduce father: mpi_allreduce_
 86591 exit func: MPI_Allreduce father: mpi_allreduce_
 86592 exit func: parutilitiesmodule_mp_parcollective1dint_ father: dyn_comp_mp_dyn_init_
 86593 enter func: parutilitiesmodule_mp_parcollective1dint_ father: dyn_comp_mp_dyn_init_
 86594 enter func: MPI_Allreduce father: mpi_allreduce_
 86595 exit func: MPI_Allreduce father: mpi_allreduce_
 86596 exit func: parutilitiesmodule_mp_parcollective1dint_ father: dyn_comp_mp_dyn_init_
 86597 enter func: (null) father: dyn_comp_mp_dyn_init_
 86598 exit func: (null) father: dyn_comp_mp_dyn_init_
 86599 enter func: dycore_mp_get_resolution_ father: dyn_comp_mp_dyn_init_
 86600 exit func: dycore_mp_get_resolution_ father: dyn_comp_mp_dyn_init_
 86601 enter func: (null) father: dyn_comp_mp_dyn_init_
 86602 enter func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86603 exit func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86604 enter func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86605 exit func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86606 enter func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86607 exit func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 86608 enter func: shr_infnan_mod_mp_set_r8_inf_ father: (null)
 ```

```bash
[fio_climate_model@ln132%bscc-a6 models]$ ls
atm  csm_share  dead_share  drv  glc  ice  lnd  ocn  rof  utils  wav
[fio_climate_model@ln132%bscc-a6 models]$ grep -rin __cyg_profile_func_enter
utils/timing/gptl.c:3590:void __cyg_profile_func_enter (void *this_fn,
utils/timing/private.h:123:extern void __cyg_profile_func_enter (void *, void *);
utils/timing/README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,
glc/cism/glimmer-cism/libgptl/gptl.c:3584:void __cyg_profile_func_enter (void *this_fn,
glc/cism/glimmer-cism/libgptl/private.h:123:extern void __cyg_profile_func_enter (void *, void *);
glc/cism/glimmer-cism/libgptl/README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,
[fio_climate_model@ln132%bscc-a6 models]$ pwd
/public1/home/fio_climate_model/esm_liuyao/cases/case026/sampling/models

[fio_climate_model@ln132%bscc-a6 models]$ vim +3590 utils/timing/gptl.c
[fio_climate_model@ln132%bscc-a6 models]$ vim +123 utils/timing/private.h
[fio_climate_model@ln132%bscc-a6 models]$ 
[fio_climate_model@ln132%bscc-a6 models]$ vim +3584 glc/cism/glimmer-cism/libgptl/gptl.c
[fio_climate_model@ln132%bscc-a6 models]$ vim +123 glc/cism/glimmer-cism/libgptl/private.h
```

试一下，只对一种语言添加flag
* case025:
  * 双return、双flags
  * 单flas
  * 
* case026:
##### 第一次实验：双flags，空实现的探针
###### 实验结果：跑成功
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.0/build/src
 * 文件路径: /public1/home/fio_climate_model/esm_liuyao/cases/case026/timing
 * timing文件:ccsm_timing.case026.221126-133918
###### 实验结论：
* 我们可以拿到该模式所有运行时的 caller, callee的关系 (由此，按道理来说，我们可以拿到所有采样信息)


##### 第二次实验：双flags，探针的实现 -> 添加上perf_counter()接口 (排除perf_counter()可能导致插装运行失败的情况)
###### 实验结果：跑成功, 但是有个怪现象（模式跑完的实践是原来的一倍（原先是50s，这次是100s））
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.1/build/src
 * 文件路径: /public1/home/fio_climate_model/esm_liuyao/cases/case026/timing
 * timing文件:ccsm_timing.case026.221126-144740
###### 实验结论：
* 1、对这次怪现象的猜测：可能是因为模式天数少，导致插装的开销跟原来运行的时间接近，导致出现一倍的差距
* 2、perf_counter()不是 导致 插装运行失败的原因

##### 第三次实验：只是再次验证上面的实验结果
###### 实验结果：跑成功
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.1/build/src
 * 文件路径: /public1/home/fio_climate_model/esm_liuyao/cases/case026/timing
 * timing文件:ccsm_timing.case026.221126-150921
###### 实验结论：
* 1、不是偶然的，导致出怪现象
* 2、如果要验证上面的猜想，需要在模式天数较大的情况下，进行一组对照实验（插装的，不插装的）
这个很重要，因为我们要确定出，差一倍的时间，[是否是每次的开销都这么大]



关键实验 (如果解决了这个问题，就可以使用C++，实现探针了)
##### 第四次实验：双flags，探针的实现  -> 添加上perf_counter()接口
#####                                  ->  添加上__cxa_demangle()接口 (排除__cxa_demangle()可能导致插装运行失败的情况)
###### 实验结果：跑失败, 模式一直出不来，scancel的时候，已经跑了20min了
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.2/build/src
 * some clues:
  * 1、some symbles : _dl_addr \ tbk_getModuleName>: \  dladdr (__cxa_demangle的内部实现)
  * 2、running log: cesm.log.221126-160840 (path:/public1/home/fio_climate_model/esm_liuyao/cases/case026/run)
  * 3、cesm.exe.221126-155415Assemble.txt (path: /public1/home/fio_climate_model/esm_liuyao/cases/case026/bld)
###### 实验结论：
* 1、模式一直出不来，scancel的时候，已经跑了20min了

##### 第五次实验：（作为第四次实验的对照）尝试调试debug、 探究失败原因
* 本打算，找到进程号，使用gdb -p processID 进行调试，打出调用栈，探究失败原因
* 但是，进程号一直找不到


##### 第六次实验：添加 时间栈
###### 实验结果：跑成功
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.3/build/src
 * running log: /public1/home/fio_climate_model/esm_liuyao/cases/case026/logs/221129-102614Log

```bash
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
##wys funcTimeStack_maxDepth is 1862
##wys funcAddrStack_maxDepth is 931
```

* case026:
##### 第七次实验：基于hash的探针实现
###### 实验结果：跑成功
 * 探针实现: /public1/home/fio_climate_model/esm_liuyao/probeLib/timerCHash/cyproject/libprobe/build/src
 * 文件路径: /public1/home/fio_climate_model/esm_liuyao/cases/case026/timing
 * timing文件:ccsm_timing.case026.221126-133918
###### 实验结论：
* 我们可以拿到该模式所有运行时的 caller, callee的关系 (由此，按道理来说，我们可以拿到所有采样信息)





## 20220-12-11，组会报告：
#### 像老师所说的，下班晚上回来跑几把模式，早上上班看看结果
期间发现，最近这周提交的作业需要很长时间，才被分到资源，
有天晚上回来较早，本来上多跑几把，但是八点多提交作业后，十一点多还没跑起来，第二天早上看了一下才跑完

#### 首先，发现了之前探针为什么失败
在日志中发现：forrtl: severe (174): SIGSEGV, segmentation fault occurred

当把代码 写到
在后处理中：发现funcTimeStk size is : 1160717855 出现了问题

```c
void __cyg_profile_func_enter(void *func, void *caller) {
  unsigned long long shell_start_time = perf_counter();
  push(&funcTimeStk, shell_start_time);
  push(&funcDddrStk, func);
  unsigned long long acc_start_time = perf_counter();
  push(&funcTimeStk, acc_start_time);
	
}

325 cesm.exe           00000000018C84FC  shr_infnan_mod_mp         333  shr_infnan_mod.F90
326 cesm.exe           0000000000DA186B  dyn_compdyn_init_         623  dyn_comp.F90
327 cesm.exe           0000000000DA0436  dyn_comp_mp_dyn_i         525  dyn_comp.F90
328 cesm.exe           00000000004D779D  inital_mp_cam_ini          36  inital.F90
329 cesm.exe           0000000000495B32  cam_comp_mp_cam_i         164  cam_comp.F90
330 cesm.exe           00000000004938BC  atm_comp_mct_mp_a         279  atm_comp_mct.F90
331 cesm.exe           0000000000436060  ccsm_comp_mod_mp_        1064  ccsm_comp_mod.F90
332 cesm.exe           0000000000438202  MAIN__                     90  ccsm_driver.F90
333 cesm.exe           000000000041619E  Unknown               Unknown  Unknown
334 libc-2.17.so       00002B809F408555  __libc_start_main     Unknown  Unknown
335 cesm.exe           00000000004160A9  Unknown               Unknown  Unknown
336 hash size is : 0
337 funcTimeStk size is : 1160717855
338 funcDddrStk size is : 50000
339 my __profile__rank is : 0


hash size is : 0
funcTimeStk size is : 1165225319
funcDddrStk size is : 50000
my __profile__rank is : 0
forrtl: severe (174): SIGSEGV, segmentation fault occurred


/public1/home/fio_climate_model/esm_liuyao/cases/case026/run/cesm.log.221207-214118
/public1/home/fio_climate_model/esm_liuyao/cases/case026/run/cesm.log.221207-223043

severe (174): SIGSEGV, segmentation fault occurred
函数调用栈溢出
当我们使用的push的时候，并且是源码里面的第一个push
猜测：说明，在模式运行的某个时刻的时候，里面的函数（可以看打印日志的地方）调用了push（可以看源码； 可以看反汇编）

如果是，我们把原来模式里面的函数，给替换掉了，那么问题肯定就大了

解决方法：
1、使用 __attribute__(no_instrument_function) 属性，声明不插装
2、混淆我们的函数实现，避免与被测函数重名；


```
##  发生了一个从来都没有发生的现象
#### 后来就编译不过了？以为我的探针有问题
cat /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.bldlog.221210-212003

##### （发现问题，只要加上插装flags 就会出现这个错误，我人麻了，破防了）

R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' （以前从来没有出现过，这周六就出现了这个问题，环境有问题吗？？）

cat /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.bldlog.221210-212003
最新的一次build：
 /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.bldlog.221211-093947

```bash
[fio_climate_model@ln132%bscc-a6 libprobe]$  cat /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.bldlog.221210-212003
Sat Dec 10 21:20:20 CST 2022 /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.bldlog.221210-212003
-------------------------------------------------------------------------
 Building a single executable version of CESM 
-------------------------------------------------------------------------
/public1/home/fio_climate_model/esm_liuyao/cases/case027/Tools/mkSrcfiles 
cp -f /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm/obj/Filepath /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm/obj/Deppath
/public1/home/fio_climate_model/esm_liuyao/cases/case027/Tools/mkDepends  Deppath Srcfiles > /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm/obj/Depends
/public1/home/fio_climate_model/esm_liuyao/cases/case027/Tools/mkSrcfiles 
mpiifort  -o /public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.exe ccsm_comp_mod.o ccsm_driver.o mrg_mod.o seq_avdata_mod.o seq_diag_mct.o seq_domain_mct.o seq_flux_mct.o seq_frac_mct.o seq_hist_mod.o seq_map_esmf.o seq_mald/lib/ -latm  -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/lib/ -lice  -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/lib/ -llnd  -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/lib/ -locnate_model/esm_liuyao/cases/case027/bld/lib/ -lglc  -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/lib/ -lwav -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/lib -lcsm_share  -L/public1/home/fio_climate_model7/bld/mct/mpeu -lmpeu -L/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/pio -lpio -lgptl -L/public1/soft/netcdf/4.4.1-parallel-icc17/lib -lnetcdff -lnetcdf   -mcmodel=large 
ccsm_comp_mod.o: In function `ccsm_comp_mod_mp_ccsm_pre_init_':
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:571:(.text+0x40c): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_cplid_' defined in COMMON section in /publ
ccsm_comp_mod.o: In function `ccsm_comp_mod_mp_ccsm_init_':
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1330:(.text+0xfb02): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1332:(.text+0xfb34): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1334:(.text+0xfb66): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1336:(.text+0xfb98): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1338:(.text+0xfbca): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1340:(.text+0xfbfc): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1342:(.text+0xfc2e): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_max_' defined in COMMON section
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1371:(.text+0x1001d): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_timemgr_mod_mp_seq_timemgr_histavg_type_' defined iseq_timemgr_mod.o)
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1936:(.text+0x1c6fd): relocation truncated to fit: R_X86_64_PC32 against symbol `seq_comm_mct_mp_num_inst_xao_' defined in COMMON sectio
/public1/home/fio_climate_model/esm_liuyao/cases/case027/sampling/models/drv/driver/ccsm_comp_mod.F90:1936:(.text+0x1c714): additional relocation overflows omitted from the output
gmake: *** [/public1/home/fio_climate_model/esm_liuyao/cases/case027/bld/cesm.exe] Error 1
[fio_climate_model@ln132%bscc-a6 libprobe]$ R_X86_64_PC32
bash: R_X86_64_PC32: command not found...
```

##### 网上问题解决方法一：
https://www.coder.work/article/6329758

您得到的错误由链接器返回，因为静态分配 block 的大小超出了 32 位寻址指令可以寻址的范围，即 2 GB。这与您使用 32 位还是 64 位整数索引数组无关 - `问题与静态分配数组的总大小有关`。这在这里详细解释:

gfortran for dummies: What does mcmodel=medium do exactly?

如您所见，为了解决此问题，您可以使用 -mcmodel=medium 编译您的代码。或 -mcmodel=large .然后允许使用大于 2 GB 的静态分配数组。

##### 网上问题解决方法二：
https://blog.csdn.net/qq_41035283/article/details/119614206

链接库中使用了libglog.so与libgflags.a，`编译时动态库与静态库不能混用`。

重新编译了gflags生成动态库libgflags.so，然后加入cmake的target_link_libraries中，问题解决。




#### 组会：2022/12/12记录
修改gptl源码：
```bash
[fio_climate_model@ln132%bscc-a6 models]$ grep -rin __cyg_profile_func_enter
utils/timing/gptl.c:3590:void __cyg_profile_func_enter (void *this_fn,
utils/timing/private.h:123:extern void __cyg_profile_func_enter (void *, void *);
utils/timing/README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,
glc/cism/glimmer-cism/libgptl/gptl.c:3584:void __cyg_profile_func_enter (void *this_fn,
glc/cism/glimmer-cism/libgptl/private.h:123:extern void __cyg_profile_func_enter (void *, void *);
glc/cism/glimmer-cism/libgptl/README:121:__cyg_profile_func_enter (void *this_fn, void *call_site) at function start,
[fio_climate_model@ln132%bscc-a6 models]$ pwd
/public1/home/fio_climate_model/zyp/tmp/case30/sampling/models

vim +3590 utils/timing/gptl.c
vim +123 utils/timing/private.h
vim +3584 glc/cism/glimmer-cism/libgptl/gptl.c
vim +123 glc/cism/glimmer-cism/libgptl/private.h

```


###### 实验结果之一：
hash size is : 0
funcTimeStk size is : 0
funcDddrStk size is : 0
maxDepthTimeStk is : 931
maxDepthDddrStk is : 1862
my __profile__rank is : 0
hash size is : 0
funcTimeStk size is : 0
funcDddrStk size is : 0
maxDepthTimeStk is : 931
maxDepthDddrStk is : 1862
my __profile__rank is : 0

/public1/home/fio_climate_model/zyp/tmp/case30/run/cesm.log.221212-224941

###### 实验结果之一：
/public1/home/fio_climate_model/zyp/tmp/case032
证明了，加入-finstrument-functions 后就会 出现R_X86_64_PC32的问题，无法构建通过；

### 模式适配以动态库桩
库地址： /public1/home/fio_climate_model/esm_liuyao/probeLib/timerShared/version0.0.1
插入探针库：
686 $(EXEC_SE): $(OBJS) $(ULIBDEP)
687     $(LD) -o $(EXEC_SE) $(OBJS) $(CLIBS) $(ULIBS) $(SLIBS) $(MLIBS) $(LDFLAGS) -L/public1/home/fio_climate_model/esm_liuyao/probeLib/timerShared/version0.0.1/probelib -lprobe -L/public1/home/fio_climate_model/esm_liuyao/probeLib/timerShared/version0.0.1/probelib/sharedlib -lprobeImpl 



Model did not complete - see /public1/home/fio_climate_model/zyp/tmp/case033/run/cesm.log.221215-092213
[fio_climate_model@ln132%bscc-a6 case033]$ 
[fio_climate_model@ln132%bscc-a6 case033]$ 
[fio_climate_model@ln132%bscc-a6 case033]$ tail -F /public1/home/fio_climate_model/zyp/tmp/case033/run/cesm.log.221215-092213 
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
/public1/home/fio_climate_model/zyp/tmp/case033/bld/cesm.exe: error while loading shared libraries: libprobeImpl.so: cannot open shared object file: No such file or directory
srun: error: ga1603: tasks 0-7: Exited with exit code 127



遇到问题：
一些动态库找不到
```bash
	linux-vdso.so.1 =>  (0x00007ffe166a9000)
	libprobeImpl.so => probelib/sharedlib/libprobeImpl.so (0x00002b751fcac000)
	libmpifort.so.12 => /public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/lib/libmpifort.so.12 (0x00002b751feae000)
	libmpi.so.12 => /public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/lib/debug_mt/libmpi.so.12 (0x00002b7520257000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00002b752139c000)
	librt.so.1 => /lib64/librt.so.1 (0x00002b75215a0000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00002b75217a8000)
	libm.so.6 => /lib64/libm.so.6 (0x00002b75219c4000)
	libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00002b7521cc6000)
	libc.so.6 => /lib64/libc.so.6 (0x00002b7521edc000)
	/lib64/ld-linux-x86-64.so.2 (0x00002b751fa88000)
	libimf.so => not found
	libsvml.so => not found
	libirng.so => not found
	libintlc.so.5 => not found
  ```


问题解决：
https://blog.csdn.net/airings/article/details/9110785
export LD_LIBRARY_PATH=/public1/soft/intel/2017/compilers_and_libraries/linux/lib/intel64:$LD_LIBRARY_PATH



#### 设计实验：
* case025: 简单插装，只打印函数调用关系，只打印一个mpi进程
/public1/home/fio_climate_model/esm_liuyao/cases/case025/run/cesm.log.221113-090920












很奇怪的是:使用CMAKE输出的demo都是null
```bash 
-------------------------------------------------------------------------
demo路径
/public1/home/fio_climate_model/esm_liuyao/probeLib/timerCppSelf/v0.0.2
-------------------------------------------------------------------------

enter func: (null) father: __libc_start_main
enter func: (null) father: (null)
enter func: (null) father: (null)
enter func: (null) father: (null)
i am AA()
enter func: (null) father: (null)
enter func: (null) father: (null)
i am CC()
exit func: (null) father: (null)
i am BB()
exit func: (null) father: (null)
exit func: (null) father: (null)
exit func: (null) father: (null)
exit func: (null) father: (null)
result: 20
exit func: (null) father: __libc_start_main
-------------------------------------------------------------------------

而使用下面的这个，就可以解析出来
mpiicpc utility/test.c -g -finstrument-functions -ldl -rdynamic -Lbuild/src -linstruProbe
-------------------------------------------------------------------------

enter func: main father: __libc_start_main
enter func: do_calc(int, int) father: main
enter func: do_multi(int, int) father: do_calc(int, int)
enter func: AA() father: do_multi(int, int)
i am AA()
enter func: BB() father: AA()
enter func: CC() father: BB()
i am CC()
exit func: CC() father: BB()
i am BB()
exit func: BB() father: AA()
exit func: AA() father: do_multi(int, int)
exit func: do_multi(int, int) father: do_calc(int, int)
exit func: do_calc(int, int) father: main
result: 20
exit func: main father: __libc_start_main
-------------------------------------------------------------------------
```


* case027:


#### 出现问题的记录：
1、不同平台的编译器的差异
2、会出现null的情况

#### 常用字符串：
mpiicc test/mpi1.c -L./build/src -linstruProbe -lstdc++ -ldl -rdynamic ; mpirun -n 3 ./a.out


##### Done
小疑问：
1、env_mach_pes.xml 中后面几个的含义是什么？
```c
<entry id="TOTALPES"   value="1024"  />    
<entry id="PES_LEVEL"   value="1r"  />    
<entry id="MAX_TASKS_PER_NODE"   value="64"  />    
<entry id="PES_PER_NODE"   value="$MAX_TASKS_PER_NODE"  />    
<entry id="COST_PES"   value="0"  />    
<entry id="CCSM_PCOST"   value="-3"  />    
<entry id="CCSM_TCOST"   value="0"  />    
<entry id="CCSM_ESTCOST"   value="1"  />    
```
2、进程排布全部穿行是否这样设置：(已解决)

3、lock文件修改是否有必要(已解决)
cp env_mach_pes.xml LockedFiles/env_mach_pes.xml.locked

==============================================================================
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