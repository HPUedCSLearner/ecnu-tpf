import os

with open( './Macros', 'r') as macros_old, open('./Macros' + ".new", 'w') as macros_new:
        for line in macros_old:
            if re.match(r'\s*FFLAGS\s*:=', line):
                line = line.strip() + ' -g -finstrument-functions -mcmodel=medium \n'
                #line = line
            elif re.search(r'-o $(EXEC_SE)', line):
                print line
            macros_new.write(line)
    command = "mv" + ' Macros' + ' Macros' + '.previous'
    os.system(command)
    command = 'mv' + ' Macros' + '.new' + ' Macros'
    os.system(command)
