import os
import sys
import string
import shutil
import re
import copy
import stat
from xml.dom.minidom import parse
import configparser
import time
import math
import json


def sampling(case_path, machine,model_path, case_name,sampling_procs,qname, max_npr_yz):
    llvm_path = os.environ['LLVM_PATH']
    netcdf_path = os.environ['LLVMNETCDF_PATH']
    uq_path    = os.environ['UQ_PATH']
    db_path    = uq_path+'/DataBase/'
    sys.path.append(db_path)
    import db_init
    import db_inter
    if os.path.exists(case_path + '/sampling'):
        command = 'rm -r ' + case_path+'/sampling'
        os.system(command)
    #设置flang环境变量
    os.environ["PATH"] += os.pathsep + os.pathsep.join([llvm_path + '/bin'])
    os.environ["LD_LIBRARY_PATH"] += os.pathsep + os.pathsep.join([llvm_path + '/lib'])
    status =  os.system('flang --version >>' + case_path + '/checktmp.log 2>&1')
    assert status ==0, 'load flang compiler fail'
    #源码路径
    code_path = os.path.split(os.path.realpath(__file__))[0]
    # print(code_path)
    print('case_path',case_path)
    #插装
    #复制文件
    if not os.path.exists(case_path + '/sampling'):
        os.mkdir(case_path + '/sampling')
    if not os.path.exists(case_path + '/sampling' + '/result_module'):
        os.mkdir(case_path + '/sampling' + '/result_module')
    if not os.path.exists(case_path + '/sampling' + '/result_modules'):
        os.mkdir(case_path + '/sampling' + '/result_modules')
    if not os.path.exists(case_path + '/sampling' + '/pass'):
        os.mkdir(case_path + '/sampling' + '/pass')
    command = "cp -r  " + code_path + "/timer  " + case_path + '/sampling/'
    os.system(command)
    command = "cp -r  "  + model_path + "/models  " + case_path + '/sampling'
    os.system(command)
    command = "cp  " + code_path + "/getins/getIns1.sh  " + case_path + "/Tools/getIns.sh  "
    os.system(command)
    command = 'cp  ' + code_path + '/get_new_usrdf/get_new_usrdf.cpp  ' + case_path + '/sampling/get_new_usrdf.cpp'
    os.system(command)
    command = 'cp  ' + code_path + '/fit/*  ' + case_path + '/sampling/'
    os.system(command)
    
    #修改pass 内文件path
    
    #编译pass
    os.chdir(case_path+ '/sampling/pass')
    templatepath = code_path + "/pass/GetUsrDF.template"
    template = string.Template(open(templatepath, 'r').read())
    content = template.substitute(CASEPATH=case_path)
    pass_towrite = open(case_path + "/sampling/pass/GetUsrDF.cpp",'w')
    pass_towrite.write(content)
    pass_towrite.close()
    
    templatepath = code_path + "/pass/insert_tableline.template"
    template = string.Template(open(templatepath, 'r').read())
    content = template.substitute(CASEPATH=case_path)
    pass_towrite = open(case_path + "/sampling/pass/insert_tableline.cpp",'w')
    pass_towrite.write(content)
    pass_towrite.close()
    
    templatepath = code_path + "/pass/instrument_time_function.template"
    template = string.Template(open(templatepath, 'r').read())
    content = template.substitute(CASEPATH=case_path)
    pass_towrite = open(case_path + "/sampling/pass/instrument_time_function.cpp",'w')
    pass_towrite.write(content)
    pass_towrite.close()
    command = "`llvm-config --bindir`/clang  -shared  -fPIC `llvm-config --cxxflags`  `llvm-config --ldflags`" + case_path+ '/sampling/pass/' +  "GetUsrDF.cpp -o " +case_path + "/sampling/pass/GetUsrDF.so  >>" + case_path + '/checktmp.log 2>&1'
    os.system(command)
    command = "`llvm-config --bindir`/clang  -shared  -fPIC `llvm-config --cxxflags`  `llvm-config --ldflags`" + case_path+ '/sampling/pass/' +  "instrument_time_function.cpp -o "  + case_path + "/sampling/pass/instrument_time_function.so >>" + case_path + '/checktmp.log 2>&1'
    os.system(command)
    command = "`llvm-config --bindir`/clang  -shared  -fPIC `llvm-config --cxxflags`  `llvm-config --ldflags`" + case_path+ '/sampling/pass/' +  "insert_tableline.cpp -o "  + case_path + "/sampling/pass/insert_tableline.so >>" + case_path + '/checktmp.log 2>&1'
    os.system(command)
    
    os.system("rm " + case_path + "/checktmp.log")
    #进入case
    os.chdir(case_path)
    
    #修改Macros
    with open( './Macros.' + machine, 'r', encoding="utf-8") as macros_old, open('./Macros.' + machine + ".new", 'w', encoding="utf-8") as macros_new:
        flag = 0
        fflag = 0
        for line in macros_old:
            if re.match(r'\s*MPICH_PATH\s*:=', line):
                mpich_path = re.sub(r'MPICH_PATH\s*:=\s*', '', line)
                mpich_path = re.sub(r'\s*', '', mpich_path
                )
                # print(mpich_path)
            if re.match('\s*CPP\s*:=', line):
                line = 'CPP := clang-cpp\n'
            elif re.match(r'\s*CPPDEFS\s*:=', line):
                line = line + '\nCPP :=clang-cpp\nFPP := clang-cpp\n'
            elif re.match(r'\s*FC\s*:=', line):
                line = ' '*4 + 'FC := flang\n'
            elif re.match(r'\s*CC\s*:=', line):
                line = ' ' *4 + 'CC := clang\n'
            elif re.match(r'\s*NETCDF_PATH\s*:=', line):
                line = ' '*4 + 'NETCDF_PATH := ' + netcdf_path + '\n'
            elif re.match(r'\s*LIB_NETCDF\s*:=', line):
                line = 'LIB_NETCDF := $(NETCDF_PATH)/lib -lnetcdff -lnetcdf\n'
            elif re.match(r'\s*LIB_MPI\s*:=\s*\S+/lib', line) and re.search('openmpi',mpich_path) != None:
                line = line[:-1] + '  -lmpi_usempi -lmpi_mpifh -lmpi\n'
            elif re.match(r'\s*LIB_MPI\s*:=\s*\S+/lib',line) and re.search('intel',mpich_path) != None:
                line = line[:-1] + '  -lmpi -lmpifort\n'
            elif re.match(r'\s*FIXEDFLAGS\s*:=', line):
                line = 'FIXEDFLAGS    :=\n' #-ffixed-form -fno-strict-float-cast-overflow
            elif re.match(r'\s*FREEFLAGS\s*:=', line):
                line = 'FREEFLAGS    :=\n' #-ffree-form -fno-strict-float-cast-overflow
            elif re.match(r'ifeq\s*\(\s*\$\(strip\s*\$\(MODEL\)\)\s*,\s*pop2\s*\)', line):
                fflag = 1
            elif re.match(r'ifeq\s*\(\s*\$\(strip\s*\$\(MODEL\)\)\s*,\s*licom\s*\)', line):
                fflag = 2
            elif re.match(r'\s*FFLAGS\s*:=\s*\$\(CPPDEFS\)',line) and fflag == 0:
                line = 'FFLAGS        := $(CPPDEFS) -mcmodel=large  -m64 -Mbyteswapio -Mdaz -Kieee \n'
            elif  re.match(r'\s*FFLAGS\s*:=\s*\$\(CPPDEFS\)',line) and fflag == 1:
                line = 'FFLAGS        := $(CPPDEFS) -mcmodel=large -g  -Mbyteswapio -r8   -fno-vectorize -O1  -Kieee \n'
                fflag = 0
            elif  re.match(r'\s*FFLAGS\s*:=\s*\$\(CPPDEFS\)',line) and fflag == 2:
                line = 'FFLAGS        := $(CPPDEFS) -mcmodel=large  -g -Mbyteswapio -r8  -fno-vectorize -DLICOM -O1  -Kieee \n'
                fflag = 0
            elif re.match(r'\s*LDFLAGS\s*:=', line):
                line = 'LDFLAGS    := -m64\n'
            elif re.match(r'\s*INCLDIR\s*:=\s*-I.' ,line):
                line = line + '\nINCLDIR += -I$(EXEROOT)/atm/obj -I$(EXEROOT)/lnd/obj -I$(EXEROOT)/cpl/obj  -I$(EXEROOT)/gea/obj -I$(EXEROOT)/glc/obj -I$(EXEROOT)/ice/obj  -I$(EXEROOT)/ocn/obj   -I$(EXEROOT)/wrf/obj  -I$(EXEROOT)/ccsm/obj -I' + llvm_path + '/include\n'
            elif re.match(r'ifeq\s*\(\s*\$\(DEBUG\)\s*,\s*TRUE\s*\)', line):
                flag = 2
            elif re.match(r'\s*FFLAGS\s*\+=', line) and flag == 2:
                line = ' '*2 + 'FFLAGS  += -gmodules -g\n'
                flag = 3
            elif re.match(r'\s*FFLAGS_NOOPT\s*\+=', line) and flag ==3:
                line = ' '*2 + 'FFLAGS_NOOPT  += -gmodules -g\n'
                flag = 0
            elif re.match(r'ifeq\s*\(\s*\$\(MODEL\)\s*,\s*pio\s*\)', line):
                flag = 1
            elif re.match(r'\s*CONFIG_ARGS\s*\+=\s*MPIF90' ,line) and flag == 1:
                flag = 0
                line = '  CONFIG_ARGS += MPIF90="$(FC)" MPICC="$(CC)" CC="$(CC)" F90="$(FC)" FPP="$(FPP)" NETCDF_PATH="$(NETCDF_PATH)" MPI_INC="-I$(INC_MPI)"\n'
            elif re.match(r'ifeq\s*\(\s*\$\(MODEL\)\s*,\s*mct\s*\)', line):
                flag = 4
            elif re.match(r'\s*CONFIG_ARGS\s*\+=\s*CC' ,line) and flag == 4:
                line = '  CONFIG_ARGS += CC="$(CC)" FC="$(FC)" F90="$(FC)" MPIF90="$(FC)" FPP="$(FPP)" INCLUDEPATH="-I$(INC_MPI)"\n'
                flag = 0
            macros_new.write(line)
    command = "mv" +  '  Macros.' + machine  +  '  Macros.' + machine + '.old'
    os.system(command)
    
    command = 'mv ' + '  Macros.' + machine + '.new' + '  Macros.' + machine
    os.system(command)
    command = 'cp ' + '  Macros.' + machine + ' ./LockedFiles/Macros.' + machine + '.locked'
    os.system(command)
    #修改env_mach_specific
    with open('./env_mach_specific', 'a+', encoding = 'utf-8') as env_mach_specific:
        env_mach_specific.write("\nsetenv PATH  " + llvm_path + "/bin:${PATH}\n")
        env_mach_specific.write("setenv LD_LIBRARY_PATH " + llvm_path + "/lib:" +netcdf_path +"/lib:" + "${LD_LIBRARY_PATH}")
    
    #修改env_case
    command='./xmlchange -file env_case.xml -id CODEROOT' +' -val '+case_path+"/sampling/models"
    os.system(command)
    command='./xmlchange -file env_case.xml -id SHAREROOT' +' -val '+case_path+"/sampling/models/csm_share"
    os.system(command)
    command="cp env_case.xml ./LockedFiles/env_case.xml.locked"
    os.system(command)
    
    
    
    #编译timer
    os.chdir(case_path + '/sampling/timer')
    templatepath = "./timer.template"
    template = string.Template(open(templatepath, 'r').read())
    content = template.substitute(CASEPATH=case_path)
    timer_towrite = open("./timer.c",'w')
    timer_towrite.write(content)
    timer_towrite.close()
    
    #copy replace code 手动插装
    os.chdir(case_path + '/sampling/models')
    command = 'cp  ' +   code_path + "/code_replace/m_List.F90  " + case_path + '/sampling/models/utils/mct/mpeu/'
    os.system(command)
    command = 'cp  ' +   code_path + "/code_replace/m_String.F90  " + case_path + '/sampling/models/utils/mct/mpeu/'
    os.system(command)
    command = 'cp  ' +   code_path + "/code_replace/alloc_mod.F90.in  " + case_path + '/sampling/models/utils/pio/'
    os.system(command)

    #change buildlib
    os.chdir(case_path + '/Buildconf')
    with open('mct.buildlib', 'r', encoding = 'utf-8') as f1, open('mct.buildlib.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*setenv\s*MCT_DIR', line):
                line = 'setenv MCT_DIR $CODEROOT/utils/mct\n'
            f2.write(line)
    command = 'mv  mct.buildlib  mct.buildlib.old'
    os.system(command)
    command = 'mv mct.buildlib.new  mct.buildlib'
    os.system(command)
    with open('pio.buildlib', 'r', encoding = 'utf-8') as f1, open('pio.buildlib.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*setenv\s*PIO_DIR', line):
                line = 'setenv PIO_DIR $CODEROOT/utils/pio\n'
            f2.write(line)
    command = 'mv  pio.buildlib  pio.buildlib.old'
    os.system(command)
    command = 'mv pio.buildlib.new  pio.buildlib'
    os.system(command)
    
    os.chmod('mct.buildlib', stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
    os.chmod('pio.buildlib', stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
    
    #change mct pio Makefile
    os.chdir(case_path + '/sampling/models/utils/mct/mct')
    with open('Makefile', 'r', encoding = 'utf-8') as f1, open('Makefile.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCPATH\)\s+\$\(DEFS\)', line):
                line = '\t$(FC) -emit-llvm -c  $(INCPATH) $(DEFS) $(FCFLAGS) $(F90FLAGS) $(MCTFLAGS) $*.F90 -o $*.bc \n\tsh $(CASETOOLS)/getIns.sh $< \n'
            elif re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCPATH\)\s+\$\(FCFLAGS\)' ,line):
                line = '\t$(FC) -emit-llvm -c $(INCPATH) $(FCFLAGS) $(F90FLAGS) $(MCTFLAGS) $*.f90 -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $< \n'
            f2.write(line)
    command = 'mv  Makefile  Makefile.old'
    os.system(command)
    command = 'mv Makefile.new  Makefile'
    os.system(command)
    
    os.chdir(case_path + '/sampling/models/utils/mct/mpeu')
    with open('Makefile', 'r', encoding = 'utf-8') as f1, open('Makefile.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCPATH\)\s+\$\(DEFS\)', line):
                line = '\t$(FC) -emit-llvm -c $(INCPATH) $(DEFS) $(FCFLAGS) $(F90FLAGS) $(MPEUFLAGS) $*.F90 -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCPATH\)\s+\$\(FCFLAGS\)' ,line):
                line = '\t$(FC) -emit-llvm -c $(INCPATH) $(FCFLAGS) $(F90FLAGS) $(MPEUFLAGS) $*.f90 -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(CC\)\s+-c\s+\$\(ALLCFLAGS\)', line):
                line = '\t$(CC) -emit-llvm -c $(ALLCFLAGS) $*.c -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            f2.write(line)
    command = 'mv  Makefile  Makefile.old'
    os.system(command)
    command = 'mv Makefile.new  Makefile'
    os.system(command)
    
    os.chdir(case_path + '/sampling/models/utils/pio')
    with open('Makefile', 'r', encoding = 'utf-8') as f1, open('Makefile.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*\$\(MPIF90\)\s+-c\s+\$\(FFLAGS\)\s+[\s\S]+F90', line):
                line = '\t$(MPIF90) -emit-llvm -c $(FFLAGS) $(FOPTS) $(INCLUDES) $*.F90 -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(MPIF90\)\s+-c\s+\$\(FFLAGS\)\s+[\s\S]+f90', line):
                line = '\t$(MPIF90) -emit-llvm  -c $(FFLAGS) $(FOPTS) $(INCLUDES) $*.f90 -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(MPICC\)\s+-c\s+\$\(CFLAGS\)\s+[\s\S]+c', line):
                line =  '\t$(MPICC) -emit-llvm -c $(CFLAGS) $(COPTS) $(INCLUDES) $*.c -o $*.bc\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            f2.write(line)
    command = 'mv  Makefile  Makefile.old'
    os.system(command)
    command = 'mv Makefile.new  Makefile'
    os.system(command)
    
    #change Makefile.conf.in pio mct
    os.chdir(case_path + '/sampling/models/utils')
    command = 'sed -i "s/-shared-intel / /g" `grep  "-shared-intel" -rl ./`'
    os.system(command)
    
    #源码插装修改
    '''
    1. isnan修改为 ieee_is_nan  /  use ieee_arithmetic
    2. &不合语法规范导致的编译错误
    3. IF DEFINEND -> ifdef
    4.修改cloud_fraction.F90 leafinterception.F90
    5. lsize 重复定义
    '''
    
    #1. isnan修改为 ieee_is_nan  /  use ieee_arithmetic
    os.chdir(case_path + "/sampling/models/")
    command = 'grep -r -l "[ \(]isnan(" .'
    result_file = os.popen(command).read().split("\n")
    for each_file in result_file:
        if not re.match(r'\S+F90', each_file):
            continue
        to_write = each_file + '.new'
        flag1 = 0
        flag2 = 0
        with open(each_file, 'r', encoding='utf-8') as f1, open(to_write, 'w', encoding ='utf-8') as f2:
            for line in f1:
                if re.match(r'\s*module\s+', line, re.I) and flag1 == 0:
                    flag1 = 1
                    line = line + "   use ieee_arithmetic\n"
                elif (re.match(r'\s*subroutine[\s\S]+\([\S\s]+\)', line, re.I) or re.match(r'\s*subroutine\s+\w+\s*\Z', line, re.I) or re.match(r'\s*subroutine\s+[\w]+\s*!', line, re.I)) and flag1 == 0:
                    line = line  + "   use ieee_arithmetic\n"
                elif re.match(r'\s*subroutine\s+\S+\s*\([\w, &]+', line, re.I) and flag1 == 0 and flag2 == 0:
                    flag2 = 1
                elif re.match(r'\s+[\w, ]+\)',line) and flag2 == 1 and flag1 == 0:
                    line = line +  "   use ieee_arithmetic\n"
                    flag2 = 0
                f2.write(line)
        command='mv ' + to_write + '  ' + each_file
        os.system(command)
        command = "sed -i 's/ isnan(/ ieee_is_nan(/g' " + each_file
        os.system(command)
        command = "sed -i 's/(isnan(/(ieee_is_nan(/g' " + each_file
        os.system(command)
    
    # 2. &不合语法规范导致的编译错误
    os.chdir(case_path + "/sampling/models/")
    command = 'grep -r -l --include="*.F90" -P  "[\s\S]+,[\s\S]+&[\s]{5,}[\s\S]+,[\s\S]+&\s*" .'
    result = os.popen(command).read().split("\n")
    for each_file in result:
        if not re.match(r'\S+F90', each_file):
            continue
        to_write = each_file + '.new'
        with open(each_file, 'r', encoding='utf-8') as f1, open(to_write, 'w', encoding ='utf-8') as f2:
            for line in f1:
                if re.match(r'[\s\S]+,[\s\S]+&[\s]{5,}[\s\S]+,[\s\S]+&\s*', line):
                    line = re.sub(r',\s*&\s*', ', &\n', line)
                f2.write(line)
        command='mv ' + to_write + '  ' + each_file
        os.system(command)
    
    # 3. IF DEFINEND -> ifdef
    command = 'sed -i "s/#IF DEFINED/#ifdef/g"  `grep  "^#IF DEFINED" -rl ./`'
    os.system(command)
    
    # 4. 修改cloud_fraction.F90  leafinterception.F90 meltf.F90 
    #精度控制:leafinterception.F90  e-10 -> e-8
    #               meltf.F90 e-6 -> e-5
    os.chdir(case_path + "/sampling/models/atm/iap/src/physics/")
    with open("cloud_fraction.F90", 'r', encoding = "utf-8") as f1, open("cloud_fraction.F90.new", 'w', encoding = "utf-8") as f2:
        for line in f1:
            if re.match(r"\s+zmh_u00tab\s*=\s*u00tab\(k0,j0\)", line):
                line = "    zmh_u00tab = DBLE(u00tab(k0,j0))\n"
            elif re.match(r'\s+integer\(r8\),\s+intent\(in\)', line):
                line = re.sub(r'\(r8\)', '', line)
            f2.write(line)
    command='mv ' + 'cloud_fraction.F90.new  ' + 'cloud_fraction.F90'
    os.system(command)
    
    os.chdir(case_path + "/sampling/models/lnd/colm/src/mainc")
    with open("leafinterception.F90", 'r', encoding = "utf-8") as f1, open("leafinterception.F90.new", 'w', encoding = "utf-8") as f2:
        for line in f1:
            if re.match(r"\s+if\(\s*tex\s*\+\s*tti\s*-\s*p0\s*>\s*1\.e-10\s*\)\s*then", line):
                line = "       if(tex+tti-p0 > 1.e-8) then\n"
            f2.write(line)
    command='mv ' + 'leafinterception.F90.new  ' + 'leafinterception.F90'
    os.system(command)
    
    with open("meltf.F90", 'r', encoding = "utf-8") as f1, open("meltf.F90.new", 'w', encoding = "utf-8") as f2:
        for line in f1:
            if re.match(r"\s+if\(\s*abs\(we\)\s*>\s*1\.e-6\s*\)\s*stop", line):
                line = "  if(abs(we)>1.e-5) stop 'meltf error'\n"
            f2.write(line)
    command='mv ' + 'meltf.F90.new  ' + 'meltf.F90'
    os.system(command)
    
    # 5. lsize 重复定义
    def repl(matched):
        matched_str = matched.group()
        matched_str= matched_str.replace('lsize', 'lsize2')
        return matched_str
    os.chdir(case_path + '/sampling/models/lnd')
    command = 'grep -r -l -P --include="*.F90"  "\s+integer[\s\S]+lsize\s*," .'
    result = os.popen(command).read().split("\n")
    for each_file in result:
        if not re.match(r'\S+F90', each_file):
            continue
        to_write = each_file + '.new'
        with open(each_file, 'r', encoding='utf-8') as f1, open(to_write, 'w', encoding ='utf-8') as f2:
            for line in f1:
                if re.match(r'\s+integer[\s\S]+lsize[\s,]+', line):
                    line = re.sub(r'lsize[\s,]+', repl, line)
                elif re.match(r'\s+lsize\s+=', line):
                    line = re.sub(r'\s+lsize\s+=', repl, line)
                elif re.search(r'[\(=,]\s*lsize\s*[,\)]', line):
                    line = re.sub(r'[\(=,]\s*lsize\s*[,\)]', repl, line)
                f2.write(line)
        command='mv ' + to_write + '  ' + each_file
        os.system(command)
    
    #change Tools/Makefile
    os.chdir(case_path + '/Tools')
    with open('Makefile', 'r', encoding = 'utf-8') as f1, open('Makefile.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*\$\(CC\)\s+-c\s+\$\(INCLDIR\)[\s\S]+CFLAGS', line):
                line = '\t$(CC) -emit-llvm -c $< $(INCLDIR) $(INCS) $(CFLAGS)\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCLDIR\)[\s\S]+FIXEDFLAGS', line):
                line = '\t$(FC) -emit-llvm -c $< $(INCLDIR) $(INCS) $(FFLAGS) $(FIXEDFLAGS) \n\tsh $(CASETOOLS)/getIns.sh $< \n'
            elif re.match(r'\s*\$\(FC\)\s+-c\s+\$\(INCLDIR\)[\s\S]+FREEFLAGS', line):
                line = '\t$(FC) -emit-llvm -c $(INCLDIR) $(INCS) $(FFLAGS) $(FREEFLAGS)  $<\n\tsh $(CASETOOLS)/getIns.sh $<\n'
            elif re.match(r'\s*\$\(LD\)\s+-o\s+\$\(EXEC_SE\)[\s\S]+LDFLAGS', line):
                line = '\tclang -emit-llvm -c -I' + mpich_path+'/include  ' + case_path + '/sampling/timer/' +"mpiwrapper.c" + " -o mpiwrapper.bc\n"
                line = line +  '\tflang -emit-llvm -c -I' + mpich_path+'/include  ' +  case_path + '/sampling/timer/' +"mpiwrapper_f.c" + " -o mpiwrapper_f.bc\n"
                line = line + '\tsh $(CASETOOLS)/getIns.sh ' +' mpiwrapper.bc\n'
                line = line + '\tsh $(CASETOOLS)/getIns.sh ' + ' mpiwrapper_f.bc\n'
                line = line + '\t$(LD) -o $(EXEC_SE) $(OBJS) $(CLIBS) $(ULIBS) $(SLIBS) $(MLIBS) $(LDFLAGS)  ' +  '$(EXEROOT)/ccsm/obj/mpiwrapper_f.o  ' +'$(EXEROOT)/ccsm/obj/mpiwrapper.o \n'
            f2.write(line)
    command = 'mv  Makefile  Makefile.old'
    os.system(command)
    command = 'mv Makefile.new  Makefile'
    os.system(command)
    
    #first build to get usrDF
    os.chdir(case_path)
    if os.path.exists('build'):
        command = 'rm -r ./build && mkdir build'
        os.system(command)
    # command = './' + case_name + '.' + machine + '.clean_build >> ./' + case_name + '.log 2>&1'
    # os.system(command)
    command = './' + case_name + '.' + machine +'.build > ./' + case_name + '.log 2>&1'
    os.system(command)
    
    build_count = 1
    while(os.system( 'grep -q "CCSM BUILDEXE SCRIPT HAS FINISHED SUCCESSFULLY" ' +  case_name + '.log') != 0 and build_count < 5):
        command = './' + case_name + '.' + machine +'.build > ./' + case_name + '.log 2>&1'
        os.system(command)
        build_count += 1
    #还原env_conf
    command = 'cp ./LockedFiles/env_conf.xml.locked env_conf.xml'
    os.system(command)
    #去除重复
    os.chdir(case_path + '/sampling')
    command = "g++ " + case_path + "/sampling/get_new_usrdf.cpp  -o get_new_usrdf"
    os.system(command)
    command = "./get_new_usrdf"
    os.system(command)
    
    #second build
    
    #插装修改ccsm_comp_mod.F90
    command = 'cp  ' +   code_path + "/code_replace/ccsm_comp_mod.F90  " + case_path + '/sampling/models/drv/driver/'
    os.system(command)
    
    #change Tools/Makefile
    os.chdir(case_path + '/Tools')
    with open('Makefile', 'r', encoding = 'utf-8') as f1, open('Makefile.new', 'w', encoding = 'utf-8') as f2:
        for line in f1:
            if re.match(r'\s*\$\(LD\)\s+-o\s+\$\(EXEC_SE\)[\s\S]+LDFLAGS', line):
                line = "\tclang -c  " + case_path +  "/sampling/timer/timer.c  -o timer.o\n"
                line = line + '\t$(LD) -o $(EXEC_SE) $(OBJS) $(CLIBS) $(ULIBS) $(SLIBS) $(MLIBS) $(LDFLAGS)  ' + '$(EXEROOT)/ccsm/obj/timer.o  ' +  '$(EXEROOT)/ccsm/obj/mpiwrapper_f.o  ' +'$(EXEROOT)/ccsm/obj/mpiwrapper.o \n'
            f2.write(line)
    command = 'mv  Makefile  Makefile.old'
    os.system(command)
    command = 'mv Makefile.new  Makefile'
    os.system(command)
    #修改getIns.sh
    command = "cp  " + code_path + "/getins/getIns2.sh  " + case_path + "/Tools/getIns.sh  "
    os.system(command)
    
    #根据采样方案，进行采样
    #clean_build
    os.chdir(case_path)
    command = './' + case_name + '.' + machine + '.clean_build >> ./' + case_name + '.log 2>&1'
    os.system(command)
    # command = 'cp env_conf.xml ./LockedFiles/env_conf.xml.locked'
    # os.system(command)
    
    os.chdir(case_path + "/sampling")
    command = 'g++ get_fitdata.cpp -std="c++11" -o get_fitdata'
    os.system(command)
    command = 'g++ get_diff_module.cpp -std="c++11" -o get_diff_module'
    os.system(command)
    command = 'g++ get_function_time.cpp -std="c++11" -o get_function_time'
    os.system(command)
    
    
    count = 1
    for tmp_procs in sampling_procs:
        os.chdir(case_path)
        #cleanmach
        print('sampling: ',tmp_procs)
        tmp_items = list(tmp_procs.items())
        max_procs = max([tmp_tup[1] for tmp_tup in tmp_items])
        command = "./configure -cleanmach >> ./" + case_name + '.log 2>&1'
        os.system(command)
        #修改env_mach_pes
        env_mach_pes = parse("./env_mach_pes.xml")
        rootNode = env_mach_pes.documentElement
        entrys = rootNode.getElementsByTagName('entry')
        ntasks_atm = tmp_procs['atm']
        
        argv1 = str(count)
        for entry in entrys:
            id = entry.getAttribute('id')
            if  id[:6] == 'NTASKS':
                argv1 = argv1 + ',' + id[-3:].lower()
                if id[-3:].lower() in tmp_procs:
                    entry.setAttribute('value', str(tmp_procs[id[-3:].lower()]))
                    argv1 = argv1 + ',' + str(tmp_procs[id[-3:].lower()])
                else:
                    entry.setAttribute('value', str(max_procs))
                    argv1 = argv1 + ',' + str(max_procs)
            elif id[:4] == 'ROOT':
                entry.setAttribute('value', '0')
        argv1 = argv1 + ',' + 'cplatm' + ',' + str(max_procs)   + ',' + 'cpllnd' + ',' + str(max_procs)   + ',' + 'cplice' + ',' + str(max_procs)   + ',' + 'cplocn' + ',' + str(max_procs)   + ',' + 'cplwrf' + ',' + str(max_procs)   + ',' + 'cplglc' + ',' + str(max_procs)   + ',' + 'cplgea' + ',' + str(max_procs)   + ',' + 'none' + ',' + str(max_procs)  
        # print('argv1',argv1)
        with open("./env_mach_pes_new.xml", "w") as f:
            env_mach_pes.writexml(f, addindent='  ', encoding='utf-8')
        command = "mv  env_mach_pes.xml  env_mach_pes.xml.old"
        os.system(command)
        command = "mv  env_mach_pes_new.xml  env_mach_pes.xml"
        os.system(command)
        
        #configure -case
        command = "./configure -case >> ./" + case_name + '.log 2>&1'
        os.system(command)
        #修改atm_in
        npr_y = max_npr_yz
        npr_z = ntasks_atm
        while npr_z % npr_y != 0:
            npr_y -= 1
        npr_z = npr_z / npr_y
        npr_yz = "%d,%d,%d,%d"%(npr_y,npr_z,npr_z,npr_y)
        command='grep "'+'npr_yz" '+ case_path+'/Buildconf/cam.buildnml.csh'
        result_nl = os.system(command)
        if result_nl != 256:
            command = 'sed -i "'+'s/npr_yz[ \t]*.*/npr_yz = '+npr_yz +  '/g" ' +case_path+'/Buildconf/cam.buildnml.csh'
            os.system(command)
        
        #修改licom_in
        #修改参数: NUMBER  nx_proc ny_proc
        if os.path.exists(case_path + "/Buildconf/licom.buildnml.csh"):
            ntasks_ocn = tmp_procs['ocn']
            # nx_proc = ntasks_ocn
            # ny_proc = 1
            licom_result = []
            for j in range(14,0,-1):
                if ntasks_ocn % j == 0 and  360 % (ntasks_ocn / j) == 0:
                    licom_result.append([int(ntasks_ocn / j), j])
            if licom_result:
                nx_proc = licom_result[0][0]
                ny_proc = licom_result[0][1]
                command = 'sed -i "'+'s/NUMBER[ \t]*.*/NUMBER = '+str(ntasks_ocn) +  '/g" ' +case_path+'/Buildconf/licom.buildnml.csh'
                os.system(command)
                command = 'sed -i "'+'s/nx_proc[ \t]*.*/nx_proc = '+str(nx_proc) +  '/g" ' +case_path+'/Buildconf/licom.buildnml.csh'
                os.system(command)
                command = 'sed -i "'+'s/ny_proc[ \t]*.*/ny_proc = '+str(ny_proc) +  '/g" ' +case_path+'/Buildconf/licom.buildnml.csh'
                os.system(command)
            else:
                #ocn进程设置参数有误，报错
                assert licom_result != [], "ocn进程设置有误,无法找到合适的nx_proc, ny_proc"
        #build
        command = './' + case_name + '.' + machine +'.build > ./' + case_name + '.log 2>&1'
        os.system(command)
        
        build_count = 1
        while(os.system( 'grep -q "CCSM BUILDEXE SCRIPT HAS FINISHED SUCCESSFULLY" ' +  case_name + '.log') != 0 and build_count < 5):
            command = './' + case_name + '.' + machine +'.build > ./' + case_name + '.log 2>&1'
            os.system(command)
            build_count += 1
        #还原env_conf
        command = 'cp ./LockedFiles/env_conf.xml.locked env_conf.xml'
        os.system(command)
        #run
    ##############################
    #---set up schedulers---#
    ##############################

        #---get scheduler name---#
        ini = db_init.INI_search()[1:4]
        if ini[0] == 1:
            arch  = ['SBATCH']
        elif ini[1] == 1:
            arch  = ['PBS']
        elif ini[2] ==1:
            arch  = ['BSUB']
        else:
            print('No Scheduler specified') 
        archs          = ['PBS','SBATCH','BSUB']
        name_code      = ['-N','-J','-J']
        procs_code     = ['-n','-n','-n']
        queue_code     = ['-q','-p','-q']
        out_code       = ['-o','-o','-o']
        err_code       = ['-e','-e','-e']
        arch_rm = set(archs).difference(set(arch))

        for i in arch_rm:
            os.system('sed -i '+"'"+'/#'+i+' -/d'+"'"+' ./*.run')
        index   = archs.index(arch[0])

        #---modify case name patition name and number of procs---#
        #casename
        result = os.system('grep ' + '"'+arch[0]+' '+name_code[index]+'" '+case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1')
        if result == 0:
            command   = 'sed -i '+"'"+'s/*#'+arch[0]+' '+name_code[index]+' '+case_name+'.*/#'+arch[0]+' '+name_code[index]+' '+case_name+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
            os.system(command)

        #case patition
        if arch == 'SBATCH':
            result = os.system('grep ' + '"'+arch[0]+' '+patition_code[index]+'" '+case_name+ '.' +machine+ '.run >> ./' + case_name + '.log 2>&1')
            if result == 0:
                command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+patition_code[index]+'.*/#'+arch[0]+' '+patition_code[index]+' '+pname+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
                os.system(command)
            else:
                command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+patition_code[index]+' '+pname+'" ' + case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
                os.system(command)


    ###---mark out two sections
        
        result = os.system('grep ' + '"'+arch[0]+' '+queue_code[index]+'" '+case_name+ '.' +machine+ '.run >> ./' + case_name + '.log 2>&1')
        if result == 0:
            command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+queue_code[index]+'.*/#'+arch[0]+' '+queue_code[index]+' '+qname+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
            os.system(command)
        else:
            command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+queue_code[index]+' '+qname+'" ' + case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
            os.system(command)

            
        result = os.system('grep ' + '"'+arch[0]+' '+out_code[index]+'" '+case_name+ '.' +machine+ '.run >> ./' + case_name + '.log')
        if result == 0:
            command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+out_code[index]+'.*/#'+arch[0]+' '+out_code[index]+' '+case_path+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
            os.system(command)
        else:
            command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+out_code[index]+' '+case_path+'" ' + case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
            os.system(command)
        
        if arch[0]=='PBS':
            command   = 'ssh login1 qsub ' +case_path+ '/' +case_name + '.' + machine + '.run > '+case_path+'/'+case_name+'id.log'
        elif arch[0]=='SBATCH':    
            command   = 'sbatch ./' + case_name + '.' + machine + '.run > '+case_name+'id.log'
        else:
            command   = 'bsub ./' + case_name + '.' + machine + '.run > '+case_name+'id.log'
        os.system(command)
        #等待采样结束
        run_count = 0
        tmp_casename = case_name.split('_')[0]
        while(not os.path.exists(case_path + "/sampling/result_module/0.csv") and run_count < len(licom_result)):
            time.sleep(10)
            # case_out = os.popen('find . -maxdepth 1  -name "' + case_name + '*\.o*"').read().split("\n")[0]
            case_out = os.popen('find . -maxdepth 1  -name "' +  '*\.o*"').read().split("\n")[0]
            if case_out != '':
                tmp_value = os.system('grep -q "Model did not complete - see " ' + case_out)
                if tmp_value == 0:
                    tmp_searchresult = os.popen('grep  "Model did not complete - see " ' +case_out).read().split("\n")[0]
                    tmp_value1 = os.system('grep -q "BAD TERMINATION OF ONE OF YOUR APPLICATION PROCESSES" ' +"./build/run/ccsm.log." + tmp_searchresult[-13:])
                    command = "rm " + case_out
                    os.system(command)
                    #重新提交
                    if tmp_value1 == 0:
                        run_count += 1
                        if run_count <len(licom_result):
                            nx_proc = licom_result[run_count][0]
                            ny_proc = licom_result[run_count][1]
                            command = 'sed -i "'+'s/nx_proc[ \t]*.*/nx_proc = '+str(nx_proc) +  '/g" ' +case_path+'/Buildconf/licom.buildnml.csh'
                            os.system(command)
                            command = 'sed -i "'+'s/ny_proc[ \t]*.*/ny_proc = '+str(ny_proc) +  '/g" ' +case_path+'/Buildconf/licom.buildnml.csh'
                            os.system(command)
                            if arch[0]=='PBS':
                                command   = 'ssh login1 qsub ' +case_path+ '/' +case_name + '.' + machine + '.run > '+case_path+'/'+case_name+'id.log'
                            elif arch[0]=='SBATCH':    
                                command   = 'sbatch ./' + case_name + '.' + machine + '.run > '+case_name+'id.log'
                            else:
                                command   = 'bsub ./' + case_name + '.' + machine + '.run > '+case_name+'id.log'
                            os.system(command)
                            continue
                        else:
                            raise Exception("the number processes of the models is set incorrectly")
                    else:#抛出错误
                        raise Exception("the number processes of the models is set incorrectly")
                else:
                    tmp_value2=os.system('grep -q "SUCCESSFUL TERMINATION OF CPL7-CCSM" ' + case_out)
                    tmp_value3=os.system('grep -q "CSM EXECUTION HAS FINISHED" ' + case_out)
                    assert tmp_value2 == 0 or (tmp_value3 != 0 and tmp_value2 != 0), "the number processes of the models is set incorrectly"
                tmp_value = os.system('grep -q "BUILD_COMPLETE is not TRUE" ' +case_out)
                assert tmp_value == 256, "Build Error"
            else:
                continue
        time.sleep(15)
        command = "mv sampling/result_module  sampling/result_modules/result_module" + str(count)
        os.system(command)
        os.mkdir(case_path + "/sampling/result_module")
        count +=1
        #处理采样数据
        
        os.chdir(case_path + "/sampling")
        command = "./get_diff_module " + argv1
        os.system(command)
        command = "./get_function_time " + argv1
        os.system(command)
        
    os.chdir(case_path + "/sampling")
    argv1 = str(len(sampling_procs))
    command = "./get_fitdata " + argv1
    os.system(command)
    command = "python fit_data_processing.py"
    os.system(command)
    #拟合，写入数据库
    command = "python fit.py >/dev/null 2>&1"
    os.system(command)
    
    #整理拟合结果
    # modules =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # modules_name = ['cpl', 'atm','lnd', 'ice', 'ocn', 'glc', 'wrf', 'gea', 'cplatm', 'cpllnd', 'cplice', 'cplocn', 'cplglc', 'cplwrf', 'cplgea', 'none']
    fit_modules_name = ["atm","lnd","ice","ocn","glc","wrf","gea"]
    fit_modules_name_cp = ["atm","lnd","ice","ocn","wrf","glc","gea"]
    #通过采样数据文件大小判断算例模式分量个数, 最终fit_data计时文件大小小于1024byte的不统计
    for fit_module_name in fit_modules_name_cp:
        fit_module_path = case_path + "/sampling/fit_data/fit_data_module_" + fit_module_name + ".csv"
        file_size = os.path.getsize(fit_module_path)
        if file_size < 1024:
            fit_modules_name.remove(fit_module_name)
    fit_parameters_file = case_path + '/sampling/fit_result/fit_parameters.json'
    parameters_data = json.load(open(fit_parameters_file,'r'))
    fit_result = {}
    for submodule in fit_modules_name:
        if submodule == 'atm':
            parameters_atm = parameters_data[submodule]
            parameters_cplatm = parameters_data['cplatm']
            for key in parameters_atm:
                tmp_parameter1= parameters_atm[key]['parameter']
                tmp_parameter2= parameters_cplatm[key]['parameter']
                tmp_parameter3 = []
                for i in range(len(tmp_parameter1)):
                    tmp_parameter3.append(tmp_parameter1[i] + tmp_parameter2[i])
                parameters_atm[key]['parameter'] = tmp_parameter3
            fit_result[submodule] = str(parameters_atm)
        else:
            fit_result[submodule] = str( parameters_data[submodule])
    
    #采样数据备份
    if not os.path.exists(os.path.split(os.path.realpath(__file__))[0] + "/../backup/fit_data/"):
        os.mkdir(os.path.split(os.path.realpath(__file__))[0] + "/../backup/fit_data/")
    curr_date =time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time()))
    command = "cp -r "  + case_path + "/sampling/fit_data  "  + os.path.split(os.path.realpath(__file__))[0] + "/../backup/fit_data/" + case_name +'_' + curr_date
    os.system(command)
    #删除算例
    # command = "rm -rf " +  case_path
    # os.system(command)
    return fit_result
# case_path = '/public/home/thudess6/liuyao/pljiao/function_level/uq/casesm_cases/case_jpl_6'
# machine = 'hygon_intel'
# case_name = 'case_jpl_6'
# netcdf_path = '/public/home/thudess6/liuyao/pljiao/netcdf2/install2'
# model_path = '/public/home/thudess6/uq/CAS-ESM/'
# sampling_procs = [4,8,16,32,64,96,128,256,512]
# qname = 'front'
# sampling(case_path, machine, netcdf_path, model_path, case_name,sampling_procs,qname)
