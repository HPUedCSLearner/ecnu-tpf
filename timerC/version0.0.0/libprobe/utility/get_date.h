#ifndef __GET_DATE__
#define __GET_DATE__


#include <time.h>
#include <string.h>

char timestamp[32];
const char* timesStamp();

const char* timesStamp()
{
    time_t ticks = time(NULL);
    struct tm* ptm = localtime(&ticks);
    memset(timestamp, 0, sizeof(timestamp));
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d__%H-%M-%S", ptm);
    return timestamp;
}

#endif

