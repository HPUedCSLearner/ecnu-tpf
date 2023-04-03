#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import shutil
import re
import json
import thread
import time

model_dir = "/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0"

create_scripts_path = "./scripts/create_newcase -case "
create_scripts_args = " -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 "
create_scripts_pes  = " -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml"

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def build_case(case_name):
    command = './' + case_name + '.build'
    print("------command:", command)
    #os.system(command)
    os.system('pwd')
    print("------build command done!!!")
    time.sleep(300)



json_data = load_json("./config.json")

for caseConfig in json_data["sampleTimes"]:
    if caseConfig["isCreate"] != "True":
        print "isCreadte is configed not True, do not create this cases"
        continue
    case_name = caseConfig["caseName"]
    case_path = json_data["casePath"] + case_name
    STOP_N = caseConfig["stopN"]
    STOP_OPTION = caseConfig["stopN-unit"]
    ProcessN = caseConfig["ProcessN"]
    linkLibFlag = json_data["libconfig"]["staticLibPath"] + " " + json_data["libconfig"]["staticLibName"] + " "
    linkLibFlag = linkLibFlag + json_data["libconfig"]["sharedLibPath"] + " " + json_data["libconfig"]["sharedLibName"]
    
    os.chdir(model_dir)
    
    #创建CASE
    command = create_scripts_path + case_path +  create_scripts_args + create_scripts_pes
    os.system(command)
    
    os.chdir(case_path)
    
    #env_mach_pes.xml：设置组件在机器上特定的处理器布局(暂无更改)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ATM -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_LND -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ICE -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_OCN -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_OCN -val 0")
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_CPL -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_GLC -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ROF -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_WAV -val " + ProcessN)
    os.system("./xmlchange -file env_mach_pes.xml -id TOTALPES -val " + ProcessN)
    
    #备份模式源码 && env_case.xml：设置算例特定的变量
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
    
    #env_run.xml：运行设置
    #STOP_N value: none,never,nsteps,nstep,nseconds,nsecond,nminutes,nminute,nhours,nhour,ndays,nday,nmonths,nmonth,nyears,nyear,date,ifdays0,end (char)
    os.system("./xmlchange -file env_run.xml -id RUNDIR -val '$CASEROOT/run'")
    os.system("./xmlchange -file env_run.xml -id STOP_N -val " + STOP_N)
    os.system("./xmlchange -file env_run.xml -id STOP_OPTION -val " + STOP_OPTION)
    os.system("./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '$CASEROOT/archive'")
    
    #cesm_setup (需要判断是否setup成功)

    os.system("./cesm_setup > ./case_setup.log 2>&1") ##* 应改为./cesm_setup >> ./casename.log 2>&1（casename需要用变量名指代一下）
    ##* 这里的思想是我们将屏幕输出全放进一个以算例名为名字的log文件中，判断是否setup、build、run成功均通过从该log中查找相应语句，以及查看整个流程的屏幕输出，不需要每一步生成一个log
    
    #修改Macros
    with open( './Macros', 'r') as macros_old, open('./Macros' + ".new", 'w') as macros_new:
        for line in macros_old:
            if re.match(r'\s*FFLAGS\s*:=', line):
                line = line.strip() + ' -g -finstrument-functions -mcmodel=medium \n'
                #line = line
            macros_new.write(line)
    command = "mv" + ' Macros' + ' Macros' + '.previous'
    os.system(command)
    command = 'mv' + ' Macros' + '.new' + ' Macros'
    os.system(command)
    
    #修改Makefile
    with open( './Tools/Makefile', 'r') as Makefile_old, open('./Tools/Makefile' + ".new", 'w') as Makefile_new:
        for line in Makefile_old:
            if re.search( "\$\(LD\) -o \$\(EXEC_SE\)", line):
                line = line.strip() + ' ' + linkLibFlag + '\n'
                #print line
            Makefile_new.write(line)
    command = 'mv' + ' ./Tools/Makefile' + ' ./Tools/Makefile' + '.previous'
    os.system(command)
    command = 'mv' + ' ./Tools/Makefile' + '.new' + ' ./Tools/Makefile'
    os.system(command)
    
    
    # 修改屏蔽gtpl源码
    print("we will change below source files")
    print(json_data["modifyGptl"]["item1"])
    print(json_data["modifyGptl"]["item2"])
    print(json_data["modifyGptl"]["item3"])
    print(json_data["modifyGptl"]["item4"])
    command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item1"] + " -i"
    os.system(command)
    command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item2"] + " -i"
    os.system(command)
    command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item3"] + " -i"
    os.system(command)
    command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item4"] + " -i"
    os.system(command)
    
    # 构建模式
    # command = './' + case_name + '.build'
    # os.system(command)
    #try:
    #   thread.start_new_thread( build_case, (case_name,) )
    #except:
    #   print "Error: unable to start thread"
