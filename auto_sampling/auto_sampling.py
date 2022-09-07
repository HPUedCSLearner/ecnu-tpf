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

case_path =  '/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0'
caseName = 'case001'
newCase = '/case/case001'
newCasePath = case_path + newCase
STOP_N = '1'

##############################
# -------create a case-------#
##############################

def sampling(case_path):
    # print('case_path:', case_path)
    os.chdir(case_path)
    # if not os.path.exists(newCasePath):
    #     os.mkdir(newCasePath)

    #创建CASE
    command = "./scripts/create_newcase -case " + newCasePath + " -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml"
    os.system(command)

    #env_mach_pes.xml：设置组件在机器上特定的处理器布局(暂无更改)


    #备份模式源码 && env_case.xml：设置算例特定的变量
    os.chdir(newCasePath)
    os.system("mkdir sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/tools ./sampling")

    # os.system("./xmlchange -file env_case.xml -id CCSMROOT -val " + newCasePath + "/sampling")
    os.system("./xmlchange -file env_case.xml -id CCSMROOT -val '$CASEROOT/sampling'")
    os.system("./xmlchange -file env_case.xml -id CCSM_MACHDIR -val '$CCSMROOT/scripts/ccsm_utils/Machines'")
    os.system("cp ./env_case.xml ./LockedFiles/env_case.xml.locked")

    #env_build.xml：模型构建设置
    os.system("./xmlchange -file env_build.xml -id EXEROOT -val '$CASEROOT/bld'")
    os.system("cp ./env_build.xml ./LockedFiles/env_build.xml.locked")
    
    #env_run.xml：运行设置
    os.system("./xmlchange -file env_run.xml -id RUNDIR -val ' $CASEROOT/run'")
    os.system("./xmlchange -file env_run.xml -id STOP_N -val " + STOP_N)
    os.system("./xmlchange -file env_run.xml -id STOP_OPTION -val ndays")
    os.system("./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '$CASEROOT/archive'")
    os.system("cp ./env_run.xml ./LockedFiles/env_run.xml.locked")

    #cesm_setup (需要判断是否setup成功)
    os.system("./cesm_setup > ./case_setup.log 2>&1")

    #修改Macros

    #Run the build script
    os.system("./$CASE.build > ./" + caseName + " 2>&1")
    
    
def main():
    sampling(case_path)

if __name__ == '__main__':
    main()