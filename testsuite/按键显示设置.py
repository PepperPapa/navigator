# 设置按键循显
psend(":get-addr")

# 1. 按键循显项的数据标识
num = 6
manual_cycle = ["040402" + "{0:02X}".format(i) for i in range(1, num + 1)]
data = """00150000
00160000
00290000
002A0000
003D0000
003E0000
""".split("\n")[:-1]
data = [id + ",00" for id in data]
print(data)
for i in range(len(manual_cycle)):
  psend(":set-cycle-display " + manual_cycle[i] + " " + data[i])
  psend(":get-cycle-display " + manual_cycle[i])


