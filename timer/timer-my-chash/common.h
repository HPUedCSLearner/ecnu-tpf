#ifndef __common_h__
#define __common_h__


#define default_once_alloc_size  10000

typedef unsigned long long ULL;

typedef struct KEY
{
    ULL funcAddr;
    ULL faterAddr;
}KEY;

typedef struct VALUE
{
    int times;
    ULL acctime;
    ULL sheltime;
}VALUE;

typedef struct NODE
{
    KEY key;
    VALUE val;
    struct NODE* next; // 链地址法，解决冲突
}NODE, *NODE_Ptr;

void make_node(NODE_Ptr, ULL funcAddr, ULL faterAddr, int times, ULL acctime, ULL sheltime);
void show_node(NODE_Ptr);
void update_node(NODE_Ptr node1, const NODE_Ptr node2); // 把node2的数据更新到node1

// mempool data stuct
typedef struct NODE_ARRAY
{
    NODE node_array[default_once_alloc_size];
    ULL index;
}NODE_ARRAY;

typedef struct MEM_POOL_NODE
{
    struct MEM_POOL_NODE* next;
    struct NODE_ARRAY* node_array_ptr; // 连续节点空间
}MEM_POOL_NODE;

typedef struct MEM_POOL
{
    MEM_POOL_NODE* root;
    MEM_POOL_NODE* current;
    ULL index;
    ULL capacity;
    ULL uesNum;
}MEM_POOL;



#endif