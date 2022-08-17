gcc_finstrument_functions
===========================



## 目录
* [关键词](#关键词)
* [volatile](#volatile)
* [tsc](#tsc)





https://kdocs.cn/l/crR2o6G6dWZg
```
Yeeland 小论文
基于新一代神威超算的HPC应用程序多参数性能建模研究

​‌‍‬⁠⁡⁢⁣⁤﻿小论文大纲 - 飞书云文档 (feishu.cn)

逸平给的 CESM 官网
CESM Models | CESM1.2 Series Public Release (ucar.edu)


CPC大夏蜜獾 时间流水线
（学习Athread 编程）月底做一次分享，但是机器没有？
**编程手册 逸平已经给过  --> 神威高性能计算机性能工具用户手册(V1.4)
以固定的频率跳动 ？ 跟实际跳动的有什么关系？
太湖之光
海洋之光 ？？学的话，以那个为准？
TSC相关
constant_tsc：含义是以固定的频率跳动，与cpu当前的频率无关。
nonstop_tsc：进入C-State也不会停止跳动。
基于这2个特性组合，称为 invariant tsc，即tsc是以理想中的恒定频率跳动，符合对时钟的假设

关键词：constant_tsc、nonstop_tsc



正确使用cpu提供的TSC
https://zhuanlan.zhihu.com/p/437178265
Linux上采用rdtsc指令对C/C++程序进行性能测试
https://blog.csdn.net/ithiker/article/details/119981737



Gcc插装学习
关键词：-finstrument-functions、c++filt、constant_tsc、nonstop_tsc


使用gcc的-finstrument-functions选项进行函数跟踪
https://blog.csdn.net/jasonchen_gbd/article/details/44044899

C++源码调用图生成器实现
https://segmentfault.com/a/1190000008314896

```
## 关键词


`微基准测试:`   micro benchmark

## volatile




[`__asm__ __volatile__ :`](http://www.javashuo.com/article/p-aaglncbx-dz.html)


`__asm__` __volatile__内嵌汇编用法。

在阅读C/C++原码时常常会遇到`内联汇编`的状况，下面简要介绍下__asm__ __volatile__内嵌汇编用法。linux带有C/C++表达式的内联汇编格式为：

```cpp
__asm__　__volatile__("Instruction List" : Output : Input : Clobber/Modify);
```

其中每项的概念及功能用法描述以下：

一、 __asm__编译器

__asm__是GCC 关键字asm 的宏定义：

`#define __asm__ asmio`

__asm__或asm 用来声明一个内联汇编表达式，因此任何一个内联汇编表达式都是以它开头的，是必不可少的。

二、Instruction List编译

`Instruction List 是汇编指令序列`。它能够是空的，好比：`__asm__ __volatile__("");` 或 `__asm__ ("");`都是`彻底合法的内联汇编表达式`，只不过这两条语句没有什么意义。但并不是全部Instruction List 为空的内联汇编表达式都是没有意义的，好比：`__asm__ ("":::"memory");` 就很是有意义，`它向GCC 声明：“内存做了改动”，GCC 在编译的时候，会将此因素考虑进去`。 当在"Instruction List"中有多条指令的时候，能够在一对引号中列出所有指令，也能够将一条 或几条指令放在一对引号中，全部指令放在多对引号中。若是是前者，能够将每一条指令放在一行，`若是要将多条指令放在一行，则必须用分号（；）或换行符（\n）将它们分开`. 综上述：(1）每条指令都必须被双引号括起来。
(2) 两条指令必须用换行或分号分开。


```cpp

__asm__　__volatile__("Instruction List" : Output : Input : Clobber/Modify);

例如： 在ARM系统结构上关闭中断的操做

int disable_interrupts (void)
{
    unsigned long old,temp;
    __asm__ __volatile__("mrs %0, cpsr\n"
    "orr %1, %0, #0x80\n"
    "msr cpsr_c, %1"
    : "=r" (old), "=r" (temp)
    :
    : "memory");
    return (old & 0x80) == 0;
}
```

```cpp
三. __volatile__

__volatile__是GCC 关键字volatile 的宏定义

#define __volatile__ volatile

__volatile__或volatile 是可选的。若是用了它，则是向GCC 声明不容许对该内联汇编优化，不然当使用了优化选项(-O)进行编译时，GCC 将会根据本身的判断决定是否将这个内联汇编表达式中的指令优化掉。

四、 Output

Output 用来指定当前内联汇编语句的输出

例如：从arm协处理器p15中读出C1值

static unsigned long read_p15_c1 (void)
{
    unsigned long value;
    __asm__ __volatile__(
    "mrc p15, 0, %0, c1, c0, 0 @ read control reg\n"
    : "=r" (value) @编译器选择一个R*寄存器
    :
    : "memory");
    #ifdef MMU_DEBUG
    printf ("p15/c1 is = %08lx\n", value);
    #endif
    return value;
}


五、 Input

Input 域的内容用来指定当前内联汇编语句的输入Output和Input中，格式为形如“constraint”(variable)的列表（逗号分隔)

例如：向arm协处理器p15中写入C1值

static void write_p15_c1 (unsigned long value)
{
    #ifdef MMU_DEBUG
    printf ("write %08lx to p15/c1\n", value);
    #endif
    __asm__ __volatile__(
    "mcr p15, 0, %0, c1, c0, 0 @ write it back\n"
    :
    : "r" (value) @编译器选择一个R*寄存器
    : "memory");
    read_p15_c1 ();
}

6.、Clobber/Modify

有时候，你想通知GCC当前内联汇编语句可能会对某些寄存器或内存进行修改，但愿GCC在编译时可以将这一点考虑进去。
那么你就能够在Clobber/Modify域声明这些寄存器或内存。这种状况通常发生在一个寄存器出如今"Instruction List"，
但却不是由Input/Output操做表达式所指定的，也不是在一些Input/Output操做表达式使用"r"约束时由GCC 为其选择的，
同时此寄存器被"Instruction List"中的指令修改，而这个寄存器只是供当前内联汇编临时使用的状况。

例如：

__asm__ ("mov R0, #0x34" : : : "R0");

寄存器R0出如今"Instruction List中"，而且被mov指令修改，但却未被任何Input/Output操做表达式指定，因此你须要在Clobber/Modify域指定"R0"，以让GCC知道这一点。

```

****



## tsc
[再论 Time stamp counter](https://www.cnblogs.com/ralphjzhang/archive/2012/01/09/2317463.html)


`在很多年以前，`rdtsc 指令是在 x86 平台作 micro benchmark 的不二选择，它可以用很小的代价（基本上在几十个 CPU 周期）获得时间戳计数器 (time stamp counter) 的值，用来计算小代码段的性能是比较方便的。

`然而来了多核时代，以及变频时代，由于 CPU 核心的主频不是恒定的了`，time stamp counter 的值不代表时间了；同时，`又由于 CPU 有多个核心`，这些核心之间的 time stamp counter` 不一定是同步的`，所以当进程在核心之间迁移后，rdtsc 的结果就未必有意义。这一点在陈硕的文章里说得很清楚：http://blog.csdn.net/solstice/article/details/5196544

话说时光荏苒，又过了两年，两年前的结论，到了今天又未必合适。简单点说，`在较新的处理器中实现了恒定时间戳计数器 (Invariant TSC)`，在 Intel 的处理器手册 (http://www.intel.com/content/dam/doc/manual/64-ia-32-architectures-software-developer-vol-3b-part-2-manual.pdf) 里的17.12.1节是这么说的：
```
The time stamp counter in newer processors may support an enhancement, referred to as invariant TSC. Processor’s support for
 invariant TSC is indicated by CPUID.80000007H:EDX[8]. 

The invariant TSC will run at a constant rate in all ACPI P-, C-. and T-states. This is the architectural behavior moving 
forward. On processors with invariant TSC support, the OS may use the TSC for wall clock timer services (instead of ACPI or HPET
 timers). TSC reads are much more efficient and do not incur the overhead associated with a ring transition or access to a 
 platform resource.
```
上文的 newer processors 实际上是说 Nehalem 以及之后的处理器，在 AMD 那边，是 Bacelona 之后的。`在这些处理器上，可以大胆使用 rdtsc，不用担心变频，不用担心多核，time stamp counter 以恒定速率增加`，嗯，就是这样。

但是，还是没有那么简单，要做 micro benchmark ，除了 TSC 要准，`还要顾及 CPU 的乱序执行`，尤其是如果被测的代码段较小，乱序执行可能让你的测试变得完全没意义。解决这个一般是“先同步，后计时”，在 wikipedia 上的一段代码就用 cpuid 指令来同步 (http://en.wikipedia.org/wiki/Time_Stamp_Counter)。但是 cpuid 指令本身的开销相当不小，至少在 rdtsc 的3倍以上，而且自身的开销并不稳定，结果是为了同步，引入了更多不确定性，不太值得。

另外一个办法是用 memory barrier，在 Intel CPU 上，指令 lfence 可以“保护” rdtsc，起到和上面 cpuid 指令同样的作用，但是开销小得多。在 rdtsc 指令前后都加上一个 lfence ，就可以比较精确的控制 rdtsc 的行为，不让乱序执行影响时间戳的获取。在 AMD CPU 上，需要使用指令 mfence ，开销稍高一些，但仍然比 cpuid 要低。只是这样，就要对 Intel 和 AMD 写不同的代码，比较麻烦。


## FIO-ESM
### 1、创建case方法

#### 模式位置：

/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0
```C++
[fio_climate_model@ln132%bscc-a6 fioesm2_0]$ ls -l
total 32
drwxrwxr-x  3 fio_climate_model fio_climate_model 4096 Aug 17 09:58 archive
-rw-rw-r--  1 fio_climate_model fio_climate_model 2755 Aug 16 22:17 buildcast.txt
drwxrwxr-x  6 fio_climate_model fio_climate_model 4096 Jul 27 21:12 case
drwxr-xr-x 13 fio_climate_model fio_climate_model 4096 Jun 14  2018 models
-rw-rw-r--  1 fio_climate_model fio_climate_model  465 Jul 13 10:39 README.txt
drwxrwxr-x 10 fio_climate_model fio_climate_model 4096 Aug 17 09:14 run
drwxr-xr-x  5 fio_climate_model fio_climate_model 4096 Jul 21 15:11 scripts
drwxr-xr-x  4 fio_climate_model fio_climate_model 4096 Jun 14  2018 tools

```

#### 创建case：
./scripts/create_newcase -case `./case/esmtest` -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml
```参数介绍：
-case case的存储位置
-res 分辨率
-compset 选择compset个例，具有一定的命名规则，也就是定义模块。
-mach 机器要求，例如-mach bscc-a6 会自动读取在
/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts/ccsm_utils/Machines
路径下的env_mach_specific.bscc-a6, mkbatch.bscc-a6文件。其中env_mach_*会挂载环境，mkbatch.* 会生成配置项目。
```

=============================================================================================================================

```c
For example:
在/public1/home/fio_climate_model/liuyao/wys下，创建 case: esmtest_2022_0817


./scripts/create_newcase -case /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817 -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml

Note：如果要创建的case的文件夹存在，即使此文件夹是空的，也是会创建失败

[fio_climate_model@ln132%bscc-a6 fioesm2_0]$ ./scripts/create_newcase -case /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817 -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml
Caseroot directory /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817 already exists

=============================================================================================================================

[fio_climate_model@ln132%bscc-a6 fioesm2_0]$ ./scripts/create_newcase -case /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817 -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts/ccsm_utils/Case.template/ConfigCase.pm line 448.
-------------------------------------------------------------------------------
For a list of potential issues in the current tag, please point your web browser to:
https://svn-ccsm-models.cgd.ucar.edu/cesm1/known_problems/
-------------------------------------------------------------------------------
 grid longname is f09_g16 
Component set: longname (shortname) (alias) 
  1850_CAM5%PM_CLM40%CN_CICE_POP2%ECO_RTM_SGLC_SWAV_BGC%BPRP (B_1850_CAM5_PM_BGC-BPRP) (B1850C5PMBPRP) 
Component set Description: 
  CAM: CLM: RTM: CICE: POP2: SGLC: SWAV: pre-industrial: cam5 physics: CAM prescribed modal aerosols: clm4.0 physics: clm4.0 cn: prognostic cice: POP2 default: POP2/Ecosystem: BGC CO2=prog, rad CO2=prog: ECO in POP: 
Grid: 
  a%0.9x1.25_l%0.9x1.25_oi%gx1v6_r%r05_m%gx1v6_g%null_w%null (0.9x1.25_gx1v6) 
  ATM_GRID = 0.9x1.25  NX_ATM=288 NY_ATM=192 
  LND_GRID = 0.9x1.25  NX_LND=288 NX_LND=192 
  ICE_GRID = gx1v6  NX_ICE=320 NX_ICE=384 
  OCN_GRID = gx1v6  NX_OCN=320 NX_OCN=384 
  ROF_GRID = r05  NX_ROF=720 NX_ROF=360 
  GLC_GRID = 0.9x1.25  NX_GLC=288 NX_GLC=192 
  WAV_GRID = null  NX_WAV=0 NX_WAV=0 
Grid Description: 
  null is no grid: 0.9x1.25 is FV 1-deg grid: gx1v6 is Greenland pole v6 1-deg grid: r05 is 1/2 degree river routing grid: 
Non-Default Options: 
  ATM_NCPL: 48 
  BUDGETS: TRUE 
  CAM_CONFIG_OPTS: -phys cam5 -chem none -co2_cycle -microphys mg1.5 
  CAM_DYCORE: fv 
  CAM_NML_USE_CASE: 1850_cam5_pm_bgc_fioesm 
  CCSM_BGC: CO2C 
  CCSM_CCOST: 1 
  CCSM_CO2_PPMV: 284.32 
  CICE_MODE: prognostic 
  CICE_NAMELIST_OPTS: cam5=.true. 
  CLM_CO2_TYPE: prognostic 
  CLM_CONFIG_OPTS: -phys clm4_0 -bgc cn 
  CLM_NML_USE_CASE: 1850_bgcfioesm_control 
  COMP_ATM: cam 
  COMP_GLC: sglc 
  COMP_ICE: cice 
  COMP_LND: clm 
  COMP_OCN: pop2 
  COMP_ROF: rtm 
  COMP_WAV: swav 
  CPL_ALBAV: false 
  CPL_EPBAL: off 
  GET_REFCASE: TRUE 
  OCN_CHL_TYPE: prognostic 
  OCN_CO2_TYPE: prognostic 
  OCN_COUPLING: full 
  OCN_NCPL: 8 
  OCN_TIGHT_COUPLING: FALSE 
  OCN_TRACER_MODULES:  iage ecosys 
  REST_N: 12 
  REST_OPTION: nmonths 
  ROF_NCPL: 8 
  RTM_BLDNML_OPTS: -simyr 1850 
  RUN_REFCASE: esmspinup.1234.1 
  RUN_REFDATE: 1001-01-01 
  RUN_STARTDATE: 0001-01-01 
  RUN_TYPE: hybrid 
  SCIENCE_SUPPORT: NO 
  STOP_N: 12000 
  STOP_OPTION: nmonths 

Creating /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817 
Created /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/env_case.xml 
Created /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/env_mach_pes.xml 
Created /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/env_build.xml 
Created /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/env_run.xml 
Locking file /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/env_case.xml 
Successfully created the case for bscc-a6




=============================================================================================================================
[fio_climate_model@ln132%bscc-a6 wys]$ cd esmtest_2022_0817/
[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ls
archive_metadata.sh  check_case              env_build.xml      env_run.xml                    LockedFiles             SourceMods
Buildconf            check_input_data        env_case.xml       esmtest_2022_0817.build        preview_namelists       Tools
CaseStatus           create_production_test  env_mach_pes.xml   esmtest_2022_0817.clean_build  README.case             xmlchange
cesm_setup           Depends.intel           env_mach_specific  esmtest_2022_0817.submit       README.science_support  xmlquery

[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817_creat_case_step1]$ ls | wc
     24      24     371

```

### 2、配置case
`修改核数：`在env_mach_pes.xml 中进行配置，一般修改NTASKS_* 的内容，总核数定义为 各个 {NTASKS_名称+ROOTPE_名称} 中最大的那个。

`修改其他配置`：env_run.xml 模式重启、动力方案设置

```c
./cesm_setup

=============================================================================================================================
[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ./cesm_setup 
Use of qw(...) as parentheses is deprecated at ./cesm_setup line 252.
Creating Macros file for bscc-a6
/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts/ccsm_utils/Machines/config_compilers.xml intel bscc-a6
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Creating batch script esmtest_2022_0817.run 
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Locking file env_mach_pes.xml 
Creating user_nl_xxx files for components and cpl
Running preview_namelist script 
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/drv/bld/build-namelist line 781.
 infile is /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/cplconf/cesm_namelist 
CAM writing dry deposition namelist to drv_flds_in 
CAM writing namelist to atm_in 
CLM configure done.
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl1 with val 
'TOTVEGC','LITTERC','GPP','AR','NPP','HR','NBP','COL_FIRE_CLOSS','LEAFC','LEAFC_STORAGE','LEAFC_XFER','FROOTC','FROOTC_STORAGE','FROOTC_XFER','AGNPP','BGNPP','CWDC','SOIL1C','SOIL2C','SOIL3C','GR','MR','NEP','WOODC'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl2 with val 
'SNOWDP','TLAI','SOILLIQ','SOILICE','TSOI','QRUNOFF','TSA','WT','SOILWATER_10CM','SNOWLIQ','SNOWICE'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl3 with val 
'TSA:I','SOILWATER_10CM:I','QRUNOFF:A','GPP','AR','HR'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_mfilt with val 1,30,240 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_nhtfrq with val 0,-24,-3 
CLM adding use_case 1850_bgcfioesm_control defaults for var sim_year with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var sim_year_range with val constant 
CLM adding use_case 1850_bgcfioesm_control defaults for var stream_year_first_ndep with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var stream_year_last_ndep with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var use_case_desc with val Conditions to simulate 1850 land-use 
CICE configure done.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Getting init_ts_file_fmt from /public1/home/fio_climate_model/FIO-ESM/inputdata/ccsm4_init/esmspinup.1234.1/1001-01-01/rpointer.ocn.restart
POP2 build-namelist: ocn_grid is gx1v6 
POP2 build-namelist: ocn_tracer_modules are  iage ecosys 
See ./CaseDoc for component namelists 
If an old case build already exists, might want to run esmtest_2022_0817.clean_build before building


=============================================================================================================================
[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ls
archive_metadata.sh  check_case              env_case.xml       esmtest_2022_0817.build        Macros                  Tools         user_nl_pop2
Buildconf            check_input_data        env_derived        esmtest_2022_0817.clean_build  preview_namelists       user_nl_cam   user_nl_rtm
CaseDocs             create_production_test  env_mach_pes.xml   esmtest_2022_0817.run          README.case             user_nl_cice  xmlchange
CaseStatus           Depends.intel           env_mach_specific  esmtest_2022_0817.submit       README.science_support  user_nl_clm   xmlquery
cesm_setup           env_build.xml           env_run.xml        LockedFiles                    SourceMods              user_nl_cpl


[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817_setup_step2]$ ls | wc
     34      34     495


```


### 3、构建case

```c
./&{your_case_name}.build

Note:注：如果修改了xml，需要重新执行

For example:
./esmtest_2022_0817.build


[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ./esmtest_2022_0817.build 
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
-------------------------------------------------------------------------
 CESM BUILDNML SCRIPT STARTING
 - To prestage restarts, untar a restart.tar file into /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/run
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models/drv/bld/build-namelist line 781.
 infile is /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/cplconf/cesm_namelist 
CAM writing dry deposition namelist to drv_flds_in 
CAM writing namelist to atm_in 
CLM configure done.
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl1 with val 
'TOTVEGC','LITTERC','GPP','AR','NPP','HR','NBP','COL_FIRE_CLOSS','LEAFC','LEAFC_STORAGE','LEAFC_XFER','FROOTC','FROOTC_STORAGE','FROOTC_XFER','AGNPP','BGNPP','CWDC','SOIL1C','SOIL2C','SOIL3C','GR','MR','NEP','WOODC'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl2 with val 
'SNOWDP','TLAI','SOILLIQ','SOILICE','TSOI','QRUNOFF','TSA','WT','SOILWATER_10CM','SNOWLIQ','SNOWICE'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_fincl3 with val 
'TSA:I','SOILWATER_10CM:I','QRUNOFF:A','GPP','AR','HR'
 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_mfilt with val 1,30,240 
CLM adding use_case 1850_bgcfioesm_control defaults for var hist_nhtfrq with val 0,-24,-3 
CLM adding use_case 1850_bgcfioesm_control defaults for var sim_year with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var sim_year_range with val constant 
CLM adding use_case 1850_bgcfioesm_control defaults for var stream_year_first_ndep with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var stream_year_last_ndep with val 1850 
CLM adding use_case 1850_bgcfioesm_control defaults for var use_case_desc with val Conditions to simulate 1850 land-use 
CICE configure done.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Getting init_ts_file_fmt from /public1/home/fio_climate_model/FIO-ESM/inputdata/ccsm4_init/esmspinup.1234.1/1001-01-01/rpointer.ocn.restart
POP2 build-namelist: ocn_grid is gx1v6 
POP2 build-namelist: ocn_tracer_modules are  iage ecosys 
 CESM BUILDNML SCRIPT HAS FINISHED SUCCESSFULLY
-------------------------------------------------------------------------
-------------------------------------------------------------------------
 CESM PRESTAGE SCRIPT STARTING
 - Case input data directory, DIN_LOC_ROOT, is /public1/home/fio_climate_model/FIO-ESM/inputdata
 - Checking the existence of input datasets in DIN_LOC_ROOT
 
The following files were not found, this is informational only
Input Data List Files Found:
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/cam.input_data_list
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/cice.input_data_list
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/cpl.input_data_list
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/clm.input_data_list
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/rtm.input_data_list
/public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Buildconf/pop2.input_data_list
File status unknown: esmspinup.1234.1.cam.i.1001-01-01-00000.nc 
File status unknown: esmspinup.1234.1.clm2.r.1001-01-01-00000.nc 
File status unknown: esmspinup.1234.1.rtm.r.1001-01-01-00000.nc 
 
 - Prestaging REFCASE (ccsm4_init/esmspinup.1234.1/1001-01-01) to /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/run
 CESM PRESTAGE SCRIPT HAS FINISHED SUCCESSFULLY
-------------------------------------------------------------------------
-------------------------------------------------------------------------
 CESM BUILDEXE SCRIPT STARTING
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
 COMPILER is intel
 - Build Libraries: mct gptl pio csm_share 
Wed Aug 17 21:27:06 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/mct/mct.bldlog.220817-212701
Wed Aug 17 21:27:48 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/gptl/gptl.bldlog.220817-212701
Wed Aug 17 21:27:51 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/pio/pio.bldlog.220817-212701
Wed Aug 17 21:28:31 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/csm_share/csm_share.bldlog.220817-212701
Wed Aug 17 21:28:46 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/atm.bldlog.220817-212701
Wed Aug 17 21:29:37 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/lnd.bldlog.220817-212701
Wed Aug 17 21:31:35 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/ice.bldlog.220817-212701


Wed Aug 17 21:36:20 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/ocn.bldlog.220817-212701
Wed Aug 17 21:37:57 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/glc.bldlog.220817-212701
Wed Aug 17 21:37:57 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/wav.bldlog.220817-212701
Wed Aug 17 21:37:57 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/rof.bldlog.220817-212701
Wed Aug 17 21:38:07 CST 2022 /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817/bld/cesm.bldlog.220817-212701
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
Use of qw(...) as parentheses is deprecated at /public1/home/fio_climate_model/liuyao/wys/esmtest_2022_0817/Tools/ConfigCase.pm line 448.
 - Locking file env_build.xml
 CESM BUILDEXE SCRIPT HAS FINISHED SUCCESSFULLY
-------------------------------------------------------------------------

[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ls
archive_metadata.sh  check_case              env_case.xml       esmtest_2022_0817.build        logs                    SourceMods    user_nl_cpl
Buildconf            check_input_data        env_derived        esmtest_2022_0817.clean_build  Macros                  Tools         user_nl_pop2
CaseDocs             create_production_test  env_mach_pes.xml   esmtest_2022_0817.run          preview_namelists       user_nl_cam   user_nl_rtm
CaseStatus           Depends.intel           env_mach_specific  esmtest_2022_0817.submit       README.case             user_nl_cice  xmlchange
cesm_setup           env_build.xml           env_run.xml        LockedFiles                    README.science_support  user_nl_clm   xmlquery

[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ls | wc
     35      35     500

=============================================================================================================================

模式输出位置：

/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/esmtest_2022_0817

[fio_climate_model@ln132%bscc-a6 esmtest_2022_0817]$ ls
bld  run


[fio_climate_model@ln132%bscc-a6 run]$ ls
atm_in                                       esmspinup.1234.1.clm2.rh0.1001-01-01-00000.nc  gx1v6_history_contents    lnd_modelio.nml
atm_modelio.nml                              esmspinup.1234.1.clm2.rh1.1001-01-01-00000.nc  gx1v6_movie_contents      ocn_modelio.nml
cpl_modelio.nml                              esmspinup.1234.1.clm2.rh2.1001-01-01-00000.nc  gx1v6_overflow            pop2_in
drv_flds_in                                  esmspinup.1234.1.cpl.r.1001-01-01-00000.nc     gx1v6_region_ids          rof_in
drv_in                                       esmspinup.1234.1.pop.r.1001-01-01-00000.nc     gx1v6_tavg_contents       rof_modelio.nml
esmspinup.1234.1.cam.i.1001-01-01-00000.nc   esmspinup.1234.1.pop.ro.1001-01-01-00000       gx1v6_transport_contents  rpointer.drv
esmspinup.1234.1.cam.r.1001-01-01-00000.nc   esmspinup.1234.1.rtm.r.1001-01-01-00000.nc     gx1v6_vert_grid           rpointer.ocn.ovf
esmspinup.1234.1.cam.rs.1001-01-01-00000.nc  esmspinup.1234.1.rtm.rh0.1001-01-01-00000.nc   ice_in                    rpointer.ocn.restart
esmspinup.1234.1.cice.r.1001-01-01-00000.nc  glc_modelio.nml                                ice_modelio.nml           seq_maps.rc
esmspinup.1234.1.clm2.r.1001-01-01-00000.nc  gx1v6_depth_accel
```

### 4、提交任务
执行./esmtest.submit

模式输出位置/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/run/case名称,可在env_run.xml 中配置。

## 构建过程分析


bash 脚本的语法很多没有见过？

这周完善编译过程详细文档。。



[目录](#目录)