:get-addr
:get-time 04000102
:get-date 04000101

a=psend(":get-load-curve 06000000 add-03")
for i in a:
  print(i)

for i in range(100):
psend(":get-addr")


