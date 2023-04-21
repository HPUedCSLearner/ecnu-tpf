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
    // HASH_MAP hashmap;
    // hash_map_init(&hashmap);
    // // hash_map_show(&hashmap);

    // printf("size of (ULL): %ld\n", sizeof(ULL));

    // ULL key = 0x0101010101010101;
    // printf("hash(key) %lld\n", hash(key));

    // NODE_Ptr nodeptr = get_node(&hashmap.nodeMemPool);
    // nodeptr->key.funcAddr = 0x0101010101010101;
    // nodeptr->key.faterAddr = 0xab10101;
    // nodeptr->val.times = 0;
    // nodeptr->val.acctime = 456456;
    // nodeptr->val.sheltime = 789798;

    // hash_map_insert(&hashmap, nodeptr);

    // NODE_Ptr p;
    // int collision_step;
    // hash_map_find_key(&hashmap, nodeptr, p, &collision_step);



    // NODE_Ptr nodeptr1 = get_node(&hashmap.nodeMemPool);
    // make_node(nodeptr1, 0x0101010101010101, 0xab10101a, 0, 456456, 789798);
    // hash_map_find_key(&hashmap, nodeptr, p, &collision_step);


    // // show_node(nodeptr);  
    // // show_node(nodeptr1);  

    // hash_map_show(&hashmap);
}

void testHashMap1()
{
    HASH_MAP hashmap;
    hash_map_init(&hashmap);
    // hash_map_show(&hashmap);
    NODE_Ptr nodeptr1 = get_node(&hashmap.nodeMemPool);
    make_node(nodeptr1, 0x0101010101010101, 0xab10101a, 1, 456456, 789798);
    show_node(nodeptr1);
    NODE_Ptr nodeptr2 = get_node(&hashmap.nodeMemPool);
    make_node(nodeptr2, 0x0101010101010101, 0xab10101a, 1, 456456, 789798);
    show_node(nodeptr2);

    hash_map_insert(&hashmap, nodeptr1);   
    hash_map_insert(&hashmap, nodeptr2);   

    hash_map_show(&hashmap);
}

int main()
{
    // test();
    // test1();
    // testHashMap();
    testHashMap1();
    return 0;
}