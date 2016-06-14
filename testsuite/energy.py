import time
eng_type = ["00", "01", "02", "05", "06", "07", "08", "09", "0A", "15", "16", "1D", "1E", "29", "2A", "31", "32", "3D", "3E", "45", "46"]

data = [time.time(), "当前电能"]
# 当前抄读电能数据标识
cur_eng = ["00" + item + "0000" for item in eng_type]
for id in cur_eng:
  data.append(psend(":get-energy " + id))

# 上1结算日抄读电能数据标识
data.append("上1结算日电能")
last1_eng = ["00" + item + "0001" for item in eng_type]
for id in last1_eng:
  data.append(psend(":get-energy " + id))


# 上2结算日抄读电能数据标识
data.append("上2结算日电能")
last2_eng = ["00" + item + "0002" for item in eng_type]
for id in last2_eng:
  data.append(psend(":get-energy " + id))

# 上3结算日抄读电能数据标识
data.append("上3结算日电能")
last3_eng = ["00" + item + "0003" for item in eng_type]
for id in last3_eng:
  data.append(psend(":get-energy " + id))

# 上4结算日抄读电能数据标识
data.append("上4结算日电能")
last4_eng = ["00" + item + "0004" for item in eng_type]
for id in last4_eng:
  data.append(psend(":get-energy " + id))

# 上5结算日抄读电能数据标识
data.append("上5结算日电能")
last5_eng = ["00" + item + "0005" for item in eng_type]
for id in last5_eng:
  data.append(psend(":get-energy " + id))

# 上6结算日抄读电能数据标识
data.append("上6结算日电能")
last6_eng = ["00" + item + "0006" for item in eng_type]
for id in last6_eng:
  data.append(psend(":get-energy " + id))

# 上7结算日抄读电能数据标识
data.append("上7结算日电能")
last7_eng = ["00" + item + "0007" for item in eng_type]
for id in last7_eng:
  data.append(psend(":get-energy " + id))

# 上8结算日抄读电能数据标识
data.append("上8结算日电能")
last8_eng = ["00" + item + "0008" for item in eng_type]
for id in last8_eng:
  data.append(psend(":get-energy " + id))

# 上9结算日抄读电能数据标识
data.append("上9结算日电能")
last9_eng = ["00" + item + "0009" for item in eng_type]
for id in last9_eng:
  data.append(psend(":get-energy " + id))

# 上10结算日抄读电能数据标识
data.append("上10结算日电能")
last10_eng = ["00" + item + "000a" for item in eng_type]
for id in last10_eng:
  data.append(psend(":get-energy " + id))

# 上11结算日抄读电能数据标识
data.append("上11结算日电能")
last11_eng = ["00" + item + "000b" for item in eng_type]
for id in last11_eng:
  data.append(psend(":get-energy " + id))

# 上12结算日抄读电能数据标识
data.append("上12结算日电能")
last12_eng = ["00" + item + "000c" for item in eng_type]
for id in last12_eng:
  data.append(psend(":get-energy " + id))

for d in data:
  print(d)

