# !/usr/bin/python3.4

import re
import math

# 本地模块
import rs485
import lib645

# helper function
def splitByLen(string, len_list):
    """根据长度列表分割字符串

    string: 要分割的字符串
    len_list:字符串长度列表
    如string="1234567890",len_list=[2,4,3,1]
    则函数返回['12', '3456', '789', '0']
    """
    current_index = 0
    new_list = []
    for i in len_list:
        if (current_index < len(string)):
            new_list.append(string[current_index:(current_index + i)])
            current_index += i
    return new_list

def formatArray(dataList, formatList):
    """数组以指定的次序重新排序

    dataList: 原list数组
    formatList： 指定重牌次序的index list
    如 datalist = ["01", "02", "03"]
       formatList = [1, 2, 0]
       则返回值为["02", "03", "01"]
    """
    new_list = []
    for i in formatList:
        if i < len(dataList):
            new_list.append(dataList[i])
    return new_list

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
    #计算的校验和并格式化为16进制字符串数组返回
    return ["{0:02X}".format(int(math.fmod(sum(copy[:]), 256)))]

# class defination
class Meter():
    def __init__(self, matchCmd, cmdin):
        self.protocol = matchCmd
        self.pwd = "04000000"  # 密码 PA PA0 PA1 P2
        self.opcode = "01000000" # 操作者代码
        """ 提取输入的命令信息：命令名称、参数、附加参数

        举例：
        command ":get-energy 00000000"
        返回值: [':get-energy', '00000000']

        命令的封装格式包含如下三种:
        :get-xxxx             //1.抄读命令，无参数
        :get-xxxx XXXXXXXX    //2.抄读命令、参数
        :get-xxxx XXXXXXXX add-XXXXX  //3.抄读命令、参数、附加参数
        :set-xxxx XXXXXXXX    //4.设置命令、参数
        """
        self.cmd = cmdin.split()

    def _getType(self):
        """获取封装命令的类型

        0-表示抄读命令、无参数  :get-xxxx
        1-表示抄读命令、有参数  :get-xxxx XXXXXXXX
        2-表示抄读命令、有参数、有附加参数  :get-xxxx XXXXXXXX add-XXXXXXXX
        3-表示设置命令
        n-TODO：待详细划分,一切特殊情况可以进行扩展
        """
        if ":get-" in self.cmd[0]:
            if len(self.cmd) == 1:
                return 0
            elif len(self.cmd) == 2:
                return 1
            elif len(self.cmd) == 3:
                return 2
        elif ":set-" in self.cmd[0]:
            return 3

    def getAddr(self):
        """读取表计通信地址并返回

        举例:
        返回值: "010203040506"
        """
        # TODO: 先临时使用默认值，用于测试
        self.addr = "121234345656"
        return self.addr

    def getPwd(self):
        return self.pwd

    def getOpcode(self):
        return self.opcode

    def getItemName(self):
        """解析输入命令的数据项名称并返回

        :get-energy 00000000 表示抄读 (当前)组合有功总电能
        """
        # type=1或2表示封装命令包含参数或附加参数
        if self._getType() == 1 or self._getType() == 2:
            # 数据项名称从参数即self.cmd[1]中提取
            para_slice = (splitByLen(self.cmd[1],
                        self.protocol['txFormat']['slice']))
            item_name_slice = []
            for i in range(len(self.protocol['txFormat']['item'])):
                item_name_slice.append((self.protocol['txFormat']['item'][i]
                                        [para_slice[i].upper()]))
            item_name = (formatArray(item_name_slice,
                                self.protocol['txFormat']['order']))
            return "".join(item_name)
        # type=0表示封装命令不包含参数或附加参数
        elif self._getType() == 0:
            return self.protocol['txFormat']
        # type=3表示封装命令为设置命令
        elif self._getType() == 3:
            return self.protocol['txFormat']

    def buildFrame(self):
        """生成发送帧

        发送帧的生成思路为：
        :get-xxxx
          1.抄读命令，无参数：所需参数：表地址 + 数据标识
          2.数据标识：协议中已有 self.protocol['id']
        :get-xxxx XXXXXXXX
          1.抄读命令、参数：所需参数：表地址 + 数据标识
          2.数据标识：参数中提取 self.cmd[1]
          3.表地址: 调用函数获取 self.getAddr()
        :get-xxxx XXXXXXXX add-XXXXX
          1.抄读命令、参数、附加参数：所需参数：表地址 + 数据标识 + 附加参数
          2.数据标识：参数中提取 self.cmd[1]
          3.附加参数：从附加参数中提取 self.cmd[2]
          4.表地址: 调用函数获取 self.getAddr()
        :set-xxxx XXXXXXXX    //4.设置命令、参数
          TODO: 待完善
        """
        #'68':起始符
        new_frame = ['68']
        # 通信地址：反序
        new_frame.extend(splitByLen(self.getAddr(), [2] * 6)[::-1])
        #'68':起始符
        new_frame.extend(['68'])

        # type=1表示封装命令包含参数
        if self._getType() == 1:
            # 功能码: 11为抄读数据
            new_frame.extend(['11'])
            # 功能码: 数据域长度
            new_frame.extend(['04'])
            # 数据标识：数据标识从参数即self.cmd[1]中提取 加33H 反序
            new_frame.extend(add33H(splitByLen(
                             self.cmd[1], [2] * 4)[::-1]))
        # type=1表示封装命令包含参数和附加参数
        elif self._getType() == 2:
            # 提取附加参数 add-XXXXXXXX, 如果附件参数长度不是偶数，则在最后一个
            # 参数前插入0，如 抄读负荷曲线时，附件参数可能为块数，抄读02块，用户
            # 使用时可以会省略那个0
            add_para = self.cmd[2].split('-')[1]
            if len(add_para) % 2 != 0:
                add_para = add_para[0:-1] + '0' + add_para[-1]
            add_para = splitByLen(add_para, [2] * (len(add_para) // 2))

            # 功能码: 11为抄读数据
            new_frame.extend(['11'])
            # 功能码: 数据域长度
            new_frame.extend(['{0:02X}'.format(4 + len(add_para))])
            # 数据标识：数据标识从参数即self.cmd[1]中提取 加33H 反序
            new_frame.extend(add33H(splitByLen(
                             self.cmd[1], [2] * 4)[::-1]))
            # 附加参数
            new_frame.extend(add33H(add_para[::-1]))
        # type等于0表示封装命令不包含参数或附加参数
        elif self._getType() == 0:
            # 功能码: 11为抄读数据
            new_frame.extend(['11'])
            # 功能码: 数据域长度
            new_frame.extend(['04'])
            # 数据标识：加33H 反序
            new_frame.extend(add33H(splitByLen(
                             self.protocol['id'], [2] * 4)[::-1]))
        # type等于3表示封装命令为设置命令
        elif self._getType() == 3:
            # 功能码: 11为抄读数据
            new_frame.extend([self.protocol['code']])
            # 功能码: 数据域长度
            new_frame.extend([self.protocol['len']])
            # 数据标识：加33H 反序
            new_frame.extend(add33H(splitByLen(
                             self.protocol['id'], [2] * 4)[::-1]))
            # 密码：加33H 正序
            new_frame.extend(add33H(splitByLen(
                             self.getPwd(), [2] * 4)))
            # 操作者代码：加33H 正序
            new_frame.extend(add33H(splitByLen(
                             self.getOpcode(), [2] * 4)))
            # 设定值
            new_frame.extend(add33H(splitByLen(self.cmd[1],
                             [2] * (len(self.cmd[1]) // 2))[::-1]))
        # 校验和
        new_frame.extend(getCheckSum(new_frame))
        #'16':结束符
        new_frame.extend(['16'])
        self.tx = new_frame
        return new_frame

    def send(self, rs485):
        rs485.sendToCOM(self.tx)
        self.rx = rs485.getFromCom()

    def response(self):
        return self.rx

    def responseInfo(self):
        """命令返回信息提取，正常应答、异常应答及相应的错误信息、无应答

        """
        if len(self.rx) == 0:
            return "无应答..."
        elif int(self.rx[8], 16) & 0xD0 == 0xD0:
            result = "异常应答帧"
            err = int(minus33H([self.rx[-3]])[0], 16)
            if err & 0x01:
                result += ">>其他错误"
            if err & 0x02:
                result += ">>无请求数据"
            if err & 0x04:
                result += ">>密码错/未授权"
            if err & 0x08:
                result += ">>通信速率不能更改"
            if err & 0x10:
                result += ">>年时区数超"
            if err & 0x20:
                result += ">>日时段数超"
            if err & 0x40:
                result += ">>费率数超"
            return result
        else:
            return "操作成功!"
    def responseData(self):
        """提取返回帧中的数据信息并返回

        返回值：以字符串数组形式返回
        TODO: 解决数据的正负号显示问题
        """
        # 0-表示抄读命令、无参数  :get-xxxx
        if self._getType() == 0:
            data_area = minus33H(self.rx[10:-2])
            data_split = splitByLen(data_area, self.protocol['rxFormat']['unit'])
            result = []
            for i in range(len(data_split)):
                result.append(self.protocol['rxFormat']['style'][i]
                              .format(*data_split[i][::-1]))
            return result
        # 1-表示抄读命令、有参数  :get-xxxx XXXXXXXX
        elif self._getType() == 1:
            data_area = minus33H(self.rx[10:-2])
            data_split = splitByLen(data_area, self.protocol['rxFormat']['unit'])
            result = []
            for i in range(len(data_split)):
                result.append(self.protocol['rxFormat']['style'][i]
                              .format(*data_split[i][::-1]))
            return result
        # 2-表示抄读命令、有参数、有附加参数  :get-xxxx XXXXXXXX add-XXXXXXXX
        elif self._getType() == 2:
            data_area = minus33H(self.rx[10:-2])
            result = []
            temp = " ".join(data_area[7:-3]).split('AA')
            for i in range(len(temp)):
                temp[i] = (splitByLen(temp[i].split(),
                            self.protocol['rxFormat']['unit'][i]))
                for j in range(len(temp[i])):
                    result.append(self.protocol['rxFormat']['style'][i][j]
                                    .format(*temp[i][j][::-1]))
            return result

    def isValid(self):
        """检查帧起始符、结束符、校验和，判断是否是有效帧

        帧有效性检查项：
            检查帧起始符、结束符、校验码是否是正确的值，
        正确则报文有效，返回True，否则报文无效，返回False
        """
        #协议最短帧长为12字节，不足12字节直接返回None
        if len(self.rx) < 12:
            return False

        #起始符、结束符错误直接返回None
        if (self.rx[0] != '68') or (self.rx[7] != '68') or (self.rx[-1] != '16'):
            return False

        #数据域长度和实际数据域长度不符直接返回None
        if int(self.rx[9], 16) != len(self.rx[10:-2]):
            return False

        #校验码错误直接返回None
        if getCheckSum(self.rx[0:-2]) != [self.rx[-2]]:
            return False
        return True

    def toPrint(self):
        show = []
        show.append()
        show.append(self.getItemName())
        show.append("发:" + " ".join(self.tx))
        show.append("收:" + " ".join(self.rx))
        show.append(self.responseInfo())
        show.append("\n".join(self.responseData()))
        return show

if __name__ == '__main__':

    ### test code ###
    #发：68 11 11 11 11 11 11 68 11 04 33 33 33 33 17 16
    #收：68 11 11 11 11 11 11 68 91 08 33 33 33 33 68 39 33 33 A2 16

    cmdin = ":get-load-curve 06000000 add-01"
    matchCmdModel = None
    for item in lib645.CMDS:
        if re.match(item['rule'], cmdin):
            matchCmdModel = item
            break
    if matchCmdModel:
        cmd = Meter(matchCmdModel, cmdin)
        cmd.buildFrame()
        rs = rs485.RS485()
        cmd.send(rs)
        cmd.response()
        if cmd.isValid():
            show = cmd.toPrint()
            for i in show:
                print(i)

    # test code for function splitByLen
    # str = "1234567890"
    # print(splitByLen(str, [3, 4, 2, 1]) == ['123', '4567', '89', '0'])
    # print(splitByLen(str, [3, 4, 2]) == ['123', '4567', '89'])
    # print(splitByLen(str, [3, 4, 2, 9, 0]) == ['123', '4567', '89', '0'])
    # print(splitByLen(str, [3, 4, 2, 1, 10, 12]) == ['123', '4567', '89', '0'])
    # print("".join(splitByLen("45837813446281295381", [2]*10)[::-1]))
    # print(splitByLen([['44', '48', '00']], [3]))

    # test code for function formatList
    # arry = ["电能","组合有功","总","(当前)"]
    # print(arry == ['电能', '组合有功', '总', '(当前)'])
    # print(formatArray(arry, [3, 1, 2, 0]) == ['(当前)', '组合有功', '总', '电能'])
    # print(formatArray(arry, [3, 1]) == ['(当前)', '组合有功'])
    # print(formatArray(arry, [3, 1, 4, 2, 0, 100]) == ['(当前)', '组合有功', '总', '电能'])
    # arry2 = ["时间"]
    # print(formatArray(arry2, [0]) == ["时间"])
