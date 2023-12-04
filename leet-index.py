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

def get_lines_of_code(dirs, exts):
    total_lines = 0
    for x in dirs:
        if not os.path.isdir(x):
            print(x, "is not a valid directory")
            exit()
        for k in exts:
            for q in glob.glob(x + "/**/*." + k, recursive=True):
                # print(q)
                total_lines += get_num_lines(q)

    return total_lines

# get data from leet-config.txt and put into dirs & exts
def parse_config():
    dirs = []
    exts = []

    if not os.path.isfile("./leet-config.txt"):
        print("no config! make sure you ran ")
        exit()

    f = open("leet-config.txt", 'r')

    for line in f:
        if line.startswith("directories:"):
            dirs = line.replace("directories:", "").strip().split(',')
        elif line.startswith("extensions:"):
           exts = line.replace("extensions:", "").strip().split(',')
    
    return dirs, exts

parser = argparse.ArgumentParser("leet-index")
parser.add_argument('--start', action='store_true', help="start tracking work session")
parser.add_argument('--stop', action='store_true', help="stop tracking work session data and export to file")
parser.add_argument('--get', action='store_true', help="generate leet-index config file, directories and extensions are seperated by a comma dont use newlines")
args = parser.parse_args()

if(args.get):
    if not os.path.isfile("./leet-config.txt"):
        file = open("leet-config.txt", "w")
        file.write("# be careful when setting directories as leet-index recursively globs them, example input: extensions:hpp,cpp")
        file.write("directories:\n")
        file.write("extensions:")
    else:
        print("leet-config already exists")

if(args.start):
    if not os.path.isfile("./leet-config.txt"):
        print("failed to find leet-config.txt, make sure you generate and update before starting session")
        exit()

    if os.path.isfile("./leet-temp.txt"):
        print("timer has already been started, please stop it before starting a new session")
        exit()
    
    dirs, exts = parse_config()
    total_lines = get_lines_of_code(dirs, exts)

    f = open("leet-temp.txt", 'w')
    f.write("dont delete this file while in session!\n")
    f.write(str.format("lines of code:{}\n", total_lines))
    f.write(str.format("epoch time:{}", round(time.time())))
    print("successfully started timer!")

if(args.stop):
    if not os.path.isfile("./leet-temp.txt"):
        print("no data! are you sure you started a timer?")
        exit()
    
    
    dirs, exts = parse_config()

    total_lines = get_lines_of_code(dirs, exts)
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

    leet_index = round(diff_total_lines/diff_epoch_time, 1)
    date = datetime.now().strftime("%A, %y-%m-%d")

    d = open('leet-data.txt', 'a')
    d.write(str.format("[leet-index:{} lines of code:{} time spent:{}m date: {}]\n", leet_index, diff_total_lines, round((diff_epoch_time*60)), date))
    os.remove("leet-temp.txt")
    print("successfully ended session!")