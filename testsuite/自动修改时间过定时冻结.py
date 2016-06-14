# 自动修改时间过定时冻结
# 1.自动修改时间过定时冻结点： 定时冻结设置：99999925-以小时为周期定时冻结
# 2.共冻结 63次(310可以抄读上62次日冻结数据)
import time

hours = tuple("{0:02}".format(h) for h in range(24))
for t in range(63):
  psend(":set-time 04000102 %s" % hours[t % 23] + "2445")
  psend(":get-date 04000101")
  psend(":get-time 04000102")
  print("freeze times: %s" % t)
  time.sleep(25)


