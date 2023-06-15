/*======================================================================
* Copyright (C) 2018 Sangfor Ltd. All rights reserved.
* Programmer :Linyuanpeng
* Date       :2018/02/05
* 获取秒级，毫秒级和纳秒级的当前时间。
*========================================================================*/

#include<stdio.h>
#include<sys/time.h>

int main()
{
  struct timeval time_now = {0};
  long time_sec = 0;//秒
  long time_mil = 0;//1毫秒 = 1秒/1000 
  long time_mic = 0;//1微秒 = 1毫秒/1000

  gettimeofday(&time_now,NULL);
  time_sec = time_now.tv_sec;
  time_mil = time_sec * 1000 + time_now.tv_usec/1000;
  time_mic = time_now.tv_sec*1000*1000 + time_now.tv_usec;

  printf("second %ld\n",time_sec);
  printf("millisecond %ld\n",time_mil);
  printf("microsecond %ld\n",time_mic);

  return 0;
}