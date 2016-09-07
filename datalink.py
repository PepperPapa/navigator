# python3.5
# -*- coding: utf-8 -*-

"""
数据链路层，提供应用层和物理层之间的接口。
    1.接收应用层的报文并生成帧通过调用物理层接口发送到电能表。
    2.读取并解决物理层的串行信息为帧信息，并上传至应用层。
"""
import rs485

class LinkLayer:
    def read(self):
        self.rx = rs485.mRS.getFromCom()
        return self.rx

    def send(self, frame):
        self.tx = frame
        rs485.mRS.sendToCOM(frame)

    def _getControlInfo(self, control):
        detail_control = {}
        detail_control["origin"] = "{0:08b}".format(int(control, 16))
        detail_control["dir"] = (int(control, 16) & 0x80) >> 7
        detail_control["prm"] = (int(control, 16) & 0x40) >> 6
        detail_control["segment"] = (int(control, 16) & 0x20) >> 5
        detail_control["fun"] = int(control, 16) & 0x07
        return detail_control

    def _getSAInfo(self, sa, sa_len):
        detail_sa = {}
        detail_sa["origin"] = sa
        detail_sa["type"] = (int(sa[0], 16) & 0xc0) >> 6
        detail_sa["logic-addr"] = (int(sa[0], 16) & 0x30) >> 4
        detail_sa["len"] = sa_len
        detail_sa["addr"] = sa[1::]
        return detail_sa

    def getFrameInfo(self, frame):
        detail_frame = {}
        detail_frame["start"] = frame[0]
        detail_frame["end"] = frame[-1]
        detail_frame["length"] = int("".join(frame[1:3][::-1]), 16)
        detail_frame["control"] = self._getControlInfo(frame[3])
        sa_len = (int(frame[4], 16) & 0x0f) + 1
        detail_frame["sa"] = self._getSAInfo(frame[4:(4 + sa_len + 1)], sa_len)
        detail_frame["ca"] = frame[4 + sa_len + 1]
        detail_frame["hcs"] = frame[(4 + sa_len + 2):(4 + sa_len + 4)]
        detail_frame["data"] = frame[(4 + sa_len + 4):-3]
        detail_frame["fcs"] = frame[-3:-1]
        self.detail_frame = detail_frame
        return detail_frame

    def displayFrameInfo(self, dfm):
        # dfm-为解析后的dict对象，如self.detail_frame
        display = """
{
  起始符: %s
  长度域: %s
  控制域: {
    传输方向位DIR: %s
    起动标志位PRM: %s
    分帧标志位: %s
    功能码: %s
  }
  地址域: {
    服务器地址SA: {
      地址类型: %s
      逻辑地址: %s
      地址长度: %s
      地址: %s
    }
    客户机地址CA: %s
  }
  帧头校验HCS: %s
  链路用户数据: %s
  帧校验FCS: %s
  结束符: %s
}
        """ % (dfm["start"],
        dfm["length"],
        ["0--客户机发出", "1--服务器发出"][dfm["control"]["dir"]],
        ["0--服务器发起", "1--客户机发起"][dfm["control"]["prm"]],
        ["0--完整APDU", "1--APDU片段"][dfm["control"]["segment"]],
        {1: "1--链路管理", 3: "3--用户数据"}[dfm["control"]["fun"]],
        ["0--单地址", "1--通配地址", "2--组地址", "3--广播地址"][dfm["sa"]["type"]],
        "{0:02b}".format(dfm["sa"]["logic-addr"]),
        dfm["sa"]["len"],
        " ".join(dfm["sa"]["addr"]),
        dfm["ca"],
        " ".join(dfm["hcs"]),
        " ".join(dfm["data"]),
        " ".join(dfm["fcs"]),
        dfm["end"])
        return display

link = LinkLayer()

if __name__ == '__main__':
    link.send("68 17 00 43 05 11 11 11 11 11 11 10 6A 36 05 01 00 F3 00 02 01 00 C6 45 16".split())
    print(link.read())
    print(link.getFrameInfo(link.rx[4::]))
    print(link.displayFrameInfo(link.detail_frame))
