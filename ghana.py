"""
python 3.5
加纳表扣费模块
"""

PRICE_SERVICE = [2.1333, 6.3317, 6.3317, 6.3317, 0, 0, 0, 0, 0, 0]
TARIFF_ROADLIGHT = [5, 5, 5, 5, 0, 0, 0, 0, 0, 0]
TARIFF_GOV = [5, 5, 5, 5, 0, 0, 0, 0, 0, 0]
TARIFF_VAT = [17.5, 17.5, 17.5, 17.5, 0, 0, 0, 0, 0, 0]

def push(container, *value, deep = 2):
    if value:
        container.append(*value)
        if len(container) > deep:
            return container[1:]
    return container


class Ghana:
    def __init__(self):
        self.price_service = PRICE_SERVICE
        self.tariff_roadlight = TARIFF_ROADLIGHT
        self.tariff_gov = TARIFF_GOV
        self.tariff_vat = TARIFF_VAT
        self.energy = []
        self.money = []

    def eng(self, *energy):
        self.energy = push(self.energy, *energy)
        return self.energy

    def mon(self, *remain_money):
        self.money = push(self.money, *remain_money)
        return self.money


gn = Ghana()
if __name__ == '__main__':
    print(gn.eng())
    print(gn.eng(22.18))
    print(gn.eng(103.17))
    print(gn.eng(33.44))
    print(gn.mon())
    print(gn.mon(22.18))
    print(gn.mon(103.17))
    print(gn.mon(33.44))
