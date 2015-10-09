#!/usr/bin/python3.4
# Filename: encap_cmd.py
# Copyright zhongxin2506@outlook.com
# 处理电表通信命令的封装及回显格式处理

import math
import time
import re
import dl645
from dl645 import splitByLen
import navigator_window 

#全局变量
ADDRESS = ["11","11","11","11","11","11"] #通信地址

CMD_PATTERN = (r":get time|:set time \d{6}|"
                ":get address|:set address \d{12}|"
                ":get date|:set date \d{8}")
class encapCmd(object):
    """表计命令封装类

    """
    def __init__(self):
        """定义必要的属性，如帧组成信息

        """
        self.frame = []
        self.fm_start = ['68']
        # TODO(ADDRESS): 通信地址后续要修改为通过数据文件读取，先临时这么用
        self.addr = ADDRESS 
        self.code = []
        self.data_len = []
        self.data = []
        self.crc = []
        self.end = ['16']
        self.cmd = ""   #封装命令
        self.fun_code = ""  #功能码
        self.cmd_info = "" #封装命令信息
        self.send_format = "" #发送显示格式
        self.rec_frame = []  #返回帧
        self.rec_format = "" #接收信息显示格式
        self.result = "" #命令执行成功|无应答|异常应答及相应的错误信息
        self.pwd = ["00", "00", "00", "04"] #密码级别，默认04级
        self.opt = ["00", "00", "00", "01"] #操作者代码

    def genFrame(self):
        """生成发送帧

        计算校验和、生成发送帧并返回
        """
        self.frame = (self.fm_start + self.addr + self.fm_start + self.code 
                        + self.data_len + self.data)
        self.crc = [dl645.getCheckSum(self.frame)]
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+校验和+16
        self.frame += self.crc + self.end
        return self.frame
        

    def getCmd(self, input_cmd):
        """通过正则表达式获取表计封装命令
        
        表计封装命令松散要求，只要能匹配正则表达式提取出的命令就是有效命令
        如:set time 113009999999依然看做是有效命令 :set time 113009
        """
        match = re.match(CMD_PATTERN, input_cmd)
        if match:
            self.cmd = match.group(0)
        return self.cmd

    def anyCmd(self):
        """由封装命令生成帧信息
        
        把电能表的通信命令封装成有明确含义的英文命令形式，并返回该命令返回帧解析所需要的关键信息
        帧格式：68+通信地址+68+控制码+数据长度+数据域+校验和+16
        命令格式：   
        :get XXX XXX  查询命令  第一个参数表示查询命令的含义，第二个参数表示需要附加的参数
        """
        #读取时间  :get time    
        if ':get time' in self.cmd:
            self.code = ["11"]
            self.data_len = ["04"]
            self.fun_code = ["04", "00", "01", "02"]
            self.data = dl645.add33H( self.fun_code[::-1])  #数据标识已按从高到底处理
            self.genFrame()
            self.cmd_info = "%s\t功能码:[%s]" % (self.cmd, " ".join(self.fun_code))
            self.send_format = ""
            self.rec_format = "抄读时间为 {0[12]}{0[13]}:{0[10]}{0[11]}:{0[8]}{0[9]}"
        #设定时间  :set time hhmmss
        if ':set time ' in self.cmd:
            self.code = ["14"]
            self.data_len = ["0F"]
            self.fun_code = ["04", "00", "01", "02"]
            set_time = self.cmd.split()[2]  #提取时间参数hhmmss
            set_time = splitByLen(set_time, [2]*3)
            self.data = dl645.add33H(self.fun_code[::-1] + self.pwd[::-1] +
                                      self.opt[::-1] + set_time[::-1]) 
            self.genFrame() 
            self.cmd_info = "%s\t功能码:[%s]" % (self.cmd, " ".join(self.fun_code))
            self.send_format = "写时间参数为 %s:%s:%s" % (set_time[0], set_time[1], set_time[2]) 
            self.rec_format = ""
        #读取通信地址  :get address
        if ':get address' in self.cmd:
            self.frame = "68 AA AA AA AA AA AA 68 13 00 DF 16".split()
            self.cmd_info = self.cmd 
            self.send_format = ""
            self.rec_format = ("抄读通信地址为:{0[10]}{0[11]}{0[8]}{0[9]}" 
                              "{0[6]}{0[7]}{0[4]}{0[5]}{0[2]}{0[3]}{0[0]}{0[1]}") 
        #写通信地址   :set address xxxxxxxxxxxx
        if ':set address ' in self.cmd:
            self.code = ["15"]
            self.data_len = ["06"]
            self.addr = ['AA', 'AA', 'AA', 'AA', 'AA', 'AA'] 
            set_addr = self.cmd.split()[2]
            set_addr = splitByLen(set_addr, [2] * 6)[::-1]
            self.data = dl645.add33H(set_addr)
            self.genFrame()
            self.cmd_info = self.cmd
            self.send_format = "写通信地址参数为 %s" % "".join( set_addr[::-1] )
            self.rec_format = ""

        #读日期及星期 :get date
        if ':get date' in self.cmd:
            self.code = ["11"]
            self.data_len = ["04"]
            self.fun_code = ["04", "00", "01", "01"]
            self.data = dl645.add33H( self.fun_code[::-1])  #数据标识已按从高到底处理
            self.genFrame()
            self.cmd_info = "%s\t功能码:[%s]" % (self.cmd, " ".join(self.fun_code))
            self.send_format = ""
            self.rec_format = ("抄读日期及星期为 20{0[14]}{0[15]}-{0[12]}"
                               "{0[13]}-{0[10]}{0[11]} 星期{0[8]}{0[9]}")

        #写日期及星期   :set date YYMMDDWW
        if ':set date ' in self.cmd:
            self.code = ["14"]
            self.data_len = ["10"]
            self.fun_code = ["04", "00", "01", "01"]
            set_date = self.cmd.split()[2]  #提取时间参数hhmmss
            set_date = splitByLen(set_date, [2]*4)
            self.data = dl645.add33H(self.fun_code[::-1] + self.pwd[::-1] +
                                      self.opt[::-1] + set_date[::-1]) 
            self.genFrame() 
            self.cmd_info = "%s\t功能码:[%s]" % (self.cmd, " ".join(self.fun_code))
            self.send_format = "写日期及星期参数为 20%s-%s-%s 星期%s" % \
                                 (set_date[0], set_date[1], set_date[2], set_date[3]) 
            self.rec_format = ""

    def sendCmd(self):
        """发送表计帧信息到485并获取返回信息

        """        
        #命令解析没有返回None表示命令解析成功
        if len(self.frame) > 0:    
            try:
                self.rec_frame = dl645.sendCmd(dl645.toCOM(self.frame)) 
                self.rec_frame = dl645.toHex(self.rec_frame)
            except:
                print(">>>>无法打开串口...")
        else:
            pass

    def getResponse(self):
        """返回信息格式解析

        """
        global ADDRESS
        if len(self.rec_frame) > 0:
            self.rec_format = self.rec_format.format(
                                "".join( dl645.minus33H( self.rec_frame[10:-2]))) 
            self.result = "命令执行成功！"
            if self.cmd == ":get address":
                self.addr = ADDRESS = dl645.minus33H(self.rec_frame[10:16])
        else:
            self.rec_format = ""
            self.result = "无应答！"

    def print(self):
        """打印输出信息

        表计封装命令执行显示格式举例：
        ================[2015-07-30 10:50:24]=========================
        :get date [功能码:04 00 01 01]
        抄读日期及星期为 202C-55-C8 星期05
        发:68 02 00 00 00 00 00 68 11 04 34 34 33 37 B9 16
        收:68 02 00 00 00 00 00 68 91 08 34 34 33 37 38 FB 88 5F 57 16
        命令执行成功!
        """
        if self.cmd:
            operate_time = time.strftime("[%Y-%m-%d %H:%M:%S]")
            print("{:=^100}".format(operate_time))    
            if self.cmd_info:
                print(self.cmd_info)
            if self.send_format:
                print(self.send_format)
            if self.rec_format:
                print(self.rec_format)
            print("发:" + " ".join( self.frame ))
            print("收:" + " ".join( self.rec_frame))
            print(self.result)
        else:
            print("命令格式错误，请检查！")

if __name__ == '__main__':
    cmd = encapCmd()
    cmd.getCmd(':set address 987654321012')
    cmd.anyCmd()
    cmd.sendCmd()
    cmd.getResponse()
    cmd.print()
