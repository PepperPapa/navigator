"""
python 3.5
加纳表扣费模块
"""
import pprint

CHARGE_SERVICE = [2.1333, 6.3317, 6.3317, 6.3317, 0, 0, 0, 0, 0, 0]
# 百分比
TARIFF_ROADLIGHT = [5, 5, 5, 5, 0, 0, 0, 0, 0, 0]
TARIFF_GOV = [5, 5, 5, 5, 0, 0, 0, 0, 0, 0]
TARIFF_VAT = [17.5, 17.5, 17.5, 17.5, 0, 0, 0, 0, 0, 0]

NUM_STEPS = 4
STEPS = [0.5, 1.5, 3, 6, 0, 0, 0, 0]
TARIFF_STEPS = [0.3356, 0.6733, 0.6733, 0.8738, 0.9709, 0, 0, 0, 0]
MENU = """
0: 显示帮助
1: 更新或查询电量
2: 更新或查询剩余金额
3: 计算扣费
4: 查询当前运行的阶梯
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

class Ghana:
    def __init__(self):
        self.charge_service = CHARGE_SERVICE
        self.tariff_roadlight = TARIFF_ROADLIGHT
        self.tariff_gov = TARIFF_GOV
        self.tariff_vat = TARIFF_VAT
        self.num_steps = NUM_STEPS
        self.steps = STEPS
        self.tariff_steps = TARIFF_STEPS
        self.energy = []
        self.money = []

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
        if index_step == 0:
            self.cum["energy_charge"] += self.steps[0] * self.tariff_steps[0]
            return
        else:
            step_eng = self.steps[index_step] - self.steps[index_step - 1]
            self.cum["energy_charge"] += step_eng * self.tariff_steps[index_step]
            self._preStepConsume(index_step - 1)

    def consume(self):
        self.cum = {"energy_charge": 0}
        index_step = self.currentStep(self.energy[1])
        U = self.energy[1]
        if index_step == 0:
            self.cum["energy_charge"] = (U * self.tariff_steps[index_step])
        else:
            pre_step = self.steps[index_step - 1]
            self.cum["energy_charge"] = ((U - pre_step) * self.tariff_steps[index_step])
            self._preStepConsume(index_step - 1)

        if index_step >= self.num_steps - 1:
            price_gov = self.tariff_gov[index_step - 1] / 100
            price_roadlight = self.tariff_roadlight[index_step - 1] / 100
            charge_service = self.charge_service[index_step - 1]
        else:
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
        if cmd == "1":
            pp.pprint(gn.eng(innum("更新电量|回车: ")))
        if cmd == "2":
            pp.pprint(gn.mon(innum("更新剩余金额|回车: ")))
        if cmd == "3":
            pp.pprint(gn.consume())
        if cmd == "4":
            pp.pprint("当前运行阶梯序号: %s" % gn.currentStep(gn.energy[1]))

        if cmd == "exit":
            break
        else:
            # 这里用于输入计算公式，未做校验，如 2+3*8
            print(eval(cmd))
