#!/usr/bin/python3.4
# Filename: dl645.py
# Copyright zhongxin2506@outlook.com
# 645协议相关的处理

import math

#第三方库
import serial

ENERGY_TYPE = {
            '00': '组合有功',
            '01': '正向有功',
            '02': '反向有功',
            '03': '组合无功I',
            '04': '组合无功II',
            '05': '第一象限无功',
            '06': '第二象限无功',
            '07': '第三象限无功',
            '08': '第四象限无功',
            '15': 'A相正向有功',
            '16': 'A相反向有功',
            '17': 'A相组合无功I',
            '18': 'A相组合无功II',
            '19': 'A相第一象限无功',
            '1A': 'A相第二象限无功',
            '1B': 'A相第三象限无功',
            '1C': 'A相第四象限无功',
            '1C': 'A相第一象限无功',
            '29': 'B相正向有功',
            '2A': 'B相反向有功',
            '2B': 'B相组合无功I',
            '2C': 'B相组合无功II',
            '2D': 'B相第一象限无功',
            '2E': 'B相第二象限无功',
            '2F': 'B相第三象限无功',
            '30': 'B相第四象限无功',
            '3D': 'C相正向有功',
            '3E': 'C相反向有功',
            '3F': 'C相组合无功I',
            '40': 'C相组合无功II',
            '41': 'C相第一象限无功',
            '42': 'C相第二象限无功',
            '43': 'C相第三象限无功',
            '44': 'C相第四象限无功'
        }

RATE_TYPE = ('总','费率1','费率2','费率3','费率4','费率5',
            '费率6','费率7','费率8')

MONTH_TYPE = {
            '00': '(当前)',
            '01': '(上1月)',
            '02': '(上2月)',
            '03': '(上3月)',
            '04': '(上4月)',
            '05': '(上5月)',
            '06': '(上6月)',
            '07': '(上7月)',
            '08': '(上8月)',
            '09': '(上9月)',
            '0A': '(上10月)',
            '0B': '(上11月)',
            '0C': '(上12月)'
        }
ERROR_NAME = {
            '01': '其他错误',
            '02': '无请求数据',
            '04': '密码错/未授权',
            '08': '通信速率不能更改',
            '10': '年时区数超',
            '20': '日时段数超',
            '40': '费率数超'
        }

#电表通信参数全局变量
METER_PARA = {'com': 'COM5', 'baudrate': 2400, 'datasize': 8, 'stopbits': 1,
            'parity': 'E', 'timeout': 0.5}   

def toCOM(frame_list):
    """将帧列表转发为串口可接受的整型list

    参数列表：
    frame_list: 存放帧信息的列表,如
    ['68', '11', '11', '11', '11', '11', '11', '68', '11', '04', '35', '34',
    '33', '37', '1E', '16']
    用户输入数据处理为写入串口的list数据
    把输入命令转换为serial.write函数能接受的整数list类型
    """
    return [int(i, 16)  for i in frame_list]

def toHex(read_from_COM):
    """串口读出的数据处理为十六进制显示方式

    参数列表:
    read_from_COM: bytes类型"""
    return ["{0:02X}".format(i) for i in read_from_COM]

def sendCmd(cmd):
    """通过485发送命令帧并获取返回帧

    参数列表:
    cmd: toCOM()函数返回的帧列表
    需要用到第三方python库：pyserial
    """
    global METER_PARA
    #打开串口
    rs485 = serial.Serial(METER_PARA['com'], METER_PARA['baudrate'],
                                             parity=METER_PARA['parity'], timeout=METER_PARA['timeout'])
    #向串口发送命令
    rs485.write( cmd  )    #发送命令到串口，write函数只能接收整数list类型参数'''

    #读串口返回帧
    receive = rs485.read(212)	  #根据645规定计算帧长最大不会超过212字节
    rs485.close()
    return receive

def minus33H(data_list):
    """数据域作减33h处理，接收数据使用

    data_list:[xx,xx,xx,...]
    """
    fm = data_list

    # 减33h等于加上33h的补码cdh，补码为反码加1
    tem = [math.fmod( ( int(i, 16) + int('cd', 16) ), 256) for i in fm]
    for i in range(len(tem)):
        #十进制格式化为十六进制显示,format参数不能为float类型
        tem[i] = "{0:02X}".format( int( tem[i] ) )
    return tem

def add33H(data_list):
    """数据域作加33h处理，发送数据使用

    参数列表:
    data_list:[xx,xx,xx,...]
    """
    data_area = [math.fmod((int(i, 16) + int('33', 16)), 256) for i in data_list]
    for i in range(len(data_area)):
    #十进制格式化为十六进制显示,format参数不能为float类型
        data_area[i] = "{0:02X}".format( int( data_area[i] ) )
    return data_area

def getCheckSum(frame_list):
    """根据用户输入的帧信息计算出校验和，并返回计算的校验和的值，以16进制字符串形式返回

    参数列表：
    frame_list: 存放需要参与校验和计算的帧信息列表
    如['68', '11', '11', '11', '11', '11', '11', '68',
		    '11', '04', '35', '34', '33', '37']
    校验和计算方法：等于除结束符、校验码以外的所有字节的十进制数之和与256的模,以十六进制形式体现在报文中
    """
    #建立frame_list的副本，防止修改帧的内容
    copy = list(frame_list)
    # 将copy后的list值转换为10进制
    copy = [int(i, 16) for i in copy]
    return "{0:02X}".format(int(math.fmod(sum(copy[:]), 256))) #计算的校验和

def isValid(frame):
    """检查帧起始符、结束符、校验和，判断是否是有效帧

    参数列表:
    frame_list: 完整帧信息列表
    如['68', '11', '11', '11', '11', '11', '11', '68', '11', '04', '35', '34',
    '33', '37', '1E', '16']
    帧有效性检查项：
        检查帧起始符、结束符、校验码是否是正确的值，
    正确则报文有效，返回True，否则报文无效，返回False
    """
    #协议最短帧长为12字节，不足12字节直接返回None
    if len(frame) < 12:
        return False

    #起始符、结束符错误直接返回None
    if (frame[0] != '68') or (frame[7] != '68') or (frame[-1] != '16'):
        return False

    #数据域长度和实际数据域长度不符直接返回None
    if int(frame[9], 16) != len(frame[10:-2]):
        return False

    #校验码错误直接返回None
    if getCheckSum(frame[0:-2]) != frame[-2]:
        return False
    return True

def getDmdEngItem(id_list):
    """根据数据标识获取需量或电量的数据信息

    # id_list: [xx,xx,xx]
    # index0：正向有功、反向有功、组合无功I、组合无功II、第1、2、3、4象限无功
    # index1：总，费率1、2、3、4、5、6、7、8，块
    # index2：本月，上1、2、3、4、5、6、7、8、9、10、11、12月

    #如果是数据块则以list形式返回
    """
    #TODO(return) 是否可以将返回值整合到一起哪？
    if id_list[1].upper() == 'FF':
        return [MONTH_TYPE[ id_list[2].upper() ] + \
                    ENERGY_TYPE[ id_list[0].upper() ] + i \
                    for i in RATE_TYPE ]
    else:
        return MONTH_TYPE[ id_list[2].upper() ] \
            + ENERGY_TYPE[ id_list[0].upper() ] \
            + RATE_TYPE[ int( id_list[1] ) ]

def getError(error_byte):
    """根据异常应答帧的错误字节返回具体的错误信息

    error_byte: 异常应答帧的错误信息字节
    收到异常应答帧，获取具体的错误信息
    局限：目前仅支持07协议错误信息，不支持国网第4号补遗文件扩展的错误信息，暂会报错
    """
    error_info = minus33H([error_byte])
    return ERROR_NAME[error_info[0]]

def splitByLen(string, len_list):
    """根据长度列表分割字符串

    string: 要分割的字符串
    len_list:字符串长度列表
    如string="1234567890",len_list=[2,4,3,1]
    则函数返回['12', '3456', '789', '0']
    """
    #将len_list中每个字符串的长度转化为定位字符串的index列表
    for i in range(len(len_list)):
        if i > 0:
            len_list[i] += len_list[i-1]

    str_list = []
    for i in range(len(len_list)):
        if i == 0:
            str_list.append(string[0:len_list[i]])
        else:
            if len_list[i] > len(string):
                # len_list[i]表的index的值已经大于string的长度时，分割即可结束，需跳出循环
                continue
            else:
                str_list.append( string[ len_list[i-1]:len_list[i] ] )
    return str_list

if __name__ == '__main__':
    print(splitByLen.__doc__)
    test_frame = "68 02 00 00 00 00 00 68 11 04 34 34 33 37 B9 16"
    test_frame = test_frame.split()
    print(toCOM(test_frame))
    # toHex()
    # sendCmd()
    print(minus33H(test_frame))
    print(add33H(["04", "00", "01", "02"]))
    print(getCheckSum(test_frame[0:-2]))
    print(isValid(test_frame))
    print(getDmdEngItem(["00","04","0c"]))
    print(getError('37'))
    print(splitByLen("thisisateststring!", [4,2,1,4,7,8,20,9]))
