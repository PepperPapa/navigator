"""
需量结算测试用例
"""
# 抄读需量的数据标识DI3 DI2 DI1
base_item = ["010100", "010200", "010500", "010600", "010700", "010800", "010900", "010a00"]

# 当前～上12结算日需量数据标识
cur_demand = ["%s00" % i for i in base_item]
lst1_demand = ["%s01" % i for i in base_item]
lst2_demand = ["%s02" % i for i in base_item]
lst3_demand = ["%s03" % i for i in base_item]
lst4_demand = ["%s04" % i for i in base_item]
lst5_demand = ["%s05" % i for i in base_item]
lst6_demand = ["%s06" % i for i in base_item]
lst7_demand = ["%s07" % i for i in base_item]
lst8_demand = ["%s08" % i for i in base_item]
lst9_demand = ["%s09" % i for i in base_item]
lst10_demand = ["%s0a" % i for i in base_item]
lst11_demand = ["%s0b" % i for i in base_item]
lst12_demand = ["%s0c" % i for i in base_item]


# 存储结算日需量
billing_demand = []

billing_demand.extend(["当前需量"])
for id in cur_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上1结算日需量"])
for id in lst1_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上2结算日需量"])
for id in lst2_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上3结算日需量"])
for id in lst3_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上4结算日需量"])
for id in lst4_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上5结算日需量"])
for id in lst5_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上6结算日需量"])
for id in lst6_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上7结算日需量"])
for id in lst7_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上8结算日需量"])
for id in lst8_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上9结算日需量"])
for id in lst9_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上10结算日需量"])
for id in lst10_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上11结算日需量"])
for id in lst11_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["上12结算日需量"])
for id in lst12_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

# 打印当前～上12结算日需量数据
for d in billing_demand:
  print(d)



