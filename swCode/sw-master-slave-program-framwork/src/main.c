#include "common_master.h"

int main(){
    // 1. ahtread env init
    CRTS_init();

    // 2. master-slave-api
    test_master_api();
    test_spawn_join();


    // 3. atherad env halt
    CRTS_athread_halt();
    return 0;
}