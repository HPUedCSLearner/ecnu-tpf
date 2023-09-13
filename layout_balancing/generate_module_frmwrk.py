# https://blog.csdn.net/m0_51971452/article/details/111701927
# python json 文件读写

import json

module_frmwrk = {}
module_num = ['cpl', 'atm', 'lnd', 'ice', 'ocn']
max_process_num = 1024
start_process_num = 1
module_process_val = 666
module_frmwrk_file = 'trans_fit_parameters.json'

for module in module_num:
    module_frmwrk[module] = {}
    while start_process_num <= max_process_num:
        # module_frmwrk[module][start_process_num] = max_process_num - start_process_num + 2
        module_frmwrk[module][start_process_num] = 1 / start_process_num
        start_process_num += 1
    start_process_num = 1

# for debug
# print(module_frmwrk)

# trans json format for looks easy
json_data = json.dumps(module_frmwrk, sort_keys=True, indent=4, separators=(',', ': '))

# for debug
# print(json_data)

# write json format data to file
with open(module_frmwrk_file, 'w') as write_f:
	write_f.write(json_data)

