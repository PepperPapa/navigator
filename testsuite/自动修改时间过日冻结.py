# �Զ��޸�ʱ����ն���
# 1.�Զ��޸�ʱ�������㣺 00��00��
# 2.������ 63��(310���Գ�����62���ն�������)
import time

for t in range(63):
  psend(":set-time 04000102 235950")
  psend(":get-date 04000101")
  psend(":get-time 04000102")
  print("freeze times: %s" % t)
  time.sleep(25)

