"""
���������������
"""
# �������������ݱ�ʶDI3 DI2 DI1
base_item = ["010100", "010200", "010500", "010600", "010700", "010800", "010900", "010a00"]

# ��ǰ����12�������������ݱ�ʶ
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


# �洢����������
billing_demand = []

billing_demand.extend(["��ǰ����"])
for id in cur_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��1����������"])
for id in lst1_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��2����������"])
for id in lst2_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��3����������"])
for id in lst3_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��4����������"])
for id in lst4_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��5����������"])
for id in lst5_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��6����������"])
for id in lst6_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��7����������"])
for id in lst7_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��8����������"])
for id in lst8_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��9����������"])
for id in lst9_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��10����������"])
for id in lst10_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��11����������"])
for id in lst11_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

billing_demand.extend(["��12����������"])
for id in lst12_demand:
  billing_demand.extend(psend(":get-demand %s" % id))

# ��ӡ��ǰ����12��������������
for d in billing_demand:
  print(d)



