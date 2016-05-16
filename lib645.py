# !/usr/bin/python3.4
# 电表命令封装模板

# 一条命令封装模型需要能达到如下要求：
# 1.pattern:能匹配用户输入的命令对应哪个命令封装模板，即匹配命令的正则表达式
# 2.type: 命令类型，对应645协议列出的12大类型
#      [1:读数据、2：读后续数据、3：写数据、4：读通信地址、5：写通信地址、
#     6：广播校时、7：冻结命令、8：更改通信速率、9：修改密码、10：最大需量清零、
#     11：电表清零、12：事件清零]
# 3.txInfo：命令帧发送信息，如“抄读正向有功总电能”，内容为调用相应处理函数的字符串表示
# 4.rxInfo：命令帧接收信息，主要解析返回帧数据域的信息，内容为调用相应处理函数的
# 字符串表示。
import re

CMDS = [
    {'type': 0,
     'pattern': re.compile('^:get-energy \d\d\d[\da-fA-F][\dfF][\dfF]\d[\da-cA-C]$'),
     'txInfo': 'id.eng_tx_name',
     'rxInfo': 'id.eng_rx_data'
     },
    {'type': 0,
    'pattern': re.compile('^:get-demand \d\d\d[\da-fA-F][\dfF][\dfF]\d[\da-cA-C]$'),
    'txInfo': 'id.dmd_tx_name',
    'rxInfo': 'id.dmd_rx_data'
    },
    {'type': 20,    # 20表示原始命令帧
     'pattern': re.compile('^68 ([\da-fA-F]{2} ){6}68 ([\da-fA-F]{2} )+16$'),
     'txInfo': 'id.raw_tx_name',
     'rxInfo': 'id.raw_rx_data'
     },
    {'type': 0,
     'pattern': re.compile('^:get-time 04000102$'),
     'txInfo': 'id.time_tx_name',
     'rxInfo': 'id.time_rx_data'
    },
    {'type': 2,
     'pattern': re.compile('^:set-time 04000102 (\d\d){3}$'),
     'txInfo': 'id.settime_tx_name'
    },
    {'type': 0,
     'pattern': re.compile('^:get-date 04000101$'),
     'txInfo': 'id.date_tx_name',
     'rxInfo': 'id.date_rx_data'
    },
    {'type': 2,
     'pattern': re.compile('^:set-date 04000101 (\d\d){4}$'),
     'txInfo': 'id.setdate_tx_name'
    },
    {'type': 0,
     'pattern': re.compile('^:get-cycle-display 04040[12]\d[\da-fA-F]$'),
     'txInfo': 'id.cycle_tx_name',
     'rxInfo': 'id.cycle_rx_data'
    },
    {'type': 2,
     'pattern': re.compile('^:set-cycle-display 04040[12]\d[\da-fA-F] [\da-fA-F]{8},[\da-fA-F]{2}$'),
     'txInfo': 'id.setcycle_tx_name',
     # 表示需要特殊处理设定参数反序， 如 01010000,01 生成发送的顺序是00000101,01
     'reverse_setting_data': "id.reverse_setting_data"
    },
    {'type': 0,
     'pattern': re.compile('^:get-load-curve \d{8}( add-(\d)+)?$'),
     'txInfo': 'id.ldcurve_tx_name',
     'rxInfo': 'id.ldcurve_rx_data',
     'add': True   # 表示需要处理附加参数 add-nn或add-YYMMDDhhmmnn
    },
    {'type': 3,
     'pattern': re.compile('^:get-addr$'),
     'txInfo': 'id.addr_tx_name',
     'rxInfo': 'id.addr_rx_data',
    },
]

# 全局变量
eng_slice_name = [
    {"00": "电能"},
    {"00": "组合有功", "01": "正向有功", "02": "反向有功",
    "03": "组合无功I", "04": "组合无功II", "05": "第一象限无功",
    "06": "第二象限无功", "07": "第三象限无功", "08": "第四象限无功",
    "09": "正向视在", "0A": "反向视在", "15": "A向正向有功",
    "16": "A相反向有功", "17": "A相组合无功I", "18": "A相组合无功II",
    "19": "A相第一象限无功", "1A": "A相第二象限无功",
    "1B": "A相第三象限无功", "1C": "A相第四象限无功",
    "1D": "A相正向视在", "1E": "A相反向视在", "29": "B相正向有功",
    "2A": "B相反向有功", "2B": "B相组合无功I", "2C": "B相组合无功II",
    "2D": "B相第一象限无功", "2E": "B相第二象限无功",
    "2F": "B相第三象限无功","30": "B相第四象限无功",
    "31": "B相正向视在", "32": "B相反向视在", "3D": "C相正向有功",
    "3E": "C相反向有功", "3F": "C相组合无功I", "40": "C相组合无功II",
    "41": "C相第一象限无功", "42": "C相第二象限无功",
    "43": "C相第三象限无功","44": "C相第四象限无功",
    "45": "C相正向视在", "46": "C相反向视在" },
    {"00": "总", "01": "费率1", "02": "费率2", "03": "费率3",
    "04": "费率4", "05": "费率5", "06": "费率6", "07": "费率7",
    "08": "费率8", "FF": "数据块" },
    {"00": "(当前)","01": "(上1结算日)","02": "(上2结算日)",
    "03": "(上3结算日)", "04": "(上4结算日)","05": "(上5结算日)",
    "06": "(上6结算日)", "07": "(上7结算日)", "08": "(上8结算日)",
    "09": "(上9结算日)", "0A": "(上10结算日)", "0B": "(上11结算日)",
    "0C": "(上12结算日)" }
]

dmd_slice_name = [
    {"01": "最大需量及发生时间"},
    {"00": "组合有功", "01": "正向有功", "02": "反向有功",
    "03": "组合无功I", "04": "组合无功II", "05": "第一象限无功",
    "06": "第二象限无功", "07": "第三象限无功", "08": "第四象限无功",
    "09": "正向视在", "0A": "反向视在", "15": "A向正向有功",
    "16": "A相反向有功", "17": "A相组合无功I", "18": "A相组合无功II",
    "19": "A相第一象限无功", "1A": "A相第二象限无功",
    "1B": "A相第三象限无功", "1C": "A相第四象限无功",
    "1D": "A相正向视在", "1E": "A相反向视在", "29": "B相正向有功",
    "2A": "B相反向有功", "2B": "B相组合无功I", "2C": "B相组合无功II",
    "2D": "B相第一象限无功", "2E": "B相第二象限无功",
    "2F": "B相第三象限无功","30": "B相第四象限无功",
    "31": "B相正向视在", "32": "B相反向视在", "3D": "C相正向有功",
    "3E": "C相反向有功", "3F": "C相组合无功I", "40": "C相组合无功II",
    "41": "C相第一象限无功", "42": "C相第二象限无功",
    "43": "C相第三象限无功","44": "C相第四象限无功",
    "45": "C相正向视在", "46": "C相反向视在" },
    {"00": "总", "01": "费率1", "02": "费率2", "03": "费率3",
    "04": "费率4", "05": "费率5", "06": "费率6", "07": "费率7",
    "08": "费率8", "FF": "数据块" },
    {"00": "(当前)","01": "(上1结算日)","02": "(上2结算日)",
    "03": "(上3结算日)", "04": "(上4结算日)","05": "(上5结算日)",
    "06": "(上6结算日)", "07": "(上7结算日)", "08": "(上8结算日)",
    "09": "(上9结算日)", "0A": "(上10结算日)", "0B": "(上11结算日)",
    "0C": "(上12结算日)" }
]

load_curve_slice_name = [
    {"06": "负荷曲线: "
    },
    {"00": "", "01": "第1类负荷", "02": "第2类负荷",
     "03": "第3类负荷", "04": "第4类负荷", "05": "第5类负荷",
     "06": "第6类负荷"
    },
    {"00": ""
    },
    {"00": "最早记录块", "01": "给定时间记录块",
    "02": "最近一个记录块"
    }
]

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

class Id():
    """
    为封装命令模板提供获取发送信息和解析接收数据的方法
    """
    def eng_tx_name(self, id):
        "id: 数据标识，字符串形式,如00000000"

        result = self.get_slice_name(id, eng_slice_name)
        return "".join(formatArray(result, [3, 1, 2, 0]))

    def eng_rx_data(self, data):
        "data: 表示返回帧数据域（已做减33H处理）, 格式为字符串数组"
        import meter
        # 数据标识和每一项电能量数据均占用4字节，按4字节对每一项数据进行分组并反向
        all_items = [item[::-1] for item in meter.splitByLen(data, [4] * 9)]
        result = []
        for item in all_items[1::]:
            result.append(self.format("".join(item), "XXXXXX.XX"))
        return result

    def dmd_tx_name(self, id):
        "id: 数据标识，字符串形式,如00000000"

        result = self.get_slice_name(id, dmd_slice_name)
        return "".join(formatArray(result, [3, 1, 2, 0]))

    def dmd_rx_data(self, data):
        "data: 返回帧数据已做减33H处理, 格式为字符串数组"
        import meter
        # 数据标识和每一项需量数据均占用8字节，按8字节对每一项数据进行分组并反向
        all_items = [item[::-1] for item in meter.splitByLen(data, [4] + [8] * 9)]
        result = []
        for item in all_items[1::]:
            result.append(self.format("".join(item[5:] + item[:5]),
                                      "XX.XXXX,YYMMDDhhmm"))
        return result

    def raw_tx_name(self):
        return ""

    def time_tx_name(self, *id):
        return "抄读时间hhmmss"

    def time_rx_data(self, data):
        return ["".join(data[4:][::-1])]

    def settime_tx_name(self, *time):
        return "设置时间hhmmss: " + self.format(time[0], "hh:mm:ss")

    def setdate_tx_name(self, *date):
        return "设置日期及星期YYMMDDWW: " + self.format(date[0], "YY-MM-DD WW")

    def date_tx_name(self, *id):
        return "抄读日期及星期YYMMDDWW"

    def date_rx_data(self, data):
        return ["".join(data[4:][::-1])]

    def cycle_tx_name(self, id):
        type = {"01": "自动", "02": "按键"}
        return ("抄读" + type[id[4:6]] + "循环显示第" + str(int(id[6:], 16)) +
                "屏显示数据")

    def cycle_rx_data(self, data):
        result = []
        display = "".join(data[4:-1][::-1]) + data[-1]
        result.append(self.format(display, "XXXXXXXX,XX"))
        return result

    def addr_tx_name(self, id):
        return "抄读通信地址"

    def addr_rx_data(self, data):
        return ["".join(data[::-1])]

    def setcycle_tx_name(self, *args):
        """ args: 可变参数，本函数需要两个参数
        args[0]-为循显设置参数格式xxxxxxxxnn
                xxxxxxxx-标识数据标识
                nn-标识屏号
        args[1]-为数据标识
        """
        type = {"01": "自动", "02": "按键"}
        return ("设置" + type[args[1][4:6]] + "循环显示第" +
                str(int(args[1][6:], 16)) + "屏显示数据 " + args[0])

    def reverse_setting_data(self, setting):
        """setting-为命令的设置参数部分
        如命令为:set-cycle-display xxxxxxxx xxxxxxxx,nn，则
        setting的值为xxxxxxxx,nn
        """
        import meter
        reverse_list = []
        set_list = setting.split(',')
        for set in set_list:
            reverse_list.extend(meter.splitByLen(set, [2] * (len(set) // 2))[::-1])
        return reverse_list

    def ldcurve_tx_name(self, id):
        "id: 数据标识，字符串形式,如00000000"

        result = self.get_slice_name(id, load_curve_slice_name)
        return "".join(formatArray(result, [0, 1, 2, 3]))

    def ldcurve_rx_data(self, data):
        "data: 表示返回帧数据域（已做减33H处理）, 格式为字符串数组"
        import meter
        # 将data转为字符串，方便使用正则表达式进行提取
        data_str = " ".join(data)
        # 匹配组提取所需的数据信息
        r = r'.*A0 A0 [\da-fA-F]{2} (\d{2} \d{2} \d{2} \d{2} \d{2} )(.*)AA (.*)AA (.*)AA (.*)AA (.*)AA (.*)AA [\da-fA-F]{2} E5'
        # 每个数据项占用字节数列表，按照负荷曲线数据项的顺序配置，第一项为数据标识
        bl = [[5],     # 存储时刻
              [2, 2, 2, 3, 3, 3, 2],  # 电压、电流、频率
              [3] * 8, # 有、无功功率
              [2] * 4, # 功率因数
              [4] * 4, # 有、无功总电能
              [4] * 4, # 四象限无功总电能
              [3] * 4  # 有、无功需量、零线电流、总视在功率
              ]
        # 每个数据项的数据格式列表
        df = [["YYMMDDhhmm"], # 存储时刻
              ["XXX.X", "XXX.X", "XXX.X", "XXX.XXX", "XXX.XXX", "XXX.XXX",
               "XX.XX"], # 电压、电流、频率
              ["XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX",
               "XX.XXXX", "XX.XXXX", "XX.XXXX"], # 有、无功功率
              ["X.XXX", "X.XXX", "X.XXX", "X.XXX"], # 功率因数
              ["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # 有、无功总电能
              ["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # 四象限无功总电能
              ["XX.XXXX", "XX.XXXX", "XXX.XXX", "XX.XXXX"] # 有、无功需量、零线电流、总视在功率
            ]
        # 提取匹配数据
        data_matched = re.match(r, data_str)
        result = []
        if data_matched:
            data_matched = data_matched.groups()
            # 将tuple类型转化为list，因为需要修改数据的值
            data_matched = list(data_matched)
            # 对数据项进行分组、反序处理
            for i in range((len(data_matched))):
              data_matched[i] = meter.splitByLen(data_matched[i].split(), bl[i])
              for j in range(len(data_matched[i])):
                data_matched[i][j].reverse()

            # 针对数据项进行数据格式处理
            for i in range(len(data_matched)):
              if data_matched[i]:
                for j in range(len(data_matched[i])):
                  data_matched[i][j] = meter.id.format(
                                        "".join(data_matched[i][j]), df[i][j])
            result = []
            for i in data_matched:
                result.extend(i)
        else:
            result = ["返回数据区为空"]
        return result

    def format(self, data, format):
        """返回数据显示格式format要求的字符串数据形式
        data,format 均为字符串形式
        如 format=XXXXXX.XX 返回的数据形式为100326.56
        """
        # TODO: zx 考虑增加参数 **args 可以在数据前添加数据项名，后面添加单位符号

        # 字符串转化为数组，如"abc" to ["a", "b", "c"]
        tolist = list(data)

        for index in range(len(format)):
            if (format[index] in [":", ",", "-", " ", "."]):
                tolist.insert(index, format[index])
        return "".join(tolist)

    def get_slice_name(self, id, slice_name):
        # 需要使用meter模块的splitByLen函数，为防止互相引用导致错误，在此处引用
        import meter
        # 将数据标识进行拆分为4个部分DI3 DI2 DI1 DI0
        split_id = [i.upper() for i in meter.splitByLen(id, [2, 2, 2, 2])]

        # 根据DI3 DI2 DI1 DI0的值从slice_name中获取具体的表示名称数组
        result = []
        for index in range(len(split_id)):
            result.append(slice_name[index][split_id[index]])
        return result

if __name__ == '__main__':
    id = Id();
    print(CMDS[-1]['type'])
    print(CMDS[-1]['pattern'])
    print(eval(CMDS[-1]['txInfo'])('00000000'))
    print(eval(CMDS[-1]['txInfo'])('00010101'))
    print(eval(CMDS[-1]['txInfo'])('0002020c'))
    print(eval(CMDS[-1]['txInfo'])('0003030A'))
    print(eval(CMDS[-1]['txInfo'])('0004040b'))
    print(eval(CMDS[-1]['txInfo'])('0005ff00'))
    print(eval(CMDS[-1]['rxInfo'])('data'))

    print(id.format("00000376", "XXXXXX.XX"))
    print(id.format("1158161604271337", "XX.XXXX,YYMMDDhhmm"))
