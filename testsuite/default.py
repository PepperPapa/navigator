import time

for i in range(10):
  r = psend(":get-load-curve 06000002 add-01")
  print(r)
  time.sleep(30)

# ��
:get-load-curve 06000000 add-01
:get-load-curve 06000001 add-170101012801
:get-load-curve 06000002 add-01
# 1�ฺ��
:get-load-curve 06010000 add-01
:get-load-curve 06010001 add-160513090001
:get-load-curve 06010002 add-01
# 2�ฺ��
:get-load-curve 06020000 add-01
:get-load-curve 06020001 add-160513090001
:get-load-curve 06020002 add-01
# 3�ฺ��
:get-load-curve 06030000 add-01
:get-load-curve 06030001 add-160513090001
:get-load-curve 06030002 add-01
# 4�ฺ��
:get-load-curve 06040000 add-01
:get-load-curve 06040001 add-160513090001
:get-load-curve 06040002 add-01
# 5�ฺ��
:get-load-curve 06050000 add-01
:get-load-curve 06050001 add-160513090001
:get-load-curve 06050002 add-01
# 6�ฺ��
:get-load-curve 06060000 add-01
:get-load-curve 06060001 add-160513090001
:get-load-curve 06060002 add-01
