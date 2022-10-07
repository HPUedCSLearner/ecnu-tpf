

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