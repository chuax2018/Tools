import os
import sys
Python3 = True
if sys.version_info[0] < 3:
    Python3 = False


def get_dict(fileData, key_position, Separator = ",", use_list_not_whole_line = True, key_conflict_check = False):
    lines = []
    if isinstance(fileData, str):
        lines = open(fileData, "r", encoding='utf-8').readlines()
    elif isinstance(fileData, list):
        lines = fileData

    dict ={}
    fail =False

    if key_conflict_check:
        for line in lines:
            line_list = line.strip("\n").split(Separator)

            if len(line_list) <= key_position:
                fail =True
                break

            if Python3:
                if dict.__contains__(line_list[key_position]):
                    print("err: different line contains the same key(%s) !" % line_list[key_position])
                    fail = True
                    break
            else:
                if dict.has_key(line_list[key_position]):
                    print("err: different line contains the same key(%s) !" % line_list[key_position])
                    fail = True
                    break

            if use_list_not_whole_line:
                dict[line_list[key_position]] = line_list
            else:
                dict[line_list[key_position]] = line

        if fail is False:
            return dict
        else:
            return None
    else:
        for line in lines:
            line_list = line.strip("\n").split(Separator)

            if len(line_list) <= key_position:
                fail = True
                break

            if Python3:
                if use_list_not_whole_line:
                    if dict.__contains__(line_list[key_position]):
                        dict.get(line_list[key_position]).append(line_list)
                    else:
                        temp_list = []
                        temp_list.append(line_list)
                        dict[line_list[key_position]] = temp_list
                else:
                    if dict.__contains__(line_list[key_position]):
                        dict.get(line_list[key_position]).append(line)
                    else:
                        temp_list = []
                        temp_list.append(line)
                        dict[line_list[key_position]] = temp_list
            else:
                if use_list_not_whole_line:
                    if dict.has_key(line_list[key_position]):
                        dict.get(line_list[key_position]).append(line_list)
                    else:
                        temp_list = []
                        temp_list.append(line_list)
                        dict[line_list[key_position]] = temp_list
                else:
                    if dict.has_key(line_list[key_position]):
                        dict.get(line_list[key_position]).append(line)
                    else:
                        temp_list = []
                        temp_list.append(line)
                        dict[line_list[key_position]] = temp_list
        if fail is False:
            return dict
        else:
            return None
