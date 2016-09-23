# python3.5
# -*- coding: utf-8 -*-

"""
应用层： 只允许于数据链路层通信，不允许直接调用物理层接口
"""
import ctypes
import pprint

from datalink import *

APDU_TYPE = {
    "05": "GetRequest",
    "06": "SetRequest",
    "07": "ACTIONRequest",
    "85": "GetResponse",
    "86": "SetResponse",
    "87": "ACTIONResponse"
}

DAR = {
    "00": "00--成功",
    "02": "02-暂时失效",
    "03": "03--拒绝读写",
    "04": "04--对象未定义",
    "FF": "FF--其他"
}

def double_long(data):
    tem = int("".join(data), 16)
    tem = ctypes.c_long(tem).value
    return tem

def visible_string(data):
    tem = []
    for i in data:
        tem.append(chr(int(i,16)))
    return "".join(tem)

def date_time_s(data):
    return "%s-%s-%s %s:%s:%s" % ("{0:04}".format(int("".join(data[0:2]), 16)),
                                  "{0:02}".format(int(data[2], 16)),
                                  "{0:02}".format(int(data[3], 16)),
                                  "{0:02}".format(int(data[4], 16)),
                                  "{0:02}".format(int(data[5], 16)),
                                  "{0:02}".format(int(data[6], 16)))

def oad(data):
    return "OI-{}, propID-{}, index-{}".format("".join(data[0:2]),
                                               data[2],
                                               data[3])

DATA_PATTERN = {
    "00": lambda n: "null",
    # "02": structure,
    "04": lambda n: "{:08b}".format(int("".join(n), 16)),
    "05": double_long,
    "06": lambda n: int("".join(n[:]), 16),
    "09": lambda n: " ".join(n),
    "0A": visible_string,
    "11": lambda n: int(n, 16),
    "12": lambda n: int("".join(n[:]), 16),
    "16": lambda n: int(n, 16),
    "1C": date_time_s,
    "51": oad,
}

DECODE_DATA = []
def decode(data):
    # print(">>{}".format(DECODE_DATA))
    if len(data) == 0:
        return
    if data[0] in ["01", "02"]:
        return decode(data[2::])
    elif data[0] in ["04"]:
        num = int(data[1], 16) // 8
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[2: (2 + num)]))
        return decode(data[(2 + num)::])
    elif data[0] in ["06", "05", "51"]:
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[1:5]))
        return decode(data[5::])
    elif data[0] in ["09", "0A"]:
        num = int(data[1], 16)
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[2: (2 + num)]))
        return decode(data[(2 + num)::])
    elif data[0] in ["11", "16"]:
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[1]))
        return decode(data[2::])
    elif data[0] in ["10", "12"]:
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[1:3]))
        return decode(data[3::])
    elif data[0] == "1C":
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[1:8]))
        return decode(data[8::])
    elif data[0] == "00":
        DECODE_DATA.append(DATA_PATTERN[data[0]](data[0]))
        return decode(data[1::])

class App:
    def __init__(self):
        self.apdu = {}

    def resetApdu(self):
        self.apdu = {}

    def getFrameInfo(self, frame):
        self.frame = link.getFrameInfo(frame)
        return self.frame

    def displayFrameInfo(self):
        return link.displayFrameInfo(self.frame)

    def getUserData(self):
        self.user_data = self.frame["data"]
        """app_type: 5-读取请求 6-设置请求 7-操作请求 8-上报应答
                    133-读取响应 134-设置响应 135-操作响应
        """
        self.app_type = int(self.user_data[0], 16)
        """data_type: *Normal *NormalList *Record *RecordList
                     *Next
        """
        self.data_type = int(self.user_data[1], 16)
        return self.user_data

    def getAPDUType(self):
        if self.user_data[0] in APDU_TYPE:
            self.apdu["service"] = "%s--%s" % (self.user_data[0],
                                                APDU_TYPE[self.user_data[0]])
            self.apdu["TimeTag"] = self.user_data[-1]
            if int(self.user_data[0], 16) >= 130:
                self.apdu["FollowReport"] = self.user_data[-2]
            return self.apdu["service"]

    def getDataUnitType(self):
        # TIP: 前提是先运行getAPDUType方法
        type = {"01": "Normal", "05": "Next"}
        self.apdu["dataUnitType"] = "%s--%s%s" % (self.user_data[1],
                                          self.apdu["service"][4::],
                                          type[self.user_data[1]])
        return self.apdu["dataUnitType"]

    def getPIID(self):
        if int(self.user_data[0], 16) >= 130:
            self.apdu["PPID-ACD"] = self.user_data[2]
            return self.apdu["PPID-ACD"]
        else:
            self.apdu["PPID"] = self.user_data[2]
            return self.apdu["PPID"]

    def getOAD(self):
        if self.app_type in [5, 6, 133, 134]:
            self.apdu["OAD"] = {}
            if self.data_type in [1]:
                self.apdu["OAD"]["OI"] = self.user_data[3:5]
                self.apdu["OAD"]["propID"] = self.user_data[5]
                self.apdu["OAD"]["propIndex"] = self.user_data[6]
            # TODO: zx 产品实现还存在问题，临时代码
            elif self.data_type in [5]:
                self.apdu["OAD"]["OI"] = self.user_data[6:8]
                self.apdu["OAD"]["propID"] = self.user_data[8]
                self.apdu["OAD"]["propIndex"] = self.user_data[9]
            return self.apdu["OAD"]
        elif self.app_type in [7, 135]:
            self.apdu["OMD"] = {}
            self.apdu["OMD"]["OI"] = self.user_data[3:5]
            self.apdu["OMD"]["methodID"] = self.user_data[5]
            self.apdu["OMD"]["opMode"] = self.user_data[6]
            return self.apdu["OMD"]

    def getDataRelatedWithOAD(self):
        # 获取用户数据中操作OAD,OMD,相关的数据信息
        # 如 GET-Request data为空，GET-Response为抄读数据，SET-Request为设置数据
        # Set-response为执行结果
        if self.app_type in [133, 134]:
            if self.data_type == 5:
                self.apdu["dataRelatedWithOAD"] = self.user_data[10:-2]
            else:
                self.apdu["dataRelatedWithOAD"] = self.user_data[7:-2]
            return self.apdu["dataRelatedWithOAD"]
        elif self.app_type in [135]:
            self.apdu["dataRelatedWithOMD"] = self.user_data[7:-2]
            return self.apdu["dataRelatedWithOMD"]
        elif self.app_type in [5, 6]:
            if self.data_type == 5:
                self.apdu["dataRelatedWithOAD"] = self.user_data[10:-2]
            else:
                self.apdu["dataRelatedWithOAD"] = self.user_data[7:-1]
            return self.apdu["dataRelatedWithOAD"]
        elif self.app_type in [7]:
            self.apdu["dataRelatedWithOMD"] = self.user_data[7:-1]
            return self.apdu["dataRelatedWithOMD"]

    def getObjectInfo(self):
        global DECODE_DATA
        self.apdu["object"] = {}
        # 05-GET-Request
        if self.user_data[0] == "05":
            if self.user_data[1] == "01":
                self.apdu["object"] = {}
        # 06-SET-Request
        elif self.user_data[0] == "06":
            if self.user_data[1] == "01":
                self.apdu["object"]["dataType"] = self.apdu["dataRelatedWithOAD"][0]
                self.apdu["object"]["setValue"] = (
                        DATA_PATTERN[self.apdu["object"]["dataType"]](
                                    self.apdu["dataRelatedWithOAD"][1::]))
        # 07-ACTION-Request
        elif self.user_data[0] == "07":
            if self.user_data[1] == "01":
                self.apdu["object"]["dataType"] = self.apdu["dataRelatedWithOMD"][0]
                self.apdu["object"]["setValue"] = (
                        DATA_PATTERN[self.apdu["object"]["dataType"]](
                                    self.apdu["dataRelatedWithOMD"][1::]))
        # 0x85-GET-Response
        elif self.user_data[0] == "85":
            if self.user_data[1] in ["01", "05"]:
                self.apdu["object"]["result"] = self.apdu["dataRelatedWithOAD"][0]
                # 01- Data 成功抄读
                if self.apdu["object"]["result"] == "01":
                    DECODE_DATA = []
                    decode(self.apdu["dataRelatedWithOAD"][1::])
                    self.apdu["object"]["value"] = DECODE_DATA
                # 00- DAR 返回错误信息
                elif self.apdu["object"]["result"] == "00":
                    self.apdu["object"]["error"] = DAR[self.apdu["dataRelatedWithOAD"][1]]

                # TODO: 临时代码，目前产品实现还有问题，待产品实现正确后再更新
                if self.user_data[1] == "05":
                    self.apdu["segment"] = self.user_data[3:6]
        # 0x86-SET-Response
        elif self.user_data[0] == "86":
            if self.user_data[1] == "01":
                self.apdu["object"]["result"] = DAR[self.apdu["dataRelatedWithOAD"][0]]
        # 0x87-ACTION-Response
        elif self.user_data[0] == "87":
            if self.user_data[1] == "01":
                self.apdu["object"]["result"] = DAR[self.apdu["dataRelatedWithOMD"][0]]
                self.apdu["object"]["dataType"] = self.apdu["dataRelatedWithOMD"][1]
                self.apdu["object"]["value"] = (
                        DATA_PATTERN[self.apdu["object"]["dataType"]](
                            self.apdu["dataRelatedWithOMD"][2::]))
        return self.apdu["object"]


app = App()

def test():
    while True:
        cmd = input("输入待解析的帧或exit>>")
        if cmd == "exit":
            break
        frm = cmd.split()
        app.getFrameInfo(frm)
        print(app.displayFrameInfo())
        app.getUserData()
        app.getAPDUType()
        app.getDataUnitType()
        app.getPIID()
        app.getOAD()
        app.getDataRelatedWithOAD()
        app.getObjectInfo()
        print("APDU解析信息>>")
        pp = pprint.PrettyPrinter(indent=4, depth=3)
        pp.pprint(app.apdu)
        # print("解析数据项目数: {}".format(len(app.apdu["object"]["value"])))
        app.resetApdu()

if __name__ == '__main__':
    test()
