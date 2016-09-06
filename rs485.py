# python3.5
# Filename: rs485.py
# Copyright zhongxin2506@outlook.com
# 实现rs485串口通信功能，提供物理层通信接口

#第三方库
import serial

class RS485():
    def __init__(self, para={'port': 'COM3',
                              'baudrate': 2400,
                              'bytesize': 8,
                              'stopbits': 1,
                              'parity': 'E',
                              'timeout': 1.5
                              }):
        self.parameter = para
        self.receive = []
        self.isRSCreated = False

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
        return self.parameter

    def setParameter(self, settings):
        self.parameter = settings
        # 程序只在需要发送数据时才创建和操作串口，避免不必要的异常发生
        # isRSCreated设置为false的目的是下发发送数据前重新按设置新参数
        self.isRSCreated = False

    def sendToCOM(self, frame):
        """设计只有该方法允许真正的操作串口，其他方法不操作串口，避免额外的异常发生

        """
        try:
            if not self.isRSCreated:
                self.com = serial.Serial(self.parameter['port'],
                                self.parameter['baudrate'],
                                bytesize=self.parameter['bytesize'],
                                stopbits=self.parameter['stopbits'],
                                parity=self.parameter['parity'],
                                timeout=self.parameter['timeout'])
                self.isRSCreated = True
            else:
                self.com.open()
            #向串口发送命令,发送命令到串口，write函数只能接收整数list类型参数
            self.com.write(self._toInt(frame))
            #读串口返回帧
            self.receive = self.com.read(212)	  #根据645规定计算帧长最大不会超过212字节
            self.com.close()
            return self.receive
        except:
            print("{:!^60}".format("打开串口" + self.parameter['port'] +
                                    "失败，请检查是否被占用!"))
            return 'error'

    def getFromCom(self):
        return self._bytesToFrame(self.receive)

# 表计通信串口对象
mRS = RS485({'port': 'COM3',
              'baudrate': 2400,
              'bytesize': 8,
              'stopbits': 1,
              'parity': 'E',
              'timeout': 0.5
              })
# 台体通信串口对象
dRS = RS485({'port': 'COM1',
              'baudrate': 9600,
              'bytesize': 8,
              'stopbits': 1,
              'parity': 'N',
              'timeout': 1.5
              })

if __name__ == '__main__':
    # test code
    rs485 = RS485()
    print(rs485.getParameter())
    rs485.sendToCOM("68 56 56 34 34 12 12 68 11 04 33 33 33 33 4F 16".split())
    print(rs485.getFromCom())
    print(rs485.com)
    rs485.setParameter({'port': 'COM5',
                      'baudrate': 1200,
                      'bytesize': 7,
                      'stopbits': 2,
                      'parity': 'O',
                      'timeout': 2
                      })
    print(rs485.getParameter())
