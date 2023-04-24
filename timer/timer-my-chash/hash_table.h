#ifndef __hash_table__
#define __hash_table__


#include "common.h"
#include <stdlib.h>
#include <stdbool.h>

#define HASH_TABLE_SIZE  (1 << 9)


typedef struct HASH_MAP
{
    NODE_Ptr node[HASH_TABLE_SIZE][HASH_TABLE_SIZE]; // 就像二维矩阵头节点
    ULL uesNum;
    ULL colisionNum;
    ULL capacity;
    MEM_POOL nodeMemPool;
}HASH_MAP;


void hash_map_init(HASH_MAP* hashmap);
void hash_map_show(HASH_MAP* hashmap);
NODE_Ptr hash_map_find_key(HASH_MAP* hashmap, const NODE* node);
void hash_map_insert(HASH_MAP* hashmap, NODE* node);
bool is_key_equeue(KEY key1, KEY key2);
ULL hash(ULL key);
void print_hash_map_node(HASH_MAP* hashmap);
void hash_map_destory(HASH_MAP* hashmap);



// void make_node(NODE_Ptr, ULL funcAddr, ULL faterAddr, int times, ULL acctime, ULL sheltime);
// void show_node(NODE_Ptr);
// void update_node(NODE_Ptr node1, const NODE_Ptr node2); // 把node2的数据更新到node1




#endif