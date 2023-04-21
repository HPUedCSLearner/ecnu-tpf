#include "hash_table.h"

#include "mem_pool.h"


#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <limits.h>

void hash_map_init(HASH_MAP* hashmap)
{
    ULL i, j;
    for (i = 0; i < HASH_TABLE_SIZE; ++i) {
        for (j = 0; j < HASH_TABLE_SIZE; ++j) {
            hashmap->node[i][j] = NULL;
        }
    }
    hashmap->uesNum = 0;
    hashmap->colisionNum = 0;
    hashmap->capacity = (ULL)HASH_TABLE_SIZE * (ULL)HASH_TABLE_SIZE;
    mem_pool_init(&hashmap->nodeMemPool);

}

void hash_map_show(HASH_MAP* hashmap)
{
    printf("----------------Hash MAP Profile--------------------------\n");
    printf("HASH_MAP:capacity\t\t\t %lld\n", hashmap->capacity);
    printf("HASH_MAP:uesNum\t\t\t\t %lld\n", hashmap->uesNum);
    printf("HASH_MAP:colisionNum\t\t\t %lld\n", hashmap->colisionNum);
    printf("----------------------------------------------------------\n");
    mem_pool_show_profile(&hashmap->nodeMemPool);
}


bool is_key_equeue(KEY key1, KEY key2)
{
    return (key1.funcAddr == key2.funcAddr) && (key1.faterAddr == key2.faterAddr);
}

ULL hash(ULL key)
{
    unsigned char a = key       & 0x000000ff;
    unsigned char b = key >> 8  & 0x000000ff;
    unsigned char c = key >> 16 & 0x000000ff;
    unsigned char d = key >> 24 & 0x000000ff;
    unsigned char e = key >> 32 & 0x000000ff;
    unsigned char f = key >> 40 & 0x000000ff;
    unsigned char g = key >> 48 & 0x000000ff;
    unsigned char h = key >> 56 & 0x000000ff;
    ULL all = a * b + c + d + e + f + g + h;
    return all % (ULL)HASH_TABLE_SIZE;
}

void hash_map_insert(HASH_MAP* hashmap, NODE* node)
{
    // ULL row = hash(node->key.funcAddr);
    // ULL col = hash(node->key.faterAddr);

    // if (hashmap->node[row][col] == NULL) {
    //     printf("first inert to hash map\n");
    //     hashmap->uesNum++;
    //     hashmap->node[row][col] = node;
    //     hashmap->node[row][col]->next = NULL; 
    // } else {
    //     // to do 
    //     printf("not first inert to hash map\n");

    // }

    NODE_Ptr* p;
    printf("p %p\n", p);
    printf("node %p\n", node);
    int collision_step_flag;
    if (hash_map_find_key(hashmap, node, p, &collision_step_flag)) {
        update_node(*p, node);
    } else {
        printf("p %p\n", p);
        *p = node;
        // node->next = NULL; // 这个可以省略，因为在节点构造的时候，已经为NULL了
    }
    if (collision_step_flag == INT_MIN) {
        hashmap->uesNum++;
    } else if (collision_step_flag != 0) {
        hashmap->colisionNum++;
    }
}

// 如何定义插入操作之后
// 是 碰撞？ 还是使用？ 用于更新capacity，uesNum
// 先定义碰撞操作，其他操作都是使用
// 碰撞就是: hash的位置被使用过，并且找到的位置和hashmap->node[row][col]相差的距离大于等于1
//  ULL row = hash(key->key.funcAddr);
//  ULL col = hash(key->key.faterAddr);
//  1、hash的位置被使用过：
//  hashmap->node[row][col] != NULL
//  2、找到的位置和hashmap->node[row][col]相差的距离大于等于1：
//  即、第一个node的内存地址不等 && 第二个内存地址也等
//  hashmap->node[row][col]->next != key_pos_or_new_key_pos

// 分析之后，我们可以通过在查找的时候，查找步长step，来判断碰撞

bool hash_map_find_key(HASH_MAP* hashmap, const NODE* key, NODE** key_pos_or_new_key_pos, int* collision_step)
{
    *collision_step = 0;
    ULL row = hash(key->key.funcAddr);
    ULL col = hash(key->key.faterAddr);
    if (hashmap->node[row][col] == NULL) {
        printf("not find key\n");
        *collision_step = INT_MIN; // 没有步长, 属于新添加
        key_pos_or_new_key_pos = &hashmap->node[row][col];
        printf("hashmap->node[row][col]: %p\n", hashmap->node[row][col]);
        printf("&hashmap->node[row][col]: %p\n", &hashmap->node[row][col]);
        printf("key_pos_or_new_key_pos: %p\n", key_pos_or_new_key_pos);
        return false;
    } else {
        NODE* p = hashmap->node[row][col];
        while(p->next != NULL) {
            if (!is_key_equeue(p->key, key->key)) {
                p = p->next;
                *collision_step++; // 步长不为零，说明第一个节点不是我们要找的，那么就是冲突
                continue;
            } else {
                printf("find key\n");
                *key_pos_or_new_key_pos = p;
                return true;
            }
        }

        // 判断最后一个点
        if (!is_key_equeue(p->key, key->key)) {
            *key_pos_or_new_key_pos = p;
            printf("not find key\n");
            return false;
        } else {
            printf("find key\n");
            *key_pos_or_new_key_pos = p;
            return true;
        }
    }
}




void make_node(NODE_Ptr nodeptr, ULL funcAddr, ULL faterAddr, int times, ULL acctime, ULL sheltime)
{
    if (nodeptr == NULL) {
        return;
    }
    nodeptr->key.funcAddr = funcAddr;
    nodeptr->key.faterAddr = faterAddr;
    nodeptr->val.times = times;
    nodeptr->val.acctime = acctime;
    nodeptr->val.sheltime = sheltime;
    nodeptr->next = NULL;
}

void show_node(NODE_Ptr nodeptr)
{
    if (nodeptr == NULL) {
        return;
    }
    printf("----------------Node Profile------------------------------\n");
    printf("NODE:Addr\t\t\t\t %p\n", (void*)nodeptr);
    printf("NODE:key.funcAddr\t\t\t %lld\n", nodeptr->key.funcAddr);
    printf("NODE:key.faterAddr\t\t\t %lld\n", nodeptr->key.faterAddr);
    printf("NODE:val.times\t\t\t\t %d\n", nodeptr->val.times);
    printf("NODE:val.acctime\t\t\t %lld\n", nodeptr->val.acctime);
    printf("NODE:val.sheltime\t\t\t %lld\n", nodeptr->val.sheltime);
    printf("----------------------------------------------------------\n");
}

void update_node(NODE_Ptr node1, const NODE_Ptr node2)
{
    node1->val.times += node2->val.times;
    node1->val.acctime += node2->val.acctime;
    node1->val.sheltime += node2->val.sheltime;
}