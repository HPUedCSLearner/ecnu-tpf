#include "common_slave.h"

// 常用变量
unsigned long t1, t2;

// 常用宏变量
// CRTS_tid;
// CRTS_cid;
// CRTS_rid;

// Slave Lib-Api
unsigned long slave_timer()
{
    return CRTS_stime_cycle();
}

// Slave Fun-Api Imp
void slvae_fun_example(){
    int myid = CRTS_tid; int cid = CRTS_cid; int rid = CRTS_rid;
    int cgn  = CRTS_smng_get_cgn();
    int spcn = CRTS_smng_get_spcn();
    t1 = slave_timer();
    if (myid == 63) {
        printf("I am in [%d, %d], cgn: %d, spcn: %d\n", rid, cid, cgn, spcn);
        printf("%s:%d, %s(): ....\n", __FILE__, __LINE__, __func__);
    }
    t2 = slave_timer();
    if (myid == 63) {
        printf("t2 - t1 : %lld\n", t2 -t1);
    }
}


