#ifndef __get_pid_time_h__
#define __get_pid_time_h__

#include <string.h>
#include <unistd.h>
#include <time.h>

#define BUF_SIZE (1024)


const char* get_pid();
const char* timesStamp();
void get_self_file_name(char* buf);

char timestamp[BUF_SIZE] = {0};
char pid[BUF_SIZE] = {0};


const char* get_pid() {
	pid_t current_id;
	current_id = getpid();
    memset(pid, 0, sizeof(pid));
	sprintf(pid, "%d", current_id);
	return pid;
}

const char* timesStamp()
{
    time_t ticks = time(NULL);
    struct tm* ptm = localtime(&ticks);
    memset(timestamp, 0, sizeof(timestamp));
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d-%H-%M-%S", ptm);
    return timestamp;
}

void get_self_file_name(char* buf)
{
    memset(buf, 0, sizeof(buf));
    strcat(buf, timesStamp());
    strcat(buf, "_");
    strcat(buf, get_pid());
}

#endif