# !usr/bin/python3.4
DUTLIB = [
    {'cmdin': ':dut-set uaon', 'command': 'UAON\r'},
    {'cmdin': ':dut-set uaoff', 'command': 'UAOF\r'},
    {'cmdin': ':dut-set ubon', 'command': 'UBON\r'},
    {'cmdin': ':dut-set uboff', 'command': 'UBOF\r'},
    {'cmdin': ':dut-set ucon', 'command': 'UCON\r'},
    {'cmdin': ':dut-set ucoff', 'command': 'UCOF\r'},
    {'cmdin': ':dut-set iaon', 'command': 'IAON\r'},
    {'cmdin': ':dut-set iaoff', 'command': 'IAOF\r'},
    {'cmdin': ':dut-set ibon', 'command': 'IBON\r'},
    {'cmdin': ':dut-set iboff', 'command': 'IBOF\r'},
    {'cmdin': ':dut-set icon', 'command': 'ICON\r'},
    {'cmdin': ':dut-set icoff', 'command': 'ICOF\r'},
    {'cmdin': ':dut-set uion', 'command': 'UION\r'},
    {'cmdin': ':dut-set uioff', 'command': 'UIOF\r'},
    {'cmdin': ':dut-set uon', 'command': 'UON\r'},
    {'cmdin': ':dut-set uoff', 'command': 'UOF\r'},
    {'cmdin': ':dut-set ion', 'command': 'ION\r'},
    {'cmdin': ':dut-set ioff', 'command': 'IOF\r'}
]
def toASCIIList(string):
    """字符串转换为ASCII码（int型）组成的数组

    """
    return [ord(ch) for ch in string]


if __name__ == '__main__':
    print(toASCIIList('UON\r'))
