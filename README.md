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