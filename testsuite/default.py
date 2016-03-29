for i in range(1):
  psend(":get-time")
  psend(":dut-set ioff")
  time.sleep(10)
  psend(":dut-set ion")
  time.sleep(10)

