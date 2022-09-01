#ifndef __INSTRUMENT__
#define __INSTRUMENT__

#include "probe.h"

void __attribute__((no_instrument_function))
__cyg_profile_func_enter(void *this_func, void *call_site);
 
 
void __attribute__((no_instrument_function))
__cyg_profile_func_exit(void *this_func, void *call_site);

#endif
