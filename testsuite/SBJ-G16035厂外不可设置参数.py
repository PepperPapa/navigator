""" 
�������ü��Բ���--��������
"""
psend(":get-addr")

# 04040201~04040278 �Զ�ѭ��1��120��
auto_cycle = ["040402" + "{0:02X}".format(i) for i in range(1, 121)]
for item in auto_cycle:
  lcd_para = psend(":get-cycle-display %s" % item)
  psend(":set-cycle-display %s %s" % (item, lcd_para[0]))
