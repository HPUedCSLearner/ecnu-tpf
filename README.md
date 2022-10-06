【金山文档】

 [xxx碎片化学习](https://kdocs.cn/l/cpnRGw8Ou4go)



【Git】

https://github.com/HPUedCSLearner


【常用链接】

[c.biancheng.net](http://c.biancheng.net/)

[41yun](https://www.41yun.com/servicedetail?id=8786)

【HPC】

[sig小组文档](https://hpc-cool.feishu.cn/docx/doxcnTlFDwRGWGRitRboqPhlNAe)

[并行学习流水线](https://www.kdocs.cn/l/crR2o6G6dWZg)

[CASE](https://www.cesm.ucar.edu/models/cesm1.2/)

[性能建模使用说明书](https://hpc-cool.feishu.cn/docs/doccnOhEVJiZ5hiagB0rOnSYorf)

[如何快速地在每个函数入口处加入相同的语句？](https://www.zhihu.com/question/56132218)

[GCC的__attribute__ ((constructor))和__attribute__ ((destructor))](https://www.cnblogs.com/dylancao/p/9293447.html)

注意探针里要的里函数，要加上 __attribute__((no_instrument_function)) 否则，无法运行

[实现C调用C++库，如封装C++面向对象的接口给C语言用](https://blog.csdn.net/zhizhengguan/article/details/119674564)
--> 对上面上面一行做出解释， 因为 我加 编译选项 -finstrument-functions 相当于给全局加入了，所以都插装;
--> 所以又有一个思路：编译一个计时探针的库，供模式使用（给需要加入-finstrument-functions 的加入，不需要加入的不加入）
    (因为，之前做实验的时候，也发现，只有在源码后加入这个编译选项，才会插入其中)（当时使用makefile，会给不同文件 加入 不同编译选项）


[[内存问题分析,写的比较好]](https://zhuanlan.zhihu.com/p/399999297)

[c C++ Fortran 混编实例1](https://www.cnblogs.com/snake553/p/6962386.html)

[c C++ Fortran 混编实例2](https://blog.csdn.net/weixin_43580880/article/details/107225688)

##### 实用链接
[字符串补0的一个简单方法](https://blog.csdn.net/weixin_44539392/article/details/107294483?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-107294483-blog-82466210.pc_relevant_3mothn_strategy_and_data_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-107294483-blog-82466210.pc_relevant_3mothn_strategy_and_data_recovery&utm_relevant_index=2)

```c
return ("00000000" + retV).substr(retV.length());
<==>
return ("00000000" + retV).substr(8 - (8 - retV.length()));
```

###### 混合编程
* python 调用 C++
* C 调用 C++
* Fortran C++ 互调




gcc test.c  hash_func.cpp -lstdc++

##### 问题记录:
1、插装后，采样信息文件多进程环境下的写入问题

2、mpi库找不到的问题
/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi
并行A6上用的MPI库

问题解决:

export PATH=/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/bin:$PATH


常用路径:
/public1/home/fio_climate_model/zyp/fioesm_cases/B_1024_p1_bk/timing_probe4/libprobeso

-lfinstrument

常用字符串:
-finstrument-functions
##### 奇怪的现象:
1、模式插装后，第一次跑起来，可以产生多个trace文件，但是，第二次跑起来的时候，就没有trace文件
2、
###### 已解决的问题记录:
1、GCC插装编译选项问题，以及静态链接库的问题
2、变频下，使用tsc作为计时条件的可行性