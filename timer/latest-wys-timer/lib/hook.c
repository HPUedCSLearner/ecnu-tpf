#include "hash_table.h"
#include "mem_pool.h"   // 操操操操操操操操， 不包含这个文件，在静态库的场景会crash
#include <stdio.h>

HASH_MAP hashmap;
    
void __attribute__((constructor)) traceBegin(void);

void __attribute__((destructor)) traceEnd(void);

void __cyg_profile_func_enter(void *func, void *caller);

void __cyg_profile_func_exit(void *func, void *caller);



void __attribute__((constructor)) traceBegin(void) {
    printf("__traceBegin__\n");
    hash_map_init(&hashmap);
}

void __attribute__((destructor)) traceEnd(void) {
    printf("__traceEnd__\n");
    hash_map_show(&hashmap);
    hash_map_destory(&hashmap);
}

void __cyg_profile_func_enter(void *func, void *caller) {
    printf("__cyg_profile_func_enter\n");
    printf("## enter %p\n", func);
    printf("## enter %lld\n", (ULL)func);

    NODE_Ptr nodeptr = get_node(&hashmap.nodeMemPool);
    make_node(nodeptr, (ULL)func, (ULL)caller, 1, 456456, 789798);
    show_node(nodeptr);
    hash_map_insert(&hashmap, nodeptr);
}

void __cyg_profile_func_exit(void *func, void *caller) {
    printf("__cyg_profile_func_exit\n");
}