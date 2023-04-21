#include "mem_pool.h"
#include <stdio.h>


void mem_pool_init(MEM_POOL* mempool)
{
    // 申请 MEM_POOL_NODE 空间
    mempool->root = (MEM_POOL_NODE*)malloc(sizeof(MEM_POOL_NODE));

    // 申请 NODE_ARRAY 空间 (NODE_ARRAY里面是 分配连续的节点空间)
    mempool->root->node_array_ptr = (NODE_ARRAY*)malloc(sizeof(NODE_ARRAY));
    mempool->root->node_array_ptr->index = 0;
    
    // 默认初始化只有一个MEM_POOL_NODE节点
    mempool->root->next = NULL;

    // 内存池的一些特征
    mempool->index = 0; // 指定目前用到了第几个NODE_ARRAY结点
    mempool->capacity = default_once_alloc_size;
    mempool->uesNum = 0;

    // 记录内存池使用到的地方
    mempool->current = mempool->root;
}

NODE_Ptr get_node(MEM_POOL* mempool)
{
    if (is_mem_pool_empty(mempool)) {
        // printf("mem pool is empty, get node false\n");
        alloc_mem(mempool);
    }
    // 先定位到，待分配连续空间
    // ULL pool_node_idx = mempool->index;
    // MEM_POOL_NODE* poll_node = mempool->root;
    // while(pool_node_idx-- && poll_node != NULL) {
    //     poll_node = poll_node->next;
    // }
    NODE_ARRAY* local_node_array = mempool->current->node_array_ptr;
    NODE_Ptr node_ptr = &(local_node_array->node_array[local_node_array->index]);
    local_node_array->index++;
    mempool->uesNum++;
    return node_ptr;
}

void mem_pool_show_profile(MEM_POOL* mempool)
{
    printf("----------------mem pool show profile---------------------\n");
    printf("MEM_POOL:capacity\t\t\t %lld\n", mempool->capacity);
    printf("MEM_POOL:uesNum\t\t\t\t %lld\n", mempool->uesNum);
    printf("MEM_POOL:default alloc size\t\t %lld\n", (ULL)default_once_alloc_size);
    printf("MEM_POOL:pool_node row index\t\t %lld\n", mempool->index + 1);
    printf("MEM_POOL:pool_node col index\t\t %lld\n", mempool->root->node_array_ptr->index);
    printf("----------------------------------------------------------\n");
}

bool is_mem_pool_empty(MEM_POOL* mempool)
{
    return mempool->uesNum >= mempool->capacity;
}
void alloc_mem(MEM_POOL* mempool)
{
    mempool->capacity += default_once_alloc_size;
    mempool->index++;

    // MEM_POOL_NODE* poll_node = mempool->root;
    // while(poll_node->next != NULL) {
    //     poll_node = poll_node->next;
    // }
    
    MEM_POOL_NODE* current = mempool->current;
    current->next = (MEM_POOL_NODE*)malloc(sizeof(MEM_POOL_NODE));
    current = current->next;
    current->next = NULL;
    current->node_array_ptr = (NODE_ARRAY*)malloc(sizeof(NODE_ARRAY));
    current->node_array_ptr->index = 0;
    mempool->current = current;
}

void mem_poll_detory(MEM_POOL* mempool)
{
    MEM_POOL_NODE* p = NULL;
    ULL index = mempool->index;
    while(mempool->root != mempool->current) {
        mempool->index--;
        printf("destorying mem pool node %lld\n", index - mempool->index);
        p = mempool->root->next;
        free(mempool->root->node_array_ptr);
        free(mempool->root);
        mempool->root = p;
    }

    // free last mem pool node
    mempool->index--;
    printf("destorying mem pool node %lld\n", index - mempool->index);
    p = mempool->root->next;
    free(mempool->root->node_array_ptr);
    free(mempool->root);

    // 回归初始值
    mempool->index = 0;
    mempool->capacity = 0;
    mempool->uesNum = 0;
    mempool->root = NULL;
    mempool->current = NULL;
}
