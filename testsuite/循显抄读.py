# �Զ�ѭ��1��24������
auto_cycle = ["040401" + "{0:02X}".format(i) for i in range(1, 25)]
for item in auto_cycle:
  psend(":get-cycle-display " + item)

# ����ѭ��1��24������
manual_cycle = ["040402" + "{0:02X}".format(i) for i in range(1, 25)]
for item in manual_cycle:
  psend(":get-cycle-display " + item)
