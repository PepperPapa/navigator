#!/usr/bin/python3.4 
# Filename: script.py
# Copyright zhongxin2506@outlook.com
# 实现navigator测试脚本的保存、另存为、打开、新建等功能 
# 脚本文件处理:
#   脚本存放路径 navigator\script
# 1.保存：保存输入区脚本到脚本存放路径，文件名为当前使用文件名，默认文件为defaultscript.txt
# 2.打开：打开对话框并显示存放路径文件列表，鼠标双击或鼠标单击再点OPEN可以打开制定测试脚本
# 3.另存为：打开存放路径显示文件列表，用户输入执行文件名进行测试脚本保存

import os
import time

#测试脚本存放路径
script_dir = "%s\script\\" % os.getcwd()

#当前使用测试脚本文件名，默认文件名defaultscript.txt
script_name = "defaultscript.txt"

def save(content, file_name = script_name):
    """保存脚本文件

    参数列表：
    content: 测试脚本
    file_name: 脚本文件名
    """
    global script_dir
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)
    f = open( (script_dir + file_name), 'w')
    f.write(content)
    f.close

def read(file_name = script_name):
    """读取脚本文件

    参数列表:
    file_name: 脚本文件名
    读取脚本文件内容并返回
    """
    global script_dir
    f = open( script_dir + file_name )
    try:
        script = f.read()
    finally:
        f.close()
    return script

def openScriptList():
    """返回测试脚本目录文件列表

    参数列表: 无
    """
    global script_dir
    file_list = os.listdir(script_dir)
    return file_list

if __name__ == '__main__':
    print(save.__doc__)
    print(read.__doc__)
    print(openScriptList.__doc__)
    save("print('hello world!')\n"*5, "test010.txt")
    print(read("test010.txt"))
    print(openScriptList())
    print(len(openScriptList()))

