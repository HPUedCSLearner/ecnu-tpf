#ifndef __mem_poll__
#define __mem_poll__

#include "common.h"
#include <stdlib.h>
#include <stdbool.h>

void mem_pool_init(MEM_POOL* mempool);
NODE_Ptr get_node(MEM_POOL* mempool);
void mem_pool_show_profile(MEM_POOL* mempool);
bool is_mem_pool_empty(MEM_POOL* mempool);
void alloc_mem(MEM_POOL* mempool);
void mem_poll_detory(MEM_POOL* mempool);


#endif
