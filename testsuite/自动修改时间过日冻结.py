# 自动修改时间过日冻结
# 1.自动修改时间过冻结点： 00点00分
# 2.共冻结 63次(310可以抄读上62次日冻结数据)
import time

for t in range(63):
  psend(":set-time 04000102 235950")
  psend(":get-date 04000101")
  psend(":get-time 04000102")
  print("freeze times: %s" % t)
  time.sleep(25)

