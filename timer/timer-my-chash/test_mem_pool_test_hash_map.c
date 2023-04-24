#include "mem_pool.h"

#include "hash_table.h"
#include "stack.h"

#include <assert.h>
#include <stdio.h>


#include "get_pid_time.h"

void test()
{
    MEM_POOL mem_pool;
    mem_pool_init(&mem_pool);
    mem_pool_show_profile(&mem_pool);


    NODE_Ptr nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    nodeptr = get_node(&mem_pool);
    mem_pool_show_profile(&mem_pool);

    mem_poll_detory(&mem_pool);

}



void test1()
{
    MEM_POOL mem_pool;
    mem_pool_init(&mem_pool);
    mem_pool_show_profile(&mem_pool);


    NODE_Ptr nodeptr;
    for (int i = 0; i < 100000; ++i) {
        nodeptr = get_node(&mem_pool);
    }

    mem_pool_show_profile(&mem_pool);

    mem_poll_detory(&mem_pool);

}

void testHashMap()
{
    HASH_MAP hashmap;
    hash_map_init(&hashmap);

    NODE_Ptr nodeptr1 = get_node(&hashmap.nodeMemPool);
    make_node(nodeptr1, 0x0101010101010101, 0xab10101a, 1, 456456, 789798);
    assert(NULL == hash_map_find_key(&hashmap, nodeptr1));

    hash_map_insert(&hashmap, nodeptr1);
    assert(NULL != hash_map_find_key(&hashmap, nodeptr1));

    NODE_Ptr nodeptr2 = get_node(&hashmap.nodeMemPool);
    make_node(nodeptr2, 0x0101010101010101, 0xab10101a, 3, 1, 1);
    hash_map_insert(&hashmap, nodeptr2);

    show_node(hash_map_find_key(&hashmap, nodeptr1));

    // 下面的测试，可以测出碰撞, 从而调整hash函数，以及hash表size
    int thredhold = 100000;
    for (int i = 0; i < thredhold; ++i) {
        NODE_Ptr nodeptr = get_node(&hashmap.nodeMemPool);
        make_node(nodeptr, 0x0101010101010101 + i * i , 0xab10101a + i * 2 , 3, 1, 1);
        hash_map_insert(&hashmap, nodeptr);
    }  

    hash_map_show(&hashmap);
    hash_map_destory(&hashmap);
}

void test_stack()
{
    Stack stk;
    stack_init(&stk);
    get_stack_top_data(&stk);

    stack_push(&stk, 1);
    assert(get_stack_top_ptr(&stk) == 0);

    stack_push(&stk, 2);
    stack_push(&stk, 3);
    stack_push(&stk, 4);
    assert(get_stack_top_ptr(&stk) == 3);


    stack_pop(&stk);
    stack_pop(&stk);
    assert(get_stack_top_ptr(&stk) == 1);
    assert(get_stack_top_data(&stk) == 2);
    assert(is_stack_empty(&stk) == false);
    assert(is_stack_full(&stk) == false);

    assert(is_stack_full(&stk) == false);

    stack_push(&stk, 3);
    stack_push(&stk, 4);
    stack_push(&stk, 3);
    stack_push(&stk, 4);
    stack_push(&stk, 3);
    stack_push(&stk, 4);
    stack_push(&stk, 3);
    stack_push(&stk, 4);
    stack_push(&stk, 4);
    stack_push(&stk, 4);
    stack_push(&stk, 4);
    assert(get_stack_top_ptr(&stk) == DEFAULT_STACK_SIZE - 1);
    assert(get_stack_top_data(&stk) == 4);
    assert(is_stack_empty(&stk) == false);
    assert(is_stack_full(&stk) == true);

    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    stack_pop(&stk);
    assert(get_stack_top_ptr(&stk) == - 1);
    assert(is_stack_empty(&stk) == true);
    assert(is_stack_full(&stk) == false);



}


void test_get_file_name()
{
    char buf[BUF_SIZE] = {0};
    get_self_file_name(buf);
    printf("buf:%s\n", buf);
}


int main()
{             
    // test();
    // test1();
    // testHashMap();
    // test_stack();
    test_get_file_name();
    return 0;
}