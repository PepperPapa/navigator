# python3.5
# -*- coding: utf-8 -*-

"""
数据链路层，提供应用层和物理层之间的接口。
    1.接收应用层的报文并生成帧通过调用物理层接口发送到电能表。  
    2.读取并解决物理层的串行信息为帧信息，并上传至应用层。
"""
import rs485

class LinkLayer:
    def receive(self):
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
        detail_sa["addr"] = " ".join(sa[1::])
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
        return detail_frame
        
link = LinkLayer()

if __name__ == '__main__':
    link.send("68 17 00 43 05 11 11 11 11 11 11 10 6A 36 05 01 00 40 00 01 00 00 32 F0 16".split())
    print(link.receive())
    print(link.getFrameInfo(link.rx[4::]))
