import sys
import os
import csv
import math
import numpy as np
import copy
from numpy import zeros, newaxis
import re




def check_valid(table, check_table, width, currX, currY):
    # left up
    if currX>=0 and currX<width and currY>=0 and currY<width and table[currY][currX]==0 and check_table[currY][currX]==0:
        pass
    else:
        return False
    # right up
    if currX+1>=0 and currX+1<width and currY>=0 and currY<width and table[currY][currX+1]==0 and check_table[currY][currX+1]==0:
        pass
    else:
        return False
    # left down
    if currX>=0 and currX<width and currY+1>=0 and currY+1<width and table[currY+1][currX]==0 and check_table[currY+1][currX]==0:
        pass
    else:
        return False
    # right down
    if currX+1>=0 and currX+1<width and currY+1>=0 and currY+1<width and table[currY+1][currX+1]==0 and check_table[currY+1][currX+1]==0:
        pass
    else:
        return False

    return True

def x_axis_symm(base_table, each_table):
    y_len = len(base_table)
    x_len = len(base_table[0])
    for j in range(y_len):
        for i in range(x_len):
            if base_table[j][i] != each_table[y_len-j-1][i]:
                return True
    return False

def y_axis_symm(base_table, each_table):
    y_len = len(base_table)
    x_len = len(base_table[0])
    for j in range(y_len):
        for i in range(x_len):
            if base_table[j][i] != each_table[j][x_len-i-1]:
                return True
    return False

def check_NOexist_NOduplicate(base_table, pattern_list):
    for each_table in pattern_list:
        if (base_table == each_table).all():
            return False
        # 90
        elif (np.rot90(base_table, 1) == each_table).all():
            return False
        # 180
        elif (np.rot90(base_table, 2) == each_table).all():
            return False
        # 270
        elif (np.rot90(base_table, 3) == each_table).all():
            return False
        # x-axis symmetric
        elif x_axis_symm(base_table, each_table) == False:
            return False
        # y-axis symmetric
        elif y_axis_symm(base_table, each_table) == False:
            return False
        else:
            continue
    return True

def generate_patterns(numModules, idx, base_table, check_table, pattern_list, table_len, currX, currY):
    if idx == 2:
        print(idx)
    local_base_table = copy.deepcopy(base_table)
    local_check_table = copy.deepcopy(check_table)
    if idx == numModules+1:
        # try:
        # if np.all(base_table not in pattern_list):
        #     pattern_list.append(base_table)
        # except:
        #     print(base_table)
        if check_NOexist_NOduplicate(local_base_table, pattern_list):
            pattern_list.append(base_table)
        return 

    if local_base_table[currY][currX]==0 and local_base_table[currY][currX+1]==0 and local_base_table[currY+1][currX]==0 and local_base_table[currY+1][currX+1]==0:
        local_base_table[currY][currX] = idx
        local_base_table[currY][currX+1] = idx
        local_base_table[currY+1][currX] = idx
        local_base_table[currY+1][currX+1] = idx
        local_check_table[currY][currX] = -1
        local_check_table[currY][currX+1] = -1
        local_check_table[currY+1][currX] = -1
        local_check_table[currY+1][currX+1] = -1
    else:
        return

    # print(base_table)

    # uppercheck
    if check_valid(local_base_table, local_check_table, table_len, currX-1, currY-2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX-1, currY-2)
    if check_valid(local_base_table, local_check_table, table_len, currX, currY-2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX, currY-2)
    if check_valid(local_base_table, local_check_table, table_len, currX+1, currY-2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX+1, currY-2)
    
    # lowercheck
    if check_valid(local_base_table, local_check_table, table_len, currX-1, currY+2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX-1, currY+2)
    if check_valid(local_base_table, local_check_table, table_len, currX, currY+2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX, currY+2)
    if check_valid(local_base_table, local_check_table, table_len, currX+1, currY+2) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX+1, currY+2)

    # leftcheck
    if check_valid(local_base_table, local_check_table, table_len, currX-2, currY+1) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX-2, currY+1)
    if check_valid(local_base_table, local_check_table, table_len, currX-2, currY) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX-2, currY)
    if check_valid(local_base_table, local_check_table, table_len, currX-2, currY-1) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX-2, currY+1)

    # rightcheck
    if check_valid(local_base_table, local_check_table, table_len, currX+2, currY+1) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX+2, currY+1)
    if check_valid(local_base_table, local_check_table, table_len, currX+2, currY) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX+2, currY)
    if check_valid(local_base_table, local_check_table, table_len, currX+2, currY-1) is True:
        generate_patterns(numModules, idx+1, local_base_table, local_check_table, pattern_list, table_len, currX+2, currY+1)

    return

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

# def check_result(new_pattern_list):
    # result = set()
    # for pattern in new_pattern_list:
        # tmp_str = str(pattern)
        # if not re.search('0.0', tmp_str):
            # result.add(tmp_str)
    # print(result)
    # return result

def get_patterns(numModules):

    table_len = numModules*4
    # base_table = np.zeros((table_len, table_len))
    # check_table = np.zeros((table_len, table_len))
    # pattern_list = []
    # generate_patterns(numModules, 1, base_table, check_table, pattern_list, table_len, table_len//2-1, table_len//2-1)
    # pattern_list = np.array(pattern_list)
    # np.save("pattern_list_" + str(numModules) + ".npy", pattern_list)
    # f = open("pattern_3.log", 'w')
    # print(pattern_list, file = f)
    # f.close
    pattern_list = np.load("pattern_list_" + str(numModules) + ".npy")
    # print(pattern_list[93,:,:], file = f)
    # f.close、
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
            pattern_new = []
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
                pattern_new.append(tuple_new)
            
            #检查重复
            #改为默认排布：atm : 1, ocn: 2, lnd : 3, ice : 4, 其他：5、6、......
            result.add(str(pattern_new))
        
    # for i in range(len(result)):
        # if i != len(result):
            # f.write(result[i] + "\n")
        # else:
            # f.write(result[i])
    tmp_len = len(result)
    count = 0
    for i in result:
        f.write(i)
        count+=1
        if count == tmp_len:
            continue
        else:
            f.write("\n")
    f.close
    np.save("pattern_" + str(numModules) + ".npy", new_pattern_list)
    #print("------------------------")
    # print(new_pattern_list,file = f)
    # f.close
    # print("------------------------")
    return

if __name__ == "__main__":
    numModules = int(sys.argv[1])
    get_patterns(numModules)