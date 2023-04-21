#ifndef __hash_table__
#define __hash_table__


#include "common.h"
#include <stdlib.h>
#include <stdbool.h>

#define HASH_TABLE_SIZE  (1 << 8)


typedef struct HASH_MAP
{
    NODE_Ptr node[HASH_TABLE_SIZE][HASH_TABLE_SIZE];
    ULL uesNum;
    ULL colisionNum;
    ULL capacity;
    MEM_POOL nodeMemPool;
}HASH_MAP;


void hash_map_init(HASH_MAP* hashmap);
void hash_map_show(HASH_MAP* hashmap);
bool hash_map_find_key(HASH_MAP* hashmap, const NODE* node, NODE** new_node_pos, int* collision_step);
ULL hash(ULL key);
bool is_key_equeue(KEY key1, KEY key2);
void hash_map_insert(HASH_MAP* hashmap, NODE* node);
// void hash_map_destory(HASH_MAP* hashmap);




#endif