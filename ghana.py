"""
python 3.5
加纳表扣费模块
"""
import pprint

CONSUME_MODE = '01'
# CHARGE_SERVICE = [2.1333, 6.3317, 6.3317, 6.3317, 6.3317, 6.3317, 6.3317, 6.3317, 6.3317, 6.3317]
CHARGE_SERVICE = [10.5529] * 8
# 百分比
TARIFF_ROADLIGHT = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
TARIFF_GOV = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
TARIFF_VAT = [17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5]

NUM_STEPS = 2
STEPS = [300, 600, 300, 600, 0, 0, 0, 0]
# TARIFF_STEPS = [0.3356, 0.6733, 0.6733, 0.8738, 0.9709, 0, 0, 0, 0]
TARIFF_STEPS = [0.9679, 1.0300, 1.6251]
TARIFF_SUBSIDY = [0.0498, 0.0265, 0.0209, 0.0209, 0.0209, 0.0209, 0.0209, 0.0209, 0.0209, 0.0209]
MENU = """
0: 显示帮助
1: 更新或查询电量
2: 更新或查询剩余金额
3: 计算扣费
4: 查询当前运行的阶梯
5: 设置新阶梯值
6: 设置用电模式
7: 设置新阶梯电价
exit: 退出程序
"""

def push(container, *value, deep = 2):
    if value[0]:
        container.append(float(*value))
        if len(container) > deep:
            return container[1:]
    return container

def innum(tip):
    value = input(tip)
    if len(value) > 0:
        return value

def inarr(tip):
    arr = input(tip)
    if len(arr) > 0:
        arr = arr.split(' ')
        return [float(v) for v in arr]
    
class Ghana:
    def __init__(self):
        self.charge_service = CHARGE_SERVICE
        self.tariff_roadlight = TARIFF_ROADLIGHT
        self.tariff_gov = TARIFF_GOV
        self.tariff_vat = TARIFF_VAT
        self.num_steps = NUM_STEPS
        self.steps = STEPS
        self.tariff_steps = TARIFF_STEPS
        self.tariff_subsidy = TARIFF_SUBSIDY
        self.energy = []
        self.money = []
        self.consume_mode = CONSUME_MODE

    def set_steps(self, new_steps):
        self.steps = new_steps
        
    def set_tariff_steps(self, new_tariff_steps):
        self.tariff_steps = new_tariff_steps
        
    def set_consume_mode(self, mode):
        if mode:
            self.consume_mode = mode
        return self.consume_mode
    
    def eng(self, *energy):
        self.energy = push(self.energy, *energy)
        return self.energy

    def mon(self, *remain_money):
        self.money = push(self.money, *remain_money)
        return self.money

    def currentStep(self, U):
        # 根据当前电量计算运行的是哪个阶梯
        for i in range(self.num_steps):
            if U <= self.steps[i]:
                return i
        return i + 1

    def _preStepConsume(self, index_step):
        print(self.cum)
        if index_step == 0:
            self.cum["energy_charge"] += self.steps[0] * self.tariff_steps[0]
             # VAT税
            if self.consume_mode == "01":
                self.cum["vat_charge"] += ((self.tariff_steps[0] - self.tariff_subsidy[0]) * self.steps[0]
                                           * self.tariff_vat[0] / 100)
            return
        else:
            step_eng = self.steps[index_step] - self.steps[index_step - 1]
            self.cum["energy_charge"] += step_eng * self.tariff_steps[index_step]
             # VAT税
            if self.consume_mode == "01":
                self.cum["vat_charge"] += ((self.tariff_steps[index_step] - self.tariff_subsidy[index_step]) * step_eng
                                           * self.tariff_vat[index_step] / 100)
                print(self.cum)
            self._preStepConsume(index_step - 1)

    def consume(self):
        self.cum = {"energy_charge": 0,
                    "vat_charge": 0}
        index_step = self.currentStep(self.energy[1])
        U = self.energy[1]
        if index_step == 0:
            self.cum["energy_charge"] = (U * self.tariff_steps[0])
            # VAT税
            if self.consume_mode == "01":
                self.cum["vat_charge"] = ((self.charge_service[0] +
                                           (self.tariff_steps[0] - self.tariff_subsidy[0]) * U)
                                           * self.tariff_vat[0] / 100)
        else:
            pre_step = self.steps[index_step - 1]
            self.cum["energy_charge"] = ((U - pre_step) * self.tariff_steps[index_step])
            # VAT税
            if self.consume_mode == "01":
                self.cum["vat_charge"] = ((self.charge_service[index_step] +
                                           (self.tariff_steps[index_step] - self.tariff_subsidy[index_step]) * (U - pre_step))
                                           * self.tariff_vat[index_step] / 100)
            self._preStepConsume(index_step - 1)

        price_gov = self.tariff_gov[index_step] / 100
        price_roadlight = self.tariff_roadlight[index_step] / 100
        charge_service = self.charge_service[index_step]
        self.cum["service_charge"] = charge_service
        self.cum["gov_tax"] = (self.cum["energy_charge"] * price_gov)
        self.cum["roadlight_tax"] = (self.cum["energy_charge"] * price_roadlight)
        self.cum["total"] = sum([v for k,v in self.cum.items()])
        return self.cum

gn = Ghana()

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    while (True):
        cmd = input(">>> ")
        if cmd == "0":
            print(MENU)
        elif cmd == "1":
            pp.pprint(gn.eng(innum("更新电量|回车: ")))
        elif cmd == "2":
            pp.pprint(gn.mon(innum("更新剩余金额|回车: ")))
        elif cmd == "3":
            pp.pprint(gn.consume())
        elif cmd == "4":
            pp.pprint("当前运行阶梯序号: %s" % gn.currentStep(gn.energy[1]))
        elif cmd == "5":
            new_steps = inarr("设置阶梯值: ")
            if new_steps:
                gn.set_steps(new_steps)
            pp.pprint(gn.steps)
        elif cmd == "6":
            print(gn.set_consume_mode(input("00-居民用电|01-非居民用电: ")))
        elif cmd == "7":
            new_tariff_steps = inarr("设置阶梯电价: ")
            if new_tariff_steps:
                gn.set_tariff_steps(new_tariff_steps)
            pp.pprint(gn.tariff_steps)
        elif cmd == "exit":
            break
        else:
            # 这里用于输入计算公式，未做校验，如 2+3*8
            if len(cmd) > 0:
                print(eval(cmd))
