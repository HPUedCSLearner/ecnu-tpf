#include "mem_pool.h"

#include "hash_table.h"

#include <assert.h>
#include <stdio.h>


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

int main()
{             
    // test();
    // test1();
    testHashMap();
    return 0;
}