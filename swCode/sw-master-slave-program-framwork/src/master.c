#include "common_master.h"
#include "common_slave.h"


// 从核接口声明
extern void SLAVE_FUN(slvae_fun_example());


// master ge-api imp
void test_master_api()
{
    printf("hello master api\n");
}


// master spawn-fun-join-api imp
void test_spawn_join()
{
    CRTS_athread_spawn(slvae_fun_example, 0);
    CRTS_athread_join();
}



// master lib-api imp
unsigned long master_timer()
{
    return CRTS_time_cycle();
}
