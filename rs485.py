# !/usr/bin/python3.4
# Filename: rs485.py
# Copyright zhongxin2506@outlook.com
# 实现rs485通信功能，提供对外接口

import math

#第三方库
import serial

class RS485():
    def __init__(self):
        self.parameter = {'port': 'COM5',
                          'baudrate': 2400,
                          'bytesize': 8,
                          'stopbits': 1,
                          'parity': 'E',
                          'timeout': 1.5
                          }
        self.com = None
        self.receive = []

    def _toInt(self, frame):
        """将帧列表转发为串口可接受的整型list

        参数列表：
        frame: 存放帧信息的列表,如
        ['68', '11', '11', '11', '11', '11', '11', '68', '11', '04', '35', '34',
        '33', '37', '1E', '16']
        serial口仅能接受整型list，发送到串口前需转换成整型list
        """
        return [int(i, 16) for i in frame]

    def _bytesToFrame(self, receive):
        """串口读出的数据处理为十六进制list，转变为645协议帧格式

        参数列表:
        receive: bytes类型"""
        return ["{0:02X}".format(i) for i in receive]

    def getParameter(self):
        settings = self.com.getSettingsDict()
        return {
            'port': self.com.port,
            'baudrate': settings['baudrate'],
            'bytesize': settings['bytesize'],
            'stopbits': settings['stopbits'],
            'parity': settings['parity'],
            'timeout': settings['timeout']
        }

    def setParameter(self, settings):
        self.com.setPort(settings['port'])
        self.com.setBaudrate(settings['baudrate'])
        self.com.setByteSize(settings['bytesize'])
        self.com.setStopbits(settings['stopbits'])
        self.com.setParity(settings['parity'])
        self.com.setTimeout(settings['timeout'])

    def sendToCOM(self, frame):
        if not self.com:
            try:
                self.com = serial.Serial(self.parameter['port'],
                                    self.parameter['baudrate'],
                                    parity=self.parameter['parity'],
                                    timeout=self.parameter['timeout'])
            except:
                print("打开串口" + self.parameter['port'] +
                        "失败，请检查是否被占用!")
        try:
            if not self.com.isOpen():
                self.com.open()
            #向串口发送命令,发送命令到串口，write函数只能接收整数list类型参数
            self.com.write(self._toInt(frame))
            #读串口返回帧
            self.receive = self.com.read(212)	  #根据645规定计算帧长最大不会超过212字节
            self.com.close()
        except:
            print("打开串口" + self.parameter['port'] +
                    "失败，请检查是否被占用!")

    def getFromCom(self):
        return self._bytesToFrame(self.receive)

if __name__ == '__main__':
    # test code
    rs485 = RS485()
    rs485.sendToCOM("68 45 45 45 45 45 45 68 11 04 33 33 33 33 4F 16".split())
    print(rs485.getFromCom())
    print(rs485.getParameter())
    rs485.setParameter({'port': 'COM2',
                      'baudrate': 1200,
                      'bytesize': 7,
                      'stopbits': 2,
                      'parity': 'O',
                      'timeout': 2
                      })
    print(rs485.getParameter())
