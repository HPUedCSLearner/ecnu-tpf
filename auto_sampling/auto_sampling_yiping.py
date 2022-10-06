#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import shutil
import re
import copy
import stat
from xml.dom.minidom import parse
import time
import math
import json

model_dir =  '/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/case/'  ##* 变量名不规范，建议改名为model_dir
##* 在这里加一个变量定义run_path，意为生成算例的位置，如我常用的"/public1/home/fio_climate_model/zyp/fioesm_cases"这种，建议在wys或liuyao文件夹下建立一个fioesm_cases用来装生成的算例，不建议在模式源码下存储算例
newCase = sys.argv[1] ##* 1、变量名不规范，建议改名为case，即算例名; 2、建议值直接为一个名称的形式，如case_01，不建议为部分路径字符串
### if os.path.exists(run_path+case):
###     shutil.rmtree(run_path+case)   ##* 在这里加一个if判断，判断在run_path下是否已存在同名算例，若有将同名算例删除
case_path = model_dir + newCase ##* 这句可有可无，若有，建议变量名规范化，建议改名为case_path
STOP_N = '5' 

##############################
# -------create a case-------#
##############################

def sampling(model_dir):  
    # print('model_dir:', model_dir)
    os.chdir(model_dir)
    # if not os.path.exists(case_path):
    #     os.mkdir(case_path)

    #创建CASE
    command = "./../scripts/create_newcase -case " + case_path + " -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./../scripts/f09g16_1024_pes_file_bscc-a2.xml"
    os.system(command)

    #env_mach_pes.xml：设置组件在机器上特定的处理器布局(暂无更改)


    #备份模式源码 && env_case.xml：设置算例特定的变量
    os.chdir(case_path)
    os.system("mkdir sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/tools ./sampling")

    # os.system("./xmlchange -file env_case.xml -id CCSMROOT -val " + case_path + "/sampling")
    os.system("./xmlchange -file env_case.xml -id CCSMROOT -val '$CASEROOT/sampling'")
    os.system("./xmlchange -file env_case.xml -id CCSM_MACHDIR -val '$CCSMROOT/scripts/ccsm_utils/Machines'")
    os.system("cp ./env_case.xml ./LockedFiles/env_case.xml.locked")

    #env_build.xml：模型构建设置
    os.system("./xmlchange -file env_build.xml -id EXEROOT -val '$CASEROOT/bld'")
    #done-># os.system("cp ./env_build.xml ./LockedFiles/env_build.xml.locked")  ##* 可以删去
    
    #env_run.xml：运行设置
    os.system("./xmlchange -file env_run.xml -id RUNDIR -val ' $CASEROOT/run'") #done->##* $CASEROOT前面出现奇怪空格，可能会导致运行时报错，应为'$CASEROOT/run'，
    os.system("./xmlchange -file env_run.xml -id STOP_N -val " + STOP_N)
    os.system("./xmlchange -file env_run.xml -id STOP_OPTION -val ndays")
    os.system("./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '$CASEROOT/archive'")
    #done-># os.system("cp ./env_run.xml ./LockedFiles/env_run.xml.locked")  ##* 可以删去

    #cesm_setup (需要判断是否setup成功)
    os.system("./cesm_setup > ./case_setup.log 2>&1") ##* 应改为./cesm_setup >> ./casename.log 2>&1（casename需要用变量名指代一下）
    ##* 这里的思想是我们将屏幕输出全放进一个以算例名为名字的log文件中，判断是否setup、build、run成功均通过从该log中查找相应语句，以及查看整个流程的屏幕输出，不需要每一步生成一个log

    #修改Macros
    
    
def main():
    sampling(model_dir)

if __name__ == '__main__':
    main()