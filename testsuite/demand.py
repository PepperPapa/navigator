"""当前抄读需量数据标识"""
cur_dmd = ["01010000", "01020000", "01050000", "01060000", "01070000", "01080000", "01090000", "010A0000", "01150000", "01160000", "01290000", "012A0000", "013D0000", "013E0000"]
for id in cur_dmd:
  psend(":get-demand " + id)

"""上1结算日需量数据标识"""
ls1_dmd = ["01010001", "01020001", "01090001", "010A0001"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上2结算日需量数据标识
ls1_dmd = ["01010002", "01020002", "01090002", "010A0002"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上3结算日需量数据标识
ls1_dmd = ["01010003", "01020003", "01090003", "010A0003"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上4结算日需量数据标识
ls1_dmd = ["01010004", "01020004", "01090004", "010A0004"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上5结算日需量数据标识
ls1_dmd = ["01010005", "01020005", "01090005", "010A0005"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上6结算日需量数据标识
ls1_dmd = ["01010006", "01020006", "01090006", "010A0006"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上7结算日需量数据标识
ls1_dmd = ["01010007", "01020007", "01090007", "010A0007"]
for id in ls1_dmd:
  psend(":get-demand " + id)

# 上8结算日需量数据标识
ls1_dmd = ["01010008", "01020008", "01090008", "010A0008"]
for id in ls1_dmd:
  psend(":get-demand " + id)

"""上9结算日需量数据标识"""
ls1_dmd = ["01010009", "01020009", "01090009", "010A0009"]
for id in ls1_dmd:
  psend(":get-demand " + id)

"""上10结算日需量数据标识"""
ls1_dmd = ["0101000a", "0102000a", "0109000a", "010A000a"]
for id in ls1_dmd:
  psend(":get-demand " + id)

"""上11结算日需量数据标识"""
ls1_dmd = ["0101000b", "0102000b", "0109000b", "010A000b"]
for id in ls1_dmd:
  psend(":get-demand " + id)

"""上12结算日需量数据标识"""
ls1_dmd = ["0101000c", "0102000c", "0109000c", "010A000c"]
for id in ls1_dmd:
  psend(":get-demand " + id)



