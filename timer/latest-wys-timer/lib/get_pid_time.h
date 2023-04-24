#ifndef __get_pid_time_h__
#define __get_pid_time_h__

#include <string.h>
#include <unistd.h>
#include <time.h>

#define BUF_SIZE (1024)


const char* get_pid();
const char* times_stamp();
void get_self_file_name(char* buf);

char __timestamp__[BUF_SIZE] = {0};
char __pid__[BUF_SIZE] = {0};


const char* get_pid() {
	pid_t current_id;
	current_id = getpid();
    memset(__pid__, 0, sizeof(__pid__));
	sprintf(__pid__, "%d", current_id);
	return __pid__;
}

const char* times_stamp()
{
    time_t ticks = time(NULL);
    struct tm* ptm = localtime(&ticks);
    memset(__timestamp__, 0, sizeof(__timestamp__));
    strftime(__timestamp__, sizeof(__timestamp__), "%Y-%m-%d-%H-%M-%S", ptm);
    return __timestamp__;
}

void get_file_name(char* buf, const char*file_path, const char* file_postfix)
{
    memset(buf, 0, sizeof(buf));
    strcat(buf, file_path);
    strcat(buf, times_stamp());
    strcat(buf, "_"); 
    strcat(buf, get_pid());
    strcat(buf, "_");
    strcat(buf, file_postfix);
}

#endif