gcc_finstrument_functions
===========================



## 目录
* [__volatile__](#__volatile__)
* [标题](#标题)
* [文本](#文本)
    * 普通文本
    * 单行文本
    * 多行文本
    * 文字高亮
    * 换行
    * 斜体
    * 粗体
    * 删除线
* [图片](#图片)
    * 来源于网络的图片
    * GitHub仓库中的图片
* [链接](#链接)
    * 文字超链接
        *  链接外部URL
        *  链接本仓库里的URL
    *  锚点
    * [图片链接](#图片链接)
* [列表](#列表)
    * 无序列表
    * 有序列表
    * 复选框列表
* [块引用](#块引用)
* [代码高亮](#代码高亮)
* [表格](#表格)
* [表情](#表情)
* [diff语法](#diff语法)
* [常用HTML语法](#常用HTML语法)
    * [折叠](#折叠)
    * [居中](#居中)
* [其他](#其他)
    * [徽章](#徽章)
    * [star历史](#star历史






`微基准测试:`   micro benchmark

## __volatile__



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

有时候，你想通知GCC当前内联汇编语句可能会对某些寄存器或内存进行修改，但愿GCC在编译时可以将这一点考虑进去。那么你就能够在Clobber/Modify域声明这些寄存器或内存。这种状况通常发生在一个寄存器出如今"Instruction List"，但却不是由Input/Output操做表达式所指定的，也不是在一些Input/Output操做表达式使用"r"约束时由GCC 为其选择的，同时此寄存器被"Instruction List"中的指令修改，而这个寄存器只是供当前内联汇编临时使用的状况。

例如：

__asm__ ("mov R0, #0x34" : : : "R0");

寄存器R0出如今"Instruction List中"，而且被mov指令修改，但却未被任何Input/Output操做表达式指定，因此你须要在Clobber/Modify域指定"R0"，以让GCC知道这一点。

```

****
