# python3.5
# -*- coding: utf-8 -*-

"""
应用层： 只允许于数据链路层通信，不允许直接调用物理层接口
"""
from datalink import *

APDU_TYPE = {
    "05": "GetRequest",
    "06": "SetRequest",
    "85": "GetResponse",
    "86": "SetResponse"
}

class App:
    def __init__(self):
        self.apdu = {}

    def getFrameInfo(self, frame):
        self.frame = link.getFrameInfo(frame)
        return self.frame

    def displayFrameInfo(self):
        return link.displayFrameInfo(self.frame)

    def getUserData(self):
        self.user_data = self.frame["data"]
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
        if self.user_data[1] == "01":
            self.apdu["dataUnitType"] = "%s--%sNormal" % (self.user_data[1],
                                                self.apdu["service"][4::])
            return self.apdu["dataUnitType"]

    def getPIID(self):
        if int(self.user_data[0], 16) >= 130:
            self.apdu["PPID-ACD"] = self.user_data[2]
            return self.apdu["PPID-ACD"]
        else:
            self.apdu["PPID"] = self.user_data[2]
            return self.apdu["PPID"]

    def getOAD(self):
        self.apdu["OAD"] = {}
        self.apdu["OAD"]["OI"] = self.user_data[3:5]
        self.apdu["OAD"]["propID"] = self.user_data[5]
        self.apdu["OAD"]["propIndex"] = self.user_data[6]
        return self.apdu["OAD"]

    def getDataRelatedWithOAD(self):
        # 获取用户数据中操作OAD相关的数据信息
        # 如 GET-Request data为空，GET-Response为抄读数据，SET-Request为设置数据
        # Set-response为执行结果
        pass

app = App()

if __name__ == '__main__':
    app.getFrameInfo("68 17 00 43 05 11 11 11 11 11 11 10 6A 36 05 01 00 40 03 02 00 00 9B 3A 16".split())
    print(app.displayFrameInfo())
    app.getUserData()
    app.getAPDUType()
    app.getDataUnitType()
    app.getPIID()
    app.getOAD()
    print(app.apdu)
