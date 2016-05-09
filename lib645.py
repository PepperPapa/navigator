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

CMDS = [
    # {
    #  'rule': '^:get-load-curve \d{8}( add-(\d)+)?$',
    #  'txFormat': {
    #     'slice': [2]*4,
    #     'order': [0, 1, 2, 3],
    #     'item': [
    #             {"06": "负荷曲线: "
    #             },
    #             {"00": "", "01": "第1类负荷", "02": "第2类负荷",
    #              "03": "第3类负荷", "04": "第4类负荷", "05": "第5类负荷",
    #              "06": "第6类负荷"
    #             },
    #             {"00": ""
    #             },
    #             {"00": "最早记录块", "01": "给定时间记录块",
    #             "02": "最近一个记录块"
    #             }
    #            ]
    #    },
    #  'rxFormat': {
    #     'unit': [[5, 2, 2, 2, 3, 3, 3, 2],
    #              [3] * 8,
    #              [2] * 4,
    #              [4] * 4,
    #              [4] * 4,
    #              [3] * 4
    #             ],
    #     'style': [["{0}{1}{2}{3}{4}", "{0}{1[0]}.{1[1]}", "{0}{1[0]}.{1[1]}",
    #                "{0}{1[0]}.{1[1]}", "{0}{1[0]}.{1[1]}{2}",
    #                "{0}{1[0]}.{1[1]}{2}", "{0}{1[0]}.{1[1]}{2}",
    #                "{0}.{1}"],
    #               ["{0}.{1}{2}"] * 8,
    #               ["{0[0]}.{0[1]}{1}"] * 4,
    #               ["{0}{1}{2}.{3}"] * 4,
    #               ["{0}{1}{2}.{3}"] * 4,
    #               ["{0}.{1}{2}", "{0}.{1}{2}", "{0}{1[0]}.{1[1]}{2}", "{0}.{1}{2}"]
    #             ],
    #     }
    # },
    # {
    #  'rule': '^:set-time (\d\d){3}$',
    #  'id': "04000102",
    #  'code': '14',
    #  'len': '0F',
    #  'txFormat': "设置时间(hhmmss)"
    # },
    # {
    #  'rule': '^:set-date (\d\d){4}$',
    #  'id': "04000101",
    #  'code': '14',
    #  'len': '10',
    #  'txFormat': "设置日期及星期(YYMMDDWW)"
    # },

    {'type': 0,
     'pattern': '^:get-energy \d\d\d[\da-fA-F][\dfF][\dfF]\d[\da-cA-C]$',
     'txInfo': 'id.eng_tx_name',
     'rxInfo': 'id.eng_rx_data'
     },
    {'type': 0,
    'pattern': '^:get-demand \d\d\d[\da-fA-F][\dfF][\dfF]\d[\da-cA-C]$',
    'txInfo': 'id.dmd_tx_name',
    'rxInfo': 'id.dmd_rx_data'
    },
    {'type': 20,    # 20表示原始命令帧
     'pattern': '^68 ([\da-fA-F]{2} ){6}68 ([\da-fA-F]{2} )+16$',
     'txInfo': 'id.raw_tx_name',
     'rxInfo': 'id.raw_rx_data'
     },
    {'type': 0,
     'pattern': '^:get-time 04000102$',
     'txInfo': 'id.time_tx_name',
     'rxInfo': 'id.time_rx_data'
    },
    {'type': 0,
     'pattern': '^:get-date 04000101$',
     'txInfo': 'id.date_tx_name',
     'rxInfo': 'id.date_rx_data'
    },
    #  TODO: zx 还未实现
    {'type': 0,
     'pattern': '^:get-load-curve \d{8}( add-(\d)+)?$',
     'txInfo': 'id.ldcurve_tx_name',
     'rxInfo': 'id.ldcurve_rx_data'
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

    def raw_rx_data(self):
        return ""

    def time_tx_name(self, *id):
        return "时间hhmmss:"

    def time_rx_data(self, data):
        return ["".join(data[4:][::-1])]

    def date_tx_name(self, *id):
        return "日期及星期YYMMDDWW:"

    def date_rx_data(self, data):
        return ["".join(data[4:][::-1])]

    def ldcurve_tx_name(self, id):
        "id: 数据标识，字符串形式,如00000000"
        pass

    def ldcurve_rx_data(self):
        pass

    def format(self, data, format):
        """返回数据显示格式format要求的字符串数据形式
        data,format 均为字符串形式
        如 format=XXXXXX.XX 返回的数据形式为100326.56
        """
        tolist = list(data)
        for index in range(len(format)):
            if format[index] == "," or format[index] == ".":
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
