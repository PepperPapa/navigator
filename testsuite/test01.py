for i in range(5):
  psend(":get-time")
  psend(":dut-set ioff")
  time.sleep(20)
  psend(":dut-set ion")
  time.sleep(20)
