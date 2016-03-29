#!/usr/bin/python3.4
# Filename: log.py
# Copyright  zhongxin2506@outlook.com
# 主要处理程序的日志记录功能
# 日志文件处理:
# 1.只要输出窗口有新信息就更新日志文件内容.
# 2.日志文件存放路径，当前目录\log\

import os
import time

def createLogFile():
    """创建日志文件

    参数列表：无

    在程序文件目录下生成log文件夹用于存放日志文件
    log文件名格式为：log年月日时分秒.txt
    """

    #(TODO(os.getcwd()): os.getcwd()获取的不一定是navigator程序路径，
    #而是当前cmd cd到的路径需要完善)
    log_dir = "%s\log\\" % os.getcwd()
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_name = "log%s.txt" % time.strftime("%Y%m%d%H%M%S")
    f = open((log_dir + log_name), 'a')
    f.close()
    return (log_dir, log_name)

def updateLogFile(file_path, file_name, content):
    """向log文件写入日志信息

    参数列表：
    file_path: log文件路径
    file_name: log文件名
    content:  写入log的信息
    """
    f = open( (file_path + file_name), 'a')
    f.write( content )
    f.close()

if __name__ == '__main__':
    print(createLogFile.__doc__)
    print(updateLogFile.__doc__)
    log1 = createLogFile()
    updateLogFile(log1[0], log1[1], "this a test string!\n"*5)
