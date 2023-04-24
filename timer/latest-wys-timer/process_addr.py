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

objexe = sys.argv[1]
objdumpfile = objexe  + '.singal'
grepedfile = objexe  + '.greped'
colon_free_file = objexe  + '.colonfree'
terminal_file = objexe + '.terminal'


print('will processing ' + objexe + ' ......')
command = 'objdump -d' + ' ' + objexe + ' ' + '>' + ' ' + objdumpfile
os.system(command)


print('will processing ' + grepedfile + ' ......')
command = 'grep -rin' + ' ' + '">:"' + ' ' + objdumpfile + ' ' + '>' + ' ' + grepedfile
os.system(command)

print('will processing ' + colon_free_file + ' ......')
command = 'sed "s/:/ /g"' + ' ' + grepedfile + ' ' + '>' + ' ' + colon_free_file
os.system(command)

command = 'sed "s/>/ /g"' + ' ' + colon_free_file  + ' ' + '-i'
os.system(command)
command = 'sed "s/</ /g"' + ' ' + colon_free_file  + ' ' + '-i'
os.system(command)


command = 'sed "s/0000*0/0x/g"' + ' ' + colon_free_file + ' ' + '-i'
os.system(command)



print('will processing ' + terminal_file + ' ......')
command = "awk '{print $2,$3}'" + ' ' + colon_free_file + ' ' + '>' + ' ' + terminal_file
os.system(command)

print('will processing ' + objexe + ' down')







