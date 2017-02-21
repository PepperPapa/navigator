from ctypes import *

# 常量
OBJ_NAME = {
    "0x4001": "总有功功率",
    "0x4002": "A相有功功率",
    "0x4003": "B相有功功率",
    "0x4004": "C相有功功率",
    "0x4005": "总无功功率",
    "0x4006": "A相无功功率",
    "0x4007": "B相无功功率",
    "0x4008": "C相无功功率",
    "0x4009": "总视在功率",
    "0x400a": "A相视在功率",
    "0x400b": "B相视在功率",
    "0x400c": "C相视在功率",
    "0x400d": "A相电流有效值",
    "0x400e": "B相电流有效值",
    "0x400f": "C相电流有效值",
    "0x4010": "A相电压有效值",
    "0x4011": "B相电压有效值",
    "0x4012": "C相电压有效值",
    "0x4013": "A相电压频率",
    "0x4014": "B相电压频率",
    "0x4015": "C相电压频率",
    "0x4016": "总功率因数",
    "0x4017": "A相功率因数",
    "0x4018": "B相功率因数",
    "0x4019": "C相功率因数",
    "0x401a": "A相相位差",
    "0x401b": "B相相位差",
    "0x401c": "C相相位差",
    "0x401d": "A相电压相位",
    "0x401e": "B相电压相位",
    "0x401f": "C相电压相位",
    }

def convert(s):
    # 将十六进制字符串转换为浮点数
    # 如，print convert("49d377a8")  返回 1732341.0
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float

def stringToFrame(frame_string):
    return frame_string.split()

def lenASDU(frame):
    if (len(frame) > 0):
        length = int(frame[1],16)
        length = length - 3
        return length
    else:
        return 0

def getASDU(frame):
    asdu = frame[7:-2]
    return asdu

def getTI(asdu):
    return asdu[0]

def getVSQ(asdu):
    return asdu[1]

def getCOT(asdu):
    return asdu[2:4][::-1]

def getASDUAddr(asdu):
    return asdu[4:6]

def getObjAddr(asdu):
    return "0x{1}{0}".format(*asdu[6:8])

def getData(asdu):
    if (len(asdu) > 8):
        return asdu[8:]

def getSQ(vsq):
    # False - SQ = 0
    # True - SQ = 1
    return int(vsq, 16) & 0x80 != 0

def getObjNum(vsq):
    # 返回数据对象数量
    return int(vsq, 16) & 0x7f
    
def getAllObj(data, num, sq):
    # 提取所有数据对象信息
    obj = []
    # SQ = 1
    if sq:
        for i in range(num):
            obj.append("".join(data[i * 5:i * 5 + 4][::-1]))
        obj = [convert(s) for s in obj]
        return obj                   

def genObjAddrList(first_obj_addr, num):
    obj_addr = int(first_obj_addr, 16)
    obj_addr_list = []
    for i in range(num):
        obj_addr_list.append(obj_addr + i)
    obj_addr_list = ["0x{0:02x}".format(item) for item in obj_addr_list]
    return obj_addr_list
    
def displayAllObj(info):
    # SQ = 1
    if info["sq"]:
        # 生成信息对象名称列表
        obj_name_list = genObjAddrList(info["obj_addr"], info["num"])
        print("解析数据信息如下:")
        for i in range(info["num"]):
            print("%s %s:  %s" % (obj_name_list[i], OBJ_NAME[obj_name_list[i]], info["objs"][i]))
        
if __name__ == "__main__":
    info = {}
    while (True):
        cmd = input(">>> ")
        info = {}
        # 退出命令
        if (cmd == "exit"):
            break

        info["frame"] = stringToFrame(cmd)
        info["asdu"] = getASDU(info["frame"])
        info["obj_addr"] = getObjAddr(info["asdu"])
        info["vsq"] = getVSQ(info["asdu"])
        info["data"] = getData(info["asdu"])
        info["sq"] = getSQ(info["vsq"])
        info["num"] = getObjNum(info["vsq"])
        info["objs"] = getAllObj(info["data"], info["num"], info["sq"])
        displayAllObj(info)
        # 退出命令
        if (cmd == "exit"):
            break
