#ifndef __MY_DEBUG_H__
#define __MY_DEBUG_H__
 
#include <stdio.h>
#include "timer.h"

void __attribute__((no_instrument_function)) debug_log(const char *format,...);
void __attribute__((no_instrument_function)) __cyg_profile_func_enter(void*, void*);
void __attribute__((no_instrument_function)) __cyg_profile_func_exit(void*, void*);
  
#endif
 
#include <stdarg.h>
#include <stdlib.h>
//#include "my_debug.h"
 
#define DEBUG_FILE_PATH  "./mydebug.log"
#define MOD (unsigned long)(9000)
void  __attribute__((no_instrument_function)) 
debug_log(const char *format,...)
{
    FILE *fp;
    va_list ap;
    va_start(ap, format);
    
    fp = fopen(DEBUG_FILE_PATH, "a");
    if(NULL == fp)
    {
        printf("Can not open debug file.\n");
        return;
    }
    vfprintf(fp, format, ap);
    va_end(ap);
    fflush(fp);
    fclose(fp);
}

unsigned long addr2int[9001];

int getHashId(unsigned long oriId){
	int tmp=oriId%MOD;
	// printf("oriId:%ld\n",oriId);
	if(tmp==0)tmp++;
	while(addr2int[tmp]!=oriId){
		if(addr2int[tmp]==0||addr2int[tmp]==oriId){
			addr2int[tmp]=oriId;
			return tmp;
		}	
		tmp++;
		if(tmp>9000)tmp=1;
	}
	return tmp;
}
void  __attribute__((no_instrument_function))
__cyg_profile_func_enter(void *this, void *call)
{
	// printf("yes enter\n");
	// debug_log("Enter\n%p\n%p\n", call, this);

	// printf("#yes enter:%ld %ld\n",call,this);
	int funId=getHashId((unsigned long)this), faFuncId=getHashId((unsigned long)call);
	// printf("#yes enter:%d %d\n",funId,faFuncId);
	__profile__funcID=funId;
	__profile__faFuncID=faFuncId;
	__profile__record_time_begin();
    
}
 
void  __attribute__((no_instrument_function))
__cyg_profile_func_exit(void *this, void *call)
{
    // printf("yes exit\n");
	// debug_log("Exit\n%p\n%p\n", call, this);
	// printf("#yes exit:%ld %ld\n",call,this);
	int funId=getHashId((unsigned long)this), faFuncId=getHashId((unsigned long)call);
	// printf("#yes exit:%d %d\n",funId,faFuncId);
	__profile__funcID=funId;
	__profile__fatherID=faFuncId;
	__profile__record_time_end();

	// if(this==0x4ffff049cfc0)
	// 	__profile__input_csv();
}