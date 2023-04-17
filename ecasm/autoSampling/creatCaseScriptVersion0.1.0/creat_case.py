#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import shutil
import re
import json

model_dir = "/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0"

create_scripts_path = "./scripts/create_newcase -case "
create_scripts_args = " -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 "
create_scripts_pes  = " -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml"

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


json_data = load_json("./config.json")

for caseConfig in json_data["sampleTimes"]:
    case_name = caseConfig["caseName"]
    case_path = json_data["casePath"] + case_name
    STOP_N = caseConfig["stopN"]
    STOP_OPTION = caseConfig["stopN-unit"]
    ProcessN = caseConfig["ProcessN"]
    
    os.chdir(model_dir)
    
    #����CASE
    command = create_scripts_path + case_path +  create_scripts_args + create_scripts_pes
    os.system(command)
    
    os.chdir(case_path)
    
    #env_mach_pes.xml����������ڻ������ض��Ĵ���������(���޸���)
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
    
    #����ģʽԴ�� && env_case.xml�����������ض��ı���
    os.system("mkdir sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/tools ./sampling")
    
    # os.system("./xmlchange -file env_case.xml -id CCSMROOT -val " + case_path + "/sampling")
    os.system("./xmlchange -file env_case.xml -id CCSMROOT -val '$CASEROOT/sampling'")
    os.system("./xmlchange -file env_case.xml -id CCSM_MACHDIR -val '$CCSMROOT/scripts/ccsm_utils/Machines'")
    os.system("cp ./env_case.xml ./LockedFiles/env_case.xml.locked")
    
    #env_build.xml��ģ�͹�������
    os.system("./xmlchange -file env_build.xml -id EXEROOT -val '$CASEROOT/bld'")
    
    #env_run.xml����������
    #STOP_N value: none,never,nsteps,nstep,nseconds,nsecond,nminutes,nminute,nhours,nhour,ndays,nday,nmonths,nmonth,nyears,nyear,date,ifdays0,end (char)
    os.system("./xmlchange -file env_run.xml -id RUNDIR -val '$CASEROOT/run'")
    os.system("./xmlchange -file env_run.xml -id STOP_N -val " + STOP_N)
    os.system("./xmlchange -file env_run.xml -id STOP_OPTION -val " + STOP_OPTION)
    os.system("./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '$CASEROOT/archive'")
    
    #cesm_setup (��Ҫ�ж��Ƿ�setup�ɹ�)

    os.system("./cesm_setup > ./case_setup.log 2>&1") ##* Ӧ��Ϊ./cesm_setup >> ./casename.log 2>&1��casename��Ҫ�ñ�����ָ��һ�£�
    ##* �����˼�������ǽ���Ļ���ȫ�Ž�һ����������Ϊ���ֵ�log�ļ��У��ж��Ƿ�setup��build��run�ɹ���ͨ���Ӹ�log�в�����Ӧ��䣬�Լ��鿴�������̵���Ļ���������Ҫÿһ������һ��log
    
    #�޸�Macros
    with open( './Macros', 'r') as macros_old, open('./Macros' + ".new", 'w') as macros_new:
        for line in macros_old:
            if re.match(r'\s*FFLAGS\s*:=',line):
                # line = line.strip() + ' -g -finstrument-functions -mcmodel=medium \n'
                line = line
            macros_new.write(line)
    command = "mv" + ' Macros' + ' Macros' + '.previous'
    os.system(command)
    command = 'mv' + ' Macros' + '.new' + ' Macros'
    os.system(command)
    
    ##build
    #command = './' + case_name + '.build'
    #os.system(command)