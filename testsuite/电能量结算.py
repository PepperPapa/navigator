"""
�����������������
"""
# �������ܵ����ݱ�ʶDI3 DI2 DI1
base_item = ["000100", "000200", "000500", "000600", "000700", "000800", "000900", "000a00"]

# ��ǰ����12�����յ������ݱ�ʶ
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


# �洢�����յ���
billing_energy = []

billing_energy.extend(["��ǰ����"])
for id in cur_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��1�����յ���"])
for id in lst1_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��2�����յ���"])
for id in lst2_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��3�����յ���"])
for id in lst3_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��4�����յ���"])
for id in lst4_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��5�����յ���"])
for id in lst5_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��6�����յ���"])
for id in lst6_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��7�����յ���"])
for id in lst7_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��8�����յ���"])
for id in lst8_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��9�����յ���"])
for id in lst9_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��10�����յ���"])
for id in lst10_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��11�����յ���"])
for id in lst11_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

billing_energy.extend(["��12�����յ���"])
for id in lst12_energy:
  billing_energy.extend(psend(":get-energy %s" % id))

# ��ӡ��ǰ����12�����յ�������
for d in billing_energy:
  print(d)

