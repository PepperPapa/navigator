#! usr/bin/python3.4

# 标准库
import json

import dl645

cmd_lib = {
    # DI3 DI2 DI1 DI0
    "cmd": [':get-energy', '00', '01', '02', '03'],
    # TODO: 待解决输入命令的提取问题，暂时考虑以正则表达式的方式提取
    "cmd_rule": r'',
    # 定义匿名函数从cmd参数中提取所需参数数据
    "item": (lambda cmd: "(上{3}结算日)组合有功费率{2}电能".
                format(*[int(i, 16) for i in cmd.split()[1:]])),
    "send": [],
    "recv": [],
    "return": lambda r: "{7}{6}{5}.{4}".format(*r),
    "frame": {
        "start": ["68"],
        "addr": ["11"] * 6,
        "code": ["11"],
        "len": ["04"],
        # 定义匿名函数从cmd参数中提取所需参数数据 DI0 DI1 DI2 DI3
        "data": lambda cmd: cmd.split()[1:][::-1],
        "cs": [],
        "end": ["16"]
    }
}

def getFrame(cmd):
    """获取发送帧信息

    从cmd_lib["frame"]参数中得出发送帧，如得出的发送帧信息为
    ['68', '11', '11', '11', '11', '11', '11', '68', '11', '04', '33', '33',
    '33', '33', '17', '16']
    """
    fm = (cmd['frame']["start"] + cmd['frame']["addr"] + cmd['frame']["start"]
        + cmd['frame']["code"] + cmd['frame']["len"]
        + dl645.add33H(cmd['frame']["data"](cmd["cmd"])))
    cs = dl645.getCheckSum(fm)
    return fm + [cs] + cmd['frame']['end']

if __name__ == '__main__':

    ### test code ###
    #发：68 11 11 11 11 11 11 68 11 04 33 33 33 33 17 16
    #收：68 11 11 11 11 11 11 68 91 08 33 33 33 33 68 39 33 33 A2 16
    print(cmd_lib["cmd"])
    print(cmd_lib["item"](cmd_lib["cmd"]))
    print(cmd_lib["send"])
    print(cmd_lib["recv"])
    print(cmd_lib["frame"]["start"])
    print(cmd_lib["frame"]["addr"])
    print(cmd_lib["frame"]["code"])
    print(cmd_lib["frame"]["len"])
    print(cmd_lib["frame"]["data"](cmd_lib["cmd"]))
    print(cmd_lib["frame"]["cs"])
    print(cmd_lib["frame"]["end"])
    cmd_lib["recv"] = (("68 11 11 11 11 11 11 68 91 08 33 33 33 33 68 39 33 33 "
                        "A2 16").split())
    print(cmd_lib["cmd"])
    print(cmd_lib["item"](cmd_lib["cmd"]))
    print(cmd_lib["return"](dl645.minus33H(cmd_lib["recv"][10:-2])))
    print("发: ", getFrame(cmd_lib))
    print("收: ", cmd_lib["recv"])
