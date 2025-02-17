# very simple prototype that I wrote as an implementation for leet-index, hope you enjoy!

import argparse
import glob
import os
import time
from datetime import datetime
import math

# get num of lines in a file
def get_num_lines(filename):
    file = open(filename, 'r', encoding="utf-8")
    content = file.read()
    return content.count('\n')

def get_lines_of_code(dirs, exts, excl):
    total_lines = 0

    for x in dirs:
        if not os.path.isdir(x):
            print(x, "is not a valid directory")
            exit()
        for k in exts:
            for q in glob.glob(x + "/**/*." + k, recursive=True):
                # print(q)
                skip = False
                for e in excl:
                    if(e == q):
                        print(e)
                        skip = True
                
                if(not skip):
                    total_lines += get_num_lines(q)

    return total_lines

def get_streak():
    cur_streak = 1

    if not os.path.isfile("./leet-data.txt"):
        return cur_streak
        
    f = open("leet-data.txt", 'r')
    dates = []

    for x in f:
        cur_date = x.replace(']', '').split(',')[1].strip()
        already_exists = False

        for k in dates:
            if(cur_date == k):
                already_exists = True
        
        if(not already_exists):
            dates.append(cur_date)

    if(len(dates) == 1):
        #I couldnt subtract a strftime obj by strptime so we're ust gonna make it strptime
        date_obj = datetime.strptime(datetime.now().strftime("%y-%m-%d"), "%y-%m-%d")
        date_prev_obj = datetime.strptime(dates[0], "%y-%m-%d")

        if (date_obj - date_prev_obj).days == 1:
            cur_streak += 1
        print(cur_streak)
    
    for i in range(len(dates)-1, -1, -1):
        date_obj = datetime.strptime(dates[i], "%y-%m-%d")
        date_prev_obj = datetime.strptime(dates[i-1], "%y-%m-%d")

        if (date_obj - date_prev_obj).days == 1:
            cur_streak += 1
        else:
            break

    return cur_streak

get_streak()

# get data from leet-config.txt and put into dirs & exts
def parse_config():
    dirs = []
    exts = []
    excl = []

    if not os.path.isfile("./leet-config.txt"):
        print("no config! make sure you ran --get")
        exit()

    f = open("leet-config.txt", 'r')

    for line in f:
        if line.startswith("directories:"):
            dirs = line.replace("directories:", "").strip().split(',')
        elif line.startswith("extensions:"):
           exts = line.replace("extensions:", "").strip().split(',')
        elif line.startswith("excludes:"):
            excl = line.replace("excludes:", "").strip().split(',')
    
    return dirs, exts, excl

parser = argparse.ArgumentParser("leet-index")
parser.add_argument('--start', action='store_true', help="start tracking work session")
parser.add_argument('--stop', action='store_true', help="stop tracking work session data and export to file")
parser.add_argument('--get', action='store_true', help="generate leet-index config file, directories and extensions are seperated by a comma dont use newlines")
args = parser.parse_args()

if(args.get):
    if not os.path.isfile("./leet-config.txt"):
        file = open("leet-config.txt", 'a')
        file.write("# be careful when setting directories as leet-index recursively globs them, example input: extensions:hpp,cpp, exclude currently only works for files\n")
        file.write("directories:\n")
        file.write("extensions:\n")
        file.write("excludes:\n")
    else:
        print("leet-config already exists")

if(args.start):
    if not os.path.isfile("./leet-config.txt"):
        print("failed to find leet-config.txt, make sure you generate and update before starting session")
        exit()

    if os.path.isfile("./leet-temp.txt"):
        print("timer has already been started, please stop it before starting a new session")
        exit()
    
    dirs, exts, excl = parse_config()
    total_lines = get_lines_of_code(dirs, exts, excl)

    f = open("leet-temp.txt", 'w')
    f.write("dont delete this file while in session!\n")
    f.write(str.format("lines of code:{}\n", total_lines))
    f.write(str.format("epoch time:{}", round(time.time())))
    print("successfully started timer!")

if(args.stop):
    if not os.path.isfile("./leet-temp.txt"):
        print("no data! are you sure you started a timer?")
        exit()
    
    dirs, exts, excl = parse_config()
    total_lines = get_lines_of_code(dirs, exts, excl)
    epoch_time = time.time()
    start_total_lines = 0
    start_epoch_time = 0
    dff_total_lines = 0
    diff_epoch_time = 0
    leet_index = 0

    f = open("leet-temp.txt", 'r')

    for line in f:
        if line.startswith("lines of code:"):
            start_total_lines = int(line.replace("lines of code:", "").strip())
        
        if line.startswith("epoch time:"):
            start_epoch_time = int(line.replace("epoch time:", "").strip())

    diff_total_lines = total_lines - start_total_lines
    diff_epoch_time = epoch_time - start_epoch_time

    # converting the time from seconds to hours
    diff_epoch_time = (diff_epoch_time/60)/60

    # if its been less than an hour, multiply by time rather than div otherwise we will get some outrageously high number
    if(1 > diff_epoch_time):
        leet_index = round(diff_total_lines * diff_epoch_time, 1)
    else:
        leet_index = round(diff_total_lines/diff_epoch_time, 1)
    
    date = datetime.now().strftime("%A, %y-%m-%d")
    streak = get_streak()

    if streak > 1:
        data = str.format("[leet-index:{} | lines of code:{} | time spent:{}h | streak:{}d | date: {}]\n", leet_index, diff_total_lines, round(diff_epoch_time, 1), streak, date)
    else:
        data = str.format("[leet-index:{} | lines of code:{} | time spent:{}h | date: {}]\n", leet_index, diff_total_lines, round(diff_epoch_time, 1), date)

    d = open('leet-data.txt', 'a')
    d.write(data)
    f.close()
    os.remove("leet-temp.txt")
    print("successfully ended session! heres the stats:\n", data)