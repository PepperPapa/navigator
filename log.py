# log.py
# 主要处理程序的日志记录功能

import os
import time
'''日志文件处理:
1.程序首次运行首先创建日志文件.
2.只要输出窗口有新信息就更新日志文件内容.
3.日志文件存放路径，当前目录\log\
'''

def createLogFile():
    log_dir = os.getcwd() + "\log\\"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_name = "log" + time.strftime("%Y%m%d%H%M%S") + ".txt"
    f = open( (log_dir + log_name), 'a')  #每打开一次程序就创建一个日志文件
    f.close()
    return (log_dir, log_name)

def updateLogFile(file_path, file_name, record):
    '''文件如果不关闭，则打开日志文件没有显示，为了能够实时查看日志，每次调用事件都
    执行打开文件，写入信息，关闭文件的模式'''
    f = open( (file_path + file_name), 'a')
    f.write( record )
    f.close()

