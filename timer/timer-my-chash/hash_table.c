#include "hash_table.h"

#include "mem_pool.h"


#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <limits.h>

// #define __debug_hash_map__ 0

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

// ULL hash(ULL key)
// {
//     unsigned char a = key       & 0x000000ff;
//     unsigned char b = key >> 8  & 0x000000ff;
//     unsigned char c = key >> 16 & 0x000000ff;
//     unsigned char d = key >> 24 & 0x000000ff;
//     unsigned char e = key >> 32 & 0x000000ff;
//     unsigned char f = key >> 40 & 0x000000ff;
//     unsigned char g = key >> 48 & 0x000000ff;
//     unsigned char h = key >> 56 & 0x000000ff;
//     ULL all = a * b + c + d + e + f + g + h;
    
//     // // 二次hash，效果不明显
//     // a = all       & 0x000000ff;
//     // b = all >> 8  & 0x000000ff;
//     // c = all >> 16 & 0x000000ff;
//     // d = all >> 24 & 0x000000ff;
//     // all += a * b + c + d;
//     return all % (ULL)HASH_TABLE_SIZE;
// }

// ----------------Hash MAP Profile--------------------------
// HASH_MAP:capacity                        262144
// HASH_MAP:uesNum                          76555
// HASH_MAP:colisionNum                     23445
// ----------------------------------------------------------

ULL hash(ULL key)
{
    // 平方取中
    ULL a = key & 0xffffffff;
    ULL b = key >> 32;
    ULL tmp = a * a + b * b;
    tmp = tmp & 0x0000ffffffff0000;
    tmp = tmp >> 16;
    tmp *= tmp;
    tmp = tmp & 0x000000ffff000000;
    tmp = tmp >> 24;
    return tmp % (ULL)HASH_TABLE_SIZE;
}

// ----------------Hash MAP Profile--------------------------
// HASH_MAP:capacity                        262144
// HASH_MAP:uesNum                          83224
// HASH_MAP:colisionNum                     16776
// ----------------------------------------------------------

void hash_map_insert(HASH_MAP* hashmap, NODE* node)
{
    NODE_Ptr ptr = hash_map_find_key(hashmap, node);
    // 找到，直接更新原来节点的值
    if (ptr != NULL) {
        update_node(ptr, node); // 把node2的数据更新到node1
        #ifdef __debug_hash_map__
        printf("[hash_map_insert]: update node, no need inster\n");
        #endif
        return;
    }

    ULL row = hash(node->key.funcAddr);
    ULL col = hash(node->key.faterAddr);
    // 没找到，有两种情况，一、头节点为空; 二、发生碰撞
    #ifdef __debug_hash_map__
    printf("[hash_map_insert]: this node first inert to hash map\n");
    #endif
    if (hashmap->node[row][col] == NULL) { 
        hashmap->uesNum++;
        hashmap->node[row][col] = node;
    } else {
        NODE_Ptr ptr = hashmap->node[row][col];
        while(ptr->next != NULL) {
            ptr = ptr->next;
        }
        ptr->next = node;
        hashmap->colisionNum++;
    }
}

void hash_map_destory(HASH_MAP* hashmap)
{
    mem_poll_detory(&hashmap->nodeMemPool);
}

// find return ptr
// not find, return NULL
NODE_Ptr hash_map_find_key(HASH_MAP* hashmap, const NODE* node)
{
    ULL row = hash(node->key.funcAddr);
    ULL col = hash(node->key.faterAddr);
    if (hashmap->node[row][col] == NULL) {
        #ifdef __debug_hash_map__
        printf("[hash_map_find_key]: not Find this node\n");
        #endif
        return NULL;
    } else {
        NODE* p = hashmap->node[row][col];
        while(p != NULL) {
            if (!is_key_equeue(p->key, node->key)) {
                p = p->next;
                continue;
            } else {
                #ifdef __debug_hash_map__
                printf("[hash_map_find_key]: Find key\n");
                #endif
                break;
            }
        }
        return p;
    }
}

void print_hash_map_node(HASH_MAP* hashmap)
{
    int i, j;
    for (i = 0; i < HASH_TABLE_SIZE; ++i) {
        for(j = 0; j < HASH_TABLE_SIZE; ++j) {
            if (hashmap->node[i][j] == NULL) {
                continue;
            }
            NODE_Ptr first_node = hashmap->node[i][j];
            while(first_node != NULL) {
                printf("funcAddr:%p \t", (void*)first_node->key.funcAddr);
                printf("faterAddr:%p \t", (void*)first_node->key.faterAddr);
                printf("times:%d \t", first_node->val.times);
                printf("acctime:%lld \t", (ULL)first_node->val.acctime);
                printf("sheltime:%lld \t", (ULL)first_node->val.sheltime);
                printf("\n");
                first_node = first_node->next;
            }
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
    if (node1 == NULL || node2 == NULL) {
        printf("update_node false, cause at last one ptr is NULL\n");
        return;
    }
    node1->val.times += node2->val.times;
    node1->val.acctime += node2->val.acctime;
    node1->val.sheltime += node2->val.sheltime;
}