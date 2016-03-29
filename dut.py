# !usr/bin/python3.4

import rs485
import meter
import dutlib

def toASCIIList(string):
    """字符串转换为ASCII码（int型）组成的数组

    """
    return ['{0:02X}'.format(ord(ch)) for ch in string]

def matchCmd(cmdin):
    """查找是否有和输入匹配的命令，有则返回匹配项，否则返回None

    """
    for item in dutlib.DUTLIB:
        if cmdin == item['cmdin']:
            return item
    return None

def runCmd(cmdin):
    # step 1: 首先根据输入命令去查找是否有匹配的命令库
    match_lib = matchCmd(cmdin)

    # step 2：命令匹配的情况继续执行
    if match_lib:
        # step 3: 向串口发送命令
        result = rs485.dRS.sendToCOM(toASCIIList(match_lib['command']))
        # step 4: 串口执行未返回error则往下继续执行
        if result != 'error':
            meter.stampTime()
            print(match_lib['cmdin'])
            print(match_lib['info'])


if __name__ == '__main__':
    runCmd(':dut-set ioff')
