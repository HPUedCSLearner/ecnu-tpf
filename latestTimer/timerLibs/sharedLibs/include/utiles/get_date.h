#ifndef __GET_DATE__
#define __GET_DATE__

#include <sys/types.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

char timestamp[32]  = {"\0"};
const char* timesStamp();


char _pid[100] = {"\0"};
const char* get_pid();

const char* timesStamp()
{
    time_t ticks = time(NULL);
    struct tm* ptm = localtime(&ticks);
    memset(timestamp, 0, sizeof(timestamp));
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d__%H-%M-%S", ptm);
    return timestamp;
}


const char* get_pid() {
	pid_t current_id;
	current_id = getpid();
	sprintf(_pid, "%d", current_id);
	return _pid;
}

#endif

