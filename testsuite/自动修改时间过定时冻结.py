# �Զ��޸�ʱ�����ʱ����
# 1.�Զ��޸�ʱ�����ʱ����㣺 ��ʱ�������ã�99999925-��СʱΪ���ڶ�ʱ����
# 2.������ 63��(310���Գ�����62���ն�������)
import time

hours = tuple("{0:02}".format(h) for h in range(24))
for t in range(63):
  psend(":set-time 04000102 %s" % hours[t % 23] + "2445")
  psend(":get-date 04000101")
  psend(":get-time 04000102")
  print("freeze times: %s" % t)
  time.sleep(25)


