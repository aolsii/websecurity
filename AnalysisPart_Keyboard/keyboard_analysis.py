#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analysing the keyboard password mode of the CSDN and Yahoo data sets.
The analysis results consist of keyboard password dataset, pattern matched result.
"""

import re
import sys
import numpy as np


def read_csdn_data(password_file):
    '''
    读取CSDN数据集
    '''
    user_list = []
    password_list = []
    mail_list = []

    print("Reading CSDN data...")
    f = open(password_file, 'r', encoding="ISO-8859-1")
    for line in f:
        user_list.append(line.split(" # ")[0])
        password_list.append(line.split(" # ")[1])
        mail_list.append(line.split(" # ")[2][:-1])
    f.close()

    return user_list, password_list, mail_list


def read_yahoo_data(password_file):
    '''
    读取Yahoo数据集
    '''
    mail_list = []
    password_list = []

    print("Reading Yahoo data...")
    line_count = 0
    f = open(password_file, 'r', encoding="ISO-8859-1")
    for line in f:
        line_count += 1
        if len(line.split(":")) == 3:
            mail_list.append(line.split(":")[1])
            password_list.append(line.split(":")[2][:-1])
    f.close()

    return password_list, mail_list


def longest_common_substring(pattern, password):
    '''
    匹配口令与键盘模式的最长公共子串
    '''
    dp = [[0 for j in range(len(pattern) + 1)] for i in range(len(password) + 1)]

    max_longth = -1
    string_end = -1

    # 动态规划并标记最大长度回溯求取最长子串
    for i in range(1, len(password) + 1):
        for j in range(1, len(pattern) + 1):
            if password[i-1] == pattern[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            if dp[i][j] > max_longth:
                max_longth = dp[i][j]
                string_end = i

    longest_common_string = password[string_end - max_longth:string_end]

    return max_longth, longest_common_string, string_end


def keyboard_hobby_analyse(password, result_filename, dataset_filename):
    '''
    按键盘模式分析口令的键盘关键字概率分布
    '''
    # 键盘模式下的14种模式分析
    # 0-3 first keyboard line
    # 4-7 second keyboard line
    # 8-11 third keyboard line
    # 12-15 fourth keyboard line
    # 16-19 left little finger
    # 20-23 left ring finger
    # 24-27 left middle finger
    # 28-31 left index finger
    # 32-35 right index finger
    # 36-39 right middle finger
    # 40-43 right ring finger
    # 44-47 right little finger
    # 48-53 little keyboard
    # 54-57 26 English characters
    # 58-101 Reverse fingering order
    # 102-107 Random keyboard line combination

    pattern = [
        "`1234567890-=",
        "=-0987654321`",
        "~!@#$%^&*()_+",
        "+_)(*&^%$#@!~",

        "qwertyuiop[]\\",
        "\\][poiuytrewq",
        "QWERTYUIOP{}|",
        "|}{POIUYTREWQ",

        "asdfghjkl;\'",
        "\';lkjhgfdsa",
        "ASDFGHJKL:\"",
        "\":LKJHGFDSA",

        "zxcvbnm,./",
        "/.,mnbvcxz",
        "ZXCVBNM<>?",
        "?><MNBVCXZ",

        "`1qaz",
        "zaq1`",
        "~!QAZ",
        "ZAQ!~",
        
        "2wsx",
        "xsw2",
        "@WSX",
        "XSW@",

        "3edc",
        "cde3",
        "#EDC",
        "CDE#",

        "4rfv5tgb",
        "bgt5vfr4",
        "$RFV%TGB",
        "BGT%VFR$",

        "6yhn7ujm",
        "mju7nhy6",
        "^YHN&UJM",
        "MJU&NHY^",

        "8ik,",
        ",ki8",
        "*IK<",
        "<KI*",

        "9ol.",
        ".lo9",
        "(OL>",
        ">LO(",

        "0p;/-['=]\\",
        "\\]='[-/;p0",
        ")P:?_{\"+}|",
        "|}+\"{_?:P)",
        
        "0147",
        "7410",
        "0258",
        "8520",
        ".369",
        "963.",

        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",

        "`12q3wa",
        "aw3q21`",
        "~!@Q#WA",
        "AW#Q@!~",

        "zse4",
        "4esz",
        "ZSE$",
        "$ESZ",

        "xdr5",
        "5rdx",
        "XDR%",
        "%RDX",

        "cft6",
        "6tfc",
        "CFT^",
        "^TFC",

        "vgy7",
        "7ygv",
        "VGY&",
        "&YGV",

        "bhu8",
        "8uhb",
        "BHU*",
        "*UHB",

        "nji9",
        "9ijn",
        "NJI(",
        "(IJN",

        "mko0",
        "0okm",
        "MKO)",
        ")OKM",

        ",lp-",
        "-pl,",
        "<LP_",
        "_PL<",

        ".;[=",
        "=[;.",
        ">:{+",
        "+{:>",

        "/']\\",
        "\\]'/",
        "?\"}|",
        "|}\"?",

        "1q2w3e4r5t6y7u8i9o0p",
        "1Q2W3E4R5T6Y7U8I9O0P",
        "1a2s3d4f5g6h7j8k9l0;",
        "1A2S3D4F5G6H7J8K9L0;",
        "1z2x3c4v5b6n7m8,9.0/",
        "1Z2X3C4V5B6N7M8,9.0/"
    ]

    print("Keyboard hobby analyse...")
    keyword_dict = {
        "first keyboard line": {},
        "second keyboard line": {},
        "third keyboard line": {},
        "fourth keyboard line": {},
        "left little finger": {},
        "left ring finger": {},
        "left middle finger": {},
        "left index finger": {},
        "right index finger": {},
        "right middle finger": {},
        "right ring finger": {},
        "right little finger": {},
        "little keyboard": {},
        "26 English characters": {},
        "Reverse fingering order": {},
        "Random keyboard line combination": {}
    }

    # 存储含有键盘模式的键盘口令数据集
    print("Genearting keyboard password dataset...")
    f = open(dataset_filename, "w", encoding="ISO-8859-1")

    # 标志当前口令是否已匹配到键盘模式
    password_flag = [0 for i in range(len(password))]

    for mode_number in range(0, len(pattern)):
        print("Mode %s is analysing..." % mode_number)
        password_index = 0
        for password_element in password:

            # “最长公共子串”模式匹配寻找关键字
            longest_len, longest_common_string, string_end = longest_common_substring(pattern[mode_number], password_element)

            # 保留关键字长度大于3的所有口令及关键字
            if longest_len >= 3:
                if password_flag[password_index] == 0:
                    f.writelines(password_element + " \\ " + str(string_end-longest_len) + " \\ " + str(string_end) + "\n")
                    password_flag[password_index] = 1

                if 0 <= mode_number <= 3:
                    if longest_common_string in keyword_dict["first keyboard line"].keys():
                        keyword_dict["first keyboard line"][longest_common_string] += 1
                    else:
                        keyword_dict["first keyboard line"][longest_common_string] = 1
                elif 4 <= mode_number <= 7:
                    if longest_common_string in keyword_dict["second keyboard line"].keys():
                        keyword_dict["second keyboard line"][longest_common_string] += 1
                    else:
                        keyword_dict["second keyboard line"][longest_common_string] = 1
                elif 8 <= mode_number <= 11:
                    if longest_common_string in keyword_dict["third keyboard line"].keys():
                        keyword_dict["third keyboard line"][longest_common_string] += 1
                    else:
                        keyword_dict["third keyboard line"][longest_common_string] = 1
                elif 12 <= mode_number <= 15:
                    if longest_common_string in keyword_dict["fourth keyboard line"].keys():
                        keyword_dict["fourth keyboard line"][longest_common_string] += 1
                    else:
                        keyword_dict["fourth keyboard line"][longest_common_string] = 1
                elif 16 <= mode_number <= 19:
                    if longest_common_string in keyword_dict["left little finger"].keys():
                        keyword_dict["left little finger"][longest_common_string] += 1
                    else:
                        keyword_dict["left little finger"][longest_common_string] = 1
                elif 20 <= mode_number <= 23:
                    if longest_common_string in keyword_dict["left ring finger"].keys():
                        keyword_dict["left ring finger"][longest_common_string] += 1
                    else:
                        keyword_dict["left ring finger"][longest_common_string] = 1
                elif 24 <= mode_number <= 27:
                    if longest_common_string in keyword_dict["left middle finger"].keys():
                        keyword_dict["left middle finger"][longest_common_string] += 1
                    else:
                        keyword_dict["left middle finger"][longest_common_string] = 1
                elif 28 <= mode_number <= 31:
                    if longest_common_string in keyword_dict["left index finger"].keys():
                        keyword_dict["left index finger"][longest_common_string] += 1
                    else:
                        keyword_dict["left index finger"][longest_common_string] = 1
                elif 32 <= mode_number <= 35:
                    if longest_common_string in keyword_dict["right index finger"].keys():
                        keyword_dict["right index finger"][longest_common_string] += 1
                    else:
                        keyword_dict["right index finger"][longest_common_string] = 1
                elif 36 <= mode_number <= 39:
                    if longest_common_string in keyword_dict["right middle finger"].keys():
                        keyword_dict["right middle finger"][longest_common_string] += 1
                    else:
                        keyword_dict["right middle finger"][longest_common_string] = 1
                elif 40 <= mode_number <= 43:
                    if longest_common_string in keyword_dict["right ring finger"].keys():
                        keyword_dict["right ring finger"][longest_common_string] += 1
                    else:
                        keyword_dict["right ring finger"][longest_common_string] = 1
                elif 44 <= mode_number <= 47:
                    if longest_common_string in keyword_dict["right little finger"].keys():
                        keyword_dict["right little finger"][longest_common_string] += 1
                    else:
                        keyword_dict["right little finger"][longest_common_string] = 1
                elif 48 <= mode_number <= 53:
                    if longest_common_string in keyword_dict["little keyboard"].keys():
                        keyword_dict["little keyboard"][longest_common_string] += 1
                    else:
                        keyword_dict["little keyboard"][longest_common_string] = 1
                elif 54 <= mode_number <= 57:
                    if longest_common_string in keyword_dict["26 English characters"].keys():
                        keyword_dict["26 English characters"][longest_common_string] += 1
                    else:
                        keyword_dict["26 English characters"][longest_common_string] = 1
                elif 58 <= mode_number <= 101:
                    if longest_common_string in keyword_dict["Reverse fingering order"].keys():
                        keyword_dict["Reverse fingering order"][longest_common_string] += 1
                    else:
                        keyword_dict["Reverse fingering order"][longest_common_string] = 1
                elif 102 <= mode_number <= 107:
                    if longest_common_string in keyword_dict["Random keyboard line combination"].keys():
                        keyword_dict["Random keyboard line combination"][longest_common_string] += 1
                    else:
                        keyword_dict["Random keyboard line combination"][longest_common_string] = 1

            password_index += 1

    f.close()

    # 生成键盘模式下关键字概率分析结果
    print("Generating pattern matched result...")
    f = open(result_filename, "w")
    f.writelines("Number \ Keywords \ Quantity \ Percentage")
    total = len(password)
    for mode_keyword in keyword_dict.keys():

        f.writelines("\n" + "# " + mode_keyword + "\n")
        sort_list = sorted(keyword_dict[mode_keyword].items(), key=lambda item: item[1])

        for i in range(1, len(sort_list) + 1):
            f.writelines(str(i) + " \\ " + str(sort_list[len(sort_list) - i][0]) + " \\ " + str(sort_list[len(sort_list) - i][1])
                         + " \\ " + str(sort_list[len(sort_list) - i][1]/total) + "\n")
    f.close()


if __name__ == "__main__":
    '''
    主程序入口
    '''

    # 口令原始数据库
    csdn_data_path = "www.csdn.net.sql"
    yahoo_data_path = "plaintxt_yahoo.txt"

    # 含有键盘模式的口令数据库
    csdn_keyboard_password_dataset_path = "csdn_keyboard_password_dataset.txt"
    yahoo_keyboard_password_dataset_path = "yahoo_keyboard_password_dataset.txt"

    # 键盘关键字概率分布结果
    csdn_keyboard_keyword_dataset_path = "csdn_keyboard_analyse_result.txt"
    yahoo_keyboard_keyword_dataset_path = "yahoo_keyboard_analyse_result.txt"

    csdn_user, csdn_password, csdn_mail = read_csdn_data(csdn_data_path)
    yahoo_password, yahoo_mail = read_yahoo_data(yahoo_data_path)

    keyboard_hobby_analyse(csdn_password, csdn_keyboard_keyword_dataset_path, csdn_keyboard_password_dataset_path)
    keyboard_hobby_analyse(yahoo_password, yahoo_keyboard_keyword_dataset_path, yahoo_keyboard_password_dataset_path)
    
    print("Password analysis finished!")
	