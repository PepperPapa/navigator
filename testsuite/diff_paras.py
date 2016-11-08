# python3.5

import math

addr = "00 00 00 00 00 00".split()

def id_split(id_str):
    id = "{0}{1} {2}{3} {4}{5} {6}{7}".format(*id_str)
    return id.split()

def add33H(data_list):
    data_area = [math.fmod((int(i, 16) + int('33', 16)), 256) for i in data_list]
    for i in range(len(data_area)):
        data_area[i] = "{0:02X}".format( int( data_area[i] ) )
    return data_area

def minus33H(data_list):
    tem = [math.fmod( ( int(i, 16) + int('cd', 16) ), 256) for i in data_list]
    for i in range(len(tem)):
        tem[i] = "{0:02X}".format( int( tem[i] ) )
    return tem

def getCheckSum(data_list):
    copy = list(data_list)
    copy = [int(i, 16) for i in copy]
    return ["{0:02X}".format(int(math.fmod(sum(copy[:]), 256)))]

def genReadFrame(id_str, addr_list):
    data = add33H(id_split(id_str)[::-1])
    fm = ["68"] + addr_list
    fm.append("68")
    fm.append("11")
    fm.append("04")
    fm = fm + data
    cs = getCheckSum(fm)
    fm = fm + cs
    return fm + ["16"]
    
if __name__ == '__main__':
    print(genReadFrame("04000103", addr))
