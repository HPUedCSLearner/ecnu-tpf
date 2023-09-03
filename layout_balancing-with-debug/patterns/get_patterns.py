import sys
import csv
import math
import numpy as np
from numpy import zeros, newaxis
import re

def flip90_left(arr):
    new_arr = np.transpose(arr)
    new_arr = new_arr[::-1]
    return new_arr

def flip90_right(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    new_arr = np.transpose(new_arr)[::-1]
    return new_arr


def check_expand(tmp_arr, currMod, table_len, y_pos, x_pos):
    res_offset = -1
    length = len(tmp_arr)
    for y_idx in range(length):
        if x_pos-1>=0 and tmp_arr[y_pos][x_pos-1]==currMod:# and y_idx >= y_pos:
            if tmp_arr[y_idx][x_pos]==0 and x_pos-1>=0 and tmp_arr[y_idx][x_pos-1]==currMod:
                res_offset += 1
            else:
                if tmp_arr[y_idx][x_pos]!=0 and x_pos-1>=0 and tmp_arr[y_idx][x_pos-1]==currMod:
                    return -1
    return res_offset
    
    
def expand_horizon(tmp_arr, numModules, pos_dict, table_len):
    itemindex = np.where(tmp_arr==0)
    for i_pos in range(len(itemindex[0])):
        y_pos = itemindex[0][i_pos]
        x_pos = itemindex[1][i_pos]
        if tmp_arr[y_pos][x_pos] == 0:
            for i in range(1, numModules+1):
                offset = check_expand(tmp_arr, i, table_len, y_pos, x_pos)
                if offset != -1:
                    for i_offset in range(offset+1):
                        tmp_arr[y_pos+i_offset][x_pos] = i

def expand_getrelation(pattern_list, table_len, numModules):
    result = []
    dup_flag = 0
    dup_flag_1 = 0
    dup_flag_2 = 0
    cott = 0

    for each_pattern in pattern_list:
        pos_dict = {}
        
        up_most = each_pattern.reshape(1, table_len*table_len)
        bot_most = each_pattern[::-1].reshape(1, table_len*table_len)
        left_most = flip90_right(each_pattern).reshape(1, table_len*table_len)
        right_most = flip90_left(each_pattern).reshape(1, table_len*table_len)
        
        up_bound = np.nonzero(up_most)[1][0]//table_len
        bot_bound = table_len - np.nonzero(bot_most)[1][0]//table_len - 1
        left_bound = np.nonzero(left_most)[1][0]//table_len
        right_bound = table_len - np.nonzero(right_most)[1][0]//table_len - 1

        tmp_arr = np.empty(shape=[0, right_bound-left_bound+1])
        for y in range(table_len):
            if y>=up_bound and y<= bot_bound:
                tmp_arr = np.append(tmp_arr, np.array([each_pattern[y][left_bound:right_bound+1]]), axis=0)

        for i in range(1, numModules+1):
            itemindex = np.where(tmp_arr==i)
            pos_dict[i] = [(itemindex[0][0], itemindex[1][0])]
        
        # expand horizon
        expand_horizon(tmp_arr, numModules, pos_dict, table_len)
        tmp_arr = flip90_right(flip90_right(tmp_arr))
        pos_dict = {}
        for i in range(1, numModules+1):
            itemindex = np.where(tmp_arr==i)
            pos_dict[i] = [(itemindex[0][0], itemindex[1][0])]
        expand_horizon(tmp_arr, numModules, pos_dict, table_len)

        # expand verticality

        tmp_arr = flip90_right(tmp_arr)
        pos_dict = {}
        for i in range(1, numModules+1):
            itemindex = np.where(tmp_arr==i)
            pos_dict[i] = [(itemindex[0][0], itemindex[1][0])]
        expand_horizon(tmp_arr, numModules, pos_dict, table_len)

        tmp_arr = flip90_right(flip90_right(tmp_arr))
        pos_dict = {}
        for i in range(1, numModules+1):
            itemindex = np.where(tmp_arr==i)
            pos_dict[i] = [(itemindex[0][0], itemindex[1][0])]
        expand_horizon(tmp_arr, numModules, pos_dict, table_len)
        tmp_arr = flip90_left(tmp_arr)
        
        # get relationship
        tmp_res = []
        for each_row in tmp_arr:
            dup_flag = 0
            tmp_tuple = tuple(np.unique(each_row))
            for each_row in tmp_res:
                if (each_row == tmp_tuple):
                    dup_flag = 1
            if dup_flag == 0:
                tmp_res.append(tmp_tuple)
         
        # check duplicate
        if len(result) == 0:
            result.append(tmp_res)
        else:
            dup_flag_2 = 0
            for list_idx, each_list in enumerate(result):
                if len(each_list) == len(tmp_res):
                    dup_flag_1 = 0
                    for each_tuple in each_list:
                        if each_tuple not in tmp_res:
                            dup_flag_1 = 1
                    if dup_flag_1 == 1:
                        result.append(tmp_res)
                        break
                else:
                    dup_flag_2 += 1
            if dup_flag_2 == len(result):
                result.append(tmp_res) 

    return result

def get_patterns(numModules):

    table_len = numModules*4
    pattern_list = np.load("pattern_list_" + str(numModules) + ".npy")

    new_pattern_list = expand_getrelation(pattern_list, table_len, numModules)
    f = open('pattern_' + str(numModules) + '.out','w')
    result = set()
    for pattern in new_pattern_list:
        tmp_arr = str(pattern)
        if re.search('0.0', tmp_arr):
            continue
        #统计含有在不同并行tuple内各module出现次数， 出现次数 > 1且小于nummodules的module数仅限一个
        tmp_count = np.zeros(numModules)
        for part_touple in pattern:
            for i in part_touple:
                tmp_count[int(i)-1] += 1
        model_count = 0 
        for c in tmp_count:
            if c > 1 and c != len(pattern):
                model_count += 1
        if model_count < 1:
        #pattern排序
            counts = {}
            for i in range(numModules):
                counts[i+1] = 0
                
            for pattern_touple in pattern:
                for i in pattern_touple:
                    counts[int(i)]  += 1
            # counts_order = sorted(counts.items(),key=lambda x:x[1],reverse=True)
            # print(counts_order)
            pattern_new = set()
            for pattern_touple in pattern:
                tmp_order = {}
                for i in pattern_touple:
                    tmp_order[int(i)] = counts[int(i)]
                tmp_order = sorted(tmp_order.items(),key=lambda x:x[1],reverse=True)
                #提取排序后的module
                tmp_new = []
                for tmp in tmp_order:
                    tmp_new.append(tmp[0])
                tuple_new = tuple(tmp_new)
                pattern_new.add(tuple_new)
                #检查重复
                #针对不同touple中的最小值进行排序
                # pattern_new = sorted(pattern_new, key=lambda x: x[0])
            
            
            #改为默认排布：atm : 1, ocn: 2, lnd : 3, ice : 4, 其他：5、6、......
            result.add(frozenset(pattern_new))
        

    tmp_len = len(result)
    count = 0
    for i in result:
        f.write(str(list(i)))
        count+=1
        if count == tmp_len:
            continue
        else:
            f.write("\n")
    f.close
    np.save("pattern_" + str(numModules) + ".npy", new_pattern_list)

    return

if __name__ == "__main__":
    numModules = int(sys.argv[1])
    get_patterns(numModules)