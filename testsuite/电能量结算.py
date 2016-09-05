"""
电能量结算测试用例
"""
# 抄读电能的数据标识DI3 DI2 DI1
base_item = ["000100", "000200", "000500", "000600", "000700", "000800", "000900", "000a00"]

# 当前～上12结算日电能数据标识
cur_energy = ["%s00" % i for i in base_item]
lst1_energy = ["%s01" % i for i in base_item]
lst2_energy = ["%s02" % i for i in base_item]
lst3_energy = ["%s03" % i for i in base_item]
lst4_energy = ["%s04" % i for i in base_item]
lst5_energy = ["%s05" % i for i in base_item]
lst6_energy = ["%s06" % i for i in base_item]
lst7_energy = ["%s07" % i for i in base_item]
lst8_energy = ["%s08" % i for i in base_item]
lst9_energy = ["%s09" % i for i in base_item]
lst10_energy = ["%s0a" % i for i in base_item]
lst11_energy = ["%s0b" % i for i in base_item]
lst12_energy = ["%s0c" % i for i in base_item]


# 存储结算日电能
billing_energy = []

billing_energy.extend(["当前电能"])
for id in cur_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上1结算日电能"])
for id in lst1_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上2结算日电能"])
for id in lst2_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上3结算日电能"])
for id in lst3_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上4结算日电能"])
for id in lst4_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上5结算日电能"])
for id in lst5_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上6结算日电能"])
for id in lst6_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上7结算日电能"])
for id in lst7_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上8结算日电能"])
for id in lst8_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上9结算日电能"])
for id in lst9_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上10结算日电能"])
for id in lst10_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上11结算日电能"])
for id in lst11_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["上12结算日电能"])
for id in lst12_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

# 打印当前～上12结算日电能数据
for d in billing_energy:
  print(d)

