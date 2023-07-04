#ifndef __COMMON_MASTER_H__
#define __COMMON_MASTER_H__

// common_master.h文件是存放主核函数用的通用API、spawn-join-API、lib-API等...

#include "common.h"


// master ge-api
void test_master_api();

// master spawn-fun-join-api
void test_spawn_join();

// master lib-api
unsigned long master_timer();

#endif