#include "hash_table.h"
#include "mem_pool.h"   // 操操操操操操操操， 不包含这个文件，在静态库的场景会crash
#include <stdio.h>
#include <limits.h>

#include "stack.h"
#include "perf_counter.h"
#include "get_pid_time.h"

HASH_MAP hashmap;
bool trace_flag = false;
ULL depth = 0;
int depth_is_zero_num = 0;
ULL max_call_depth = 0;

Stack time_stk;
Stack func_addr_stk;

// 这个定义实在动态库
// 然后在 静态库里面extern，就可以改变这个值了？？？、好奇怪（按道理应该是不行的啊，但是效果是可以的）
// 难道确实是有这个优化嘛
int __profile__rank = INT_MAX;        //记录当前处在哪个rank中（多进程）
int __profile_common_size = INT_MAX;  // record  mpi size

ULL call_start_probe_times = 0;
ULL call_end_probe_times = 0;

void get_basic_info()
{
    if (depth == 0) {
        depth_is_zero_num++;
    }
    if (depth > max_call_depth) {
        max_call_depth = depth;
    }
}
    
void __attribute__((constructor)) traceBegin(void); // 这东西不太适合对C++插桩
// 因为，这个函数并不是限制性的，C++有可能是限制属性alloc，这个也是会被插桩的
// 对于C的目标文件是先执行的

// 所以为了统一起见，还是不要用这个东西了
// 可以使用全局变量，depth
// depth == 0
// 在__cyg_profile_func_enter()中表示刚开始
// 在__cyg_profile_func_exit() 表示结束

void __attribute__((destructor)) traceEnd(void);

void __cyg_profile_func_enter(void *func, void *caller);

void __cyg_profile_func_exit(void *func, void *caller);

 
// 这样的操作，就是只对constructor destructor之间的代码采样
void __attribute__((constructor, no_instrument_function)) traceBegin(void) {
    trace_flag = true;
    printf("__traceBegin__\n");
    hash_map_init(&hashmap);
    stack_init(&time_stk);
    stack_init(&func_addr_stk);
}

const char* outfile_path = "./out/";
const char* outfile_postfix = "factrace.txt";

void __attribute__((destructor, no_instrument_function)) traceEnd(void) {
    trace_flag = false;

    if (__profile__rank == INT_MAX || __profile__rank == 0) {
        char outfilename[BUF_SIZE] = {0};
        get_file_name(outfilename, outfile_path, outfile_postfix);
        save_hash_map_node_to_file(&hashmap, outfilename);
    
        printf("*************************TraceEnd  Basic Info*************************\n");
        hash_map_show(&hashmap);
        // print_hash_map_node(&hashmap);
        printf("[basic info]: depth_is_zero_num: \t%d\n", depth_is_zero_num);
        printf("[basic info]: max_call_depth: \t\t%lld\n", max_call_depth);
        printf("[basic info]: call_start_probe_times: \t%lld\n", call_start_probe_times);
        printf("[basic info]: call_end_probe_times: \t%lld\n", call_end_probe_times);
        printf("[basic info]: mpi rank: \t\t%d\n", __profile__rank);
        printf("[basic info]: mpi common size: \t\t%d\n", __profile_common_size);
        printf("[basic info]: sampling out file: \t%s\n", outfilename);
        printf("[basic info]: __traceEnd__\n");
        printf("***********************************************************************\n");
    }

    hash_map_destory(&hashmap);
}

// 在探针里面的变量 ，用全局变量，降低访存开销， __cyg_profile_func_enter
NODE_Ptr nodeptr = NULL; // 使用全局变量，降低访存开销
ULL print_flag = 1;
NODE tmp;



ULL shell_start_time = 0;
ULL shell_end_time = 0;
ULL self_start_time = 0;
ULL self_end_time = 0;

// 自身地址肯定是准的
// caller 是 指令内部，无法解析
bool first_call_cyg_enter = true;
// ULL god_addr = 0;
ULL self_addr = 0;
ULL fater_addr = 0;

void __cyg_profile_func_enter(void *func, void *caller) {
    if (trace_flag == false) return;

    //  自身地址肯定是准的,可以用自己实现的map解析出来，（caller不行，caller使用addr2line也许可以解析出来）
    // if (first_call_cyg_enter == true) {
    //     stack_push(&func_addr_stk, god_addr);
    //     stack_push(&func_addr_stk, (ULL)func);
    //     first_call_cyg_enter = false;
    // }
    stack_push(&func_addr_stk, (ULL)func);

    shell_start_time = perf_counter();
    stack_push(&time_stk, shell_start_time);

    get_basic_info();
    // if (depth == 0) {
    //     __traceBegin();
    // }
    // printf("depth:%lld\n",depth);
    depth++;
    call_start_probe_times++;
    // if (print_flag % 100000 == 0) hash_map_show(&hashmap);
    // print_flag++;
    // printf("__cyg_profile_func_enter\n");
    // printf("## enter %p\n", func);
    // printf("## enter %lld\n", (ULL)func);


    self_start_time = perf_counter();
    stack_push(&time_stk, shell_start_time);
   
}

void __cyg_profile_func_exit(void *func, void *caller) {
    if (trace_flag == false) return;
    // printf("__cyg_profile_func_exit\n");

    self_end_time = perf_counter();

    // 取时间栈里面的时间
    self_start_time  = get_stack_top_data(&time_stk);
    stack_pop(&time_stk);
    shell_start_time = get_stack_top_data(&time_stk);
    stack_pop(&time_stk);

    // 取函数地址栈 （self_addr, fater_addr）
    self_addr = get_stack_top_data(&func_addr_stk);     // 取自己的函数地址；（栈顶地址，就是自身地址）
    stack_pop(&func_addr_stk);
    if(is_stack_empty(&func_addr_stk) == true) {        // 取父函数地址；（如果此时函数栈空，说明函数栈里面没有他父亲函数的地址，我们使用caller作为父函数地址）
        fater_addr = (ULL)caller;
    } else {
        fater_addr = get_stack_top_data(&func_addr_stk);
    }

    // 构造父子调用关系节点，查找是否已经插入hashmap中，如果已经插入，更新节点的值，如果没有插入，插入新节点
    make_node(&tmp, self_addr, fater_addr, 1, 666666, 666666);
    // make_node(&tmp, (ULL)func, (ULL)caller, 1, 456456, 789798);
    nodeptr = hash_map_find_key(&hashmap, &tmp);
    if(nodeptr != NULL) {
        // update node
        // update_node(nodeptr, &tmp);
        nodeptr->val.times++;
        nodeptr->val.acctime += self_end_time - self_start_time;
        nodeptr->val.sheltime += perf_counter() - shell_start_time;

    } else {
        nodeptr = get_node(&hashmap.nodeMemPool);
        make_node(nodeptr, self_addr, fater_addr, 1, self_end_time - self_start_time, perf_counter() - shell_start_time);
        hash_map_insert(&hashmap, nodeptr);
    }

    depth--;
    call_end_probe_times++;


}