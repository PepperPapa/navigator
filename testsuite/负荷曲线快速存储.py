import time
for i in range(5):
  t=psend(":get-time 04000102")
  t1 = t[0][:-2] + "58"
  print(t1)
  psend(":set-time 04000102 " + t1)
  psend(":get-time 04000102")
  time.sleep(3)
