import time
eng_type = ["00", "01", "02", "05", "06", "07", "08", "09", "0A", "15", "16", "1D", "1E", "29", "2A", "31", "32", "3D", "3E", "45", "46"]

data = [time.time(), "��ǰ����"]
# ��ǰ�����������ݱ�ʶ
cur_eng = ["00" + item + "0000" for item in eng_type]
for id in cur_eng:
  data.append(psend(":get-energy " + id))

# ��1�����ճ����������ݱ�ʶ
data.append("��1�����յ���")
last1_eng = ["00" + item + "0001" for item in eng_type]
for id in last1_eng:
  data.append(psend(":get-energy " + id))


# ��2�����ճ����������ݱ�ʶ
data.append("��2�����յ���")
last2_eng = ["00" + item + "0002" for item in eng_type]
for id in last2_eng:
  data.append(psend(":get-energy " + id))

# ��3�����ճ����������ݱ�ʶ
data.append("��3�����յ���")
last3_eng = ["00" + item + "0003" for item in eng_type]
for id in last3_eng:
  data.append(psend(":get-energy " + id))

# ��4�����ճ����������ݱ�ʶ
data.append("��4�����յ���")
last4_eng = ["00" + item + "0004" for item in eng_type]
for id in last4_eng:
  data.append(psend(":get-energy " + id))

# ��5�����ճ����������ݱ�ʶ
data.append("��5�����յ���")
last5_eng = ["00" + item + "0005" for item in eng_type]
for id in last5_eng:
  data.append(psend(":get-energy " + id))

# ��6�����ճ����������ݱ�ʶ
data.append("��6�����յ���")
last6_eng = ["00" + item + "0006" for item in eng_type]
for id in last6_eng:
  data.append(psend(":get-energy " + id))

# ��7�����ճ����������ݱ�ʶ
data.append("��7�����յ���")
last7_eng = ["00" + item + "0007" for item in eng_type]
for id in last7_eng:
  data.append(psend(":get-energy " + id))

# ��8�����ճ����������ݱ�ʶ
data.append("��8�����յ���")
last8_eng = ["00" + item + "0008" for item in eng_type]
for id in last8_eng:
  data.append(psend(":get-energy " + id))

# ��9�����ճ����������ݱ�ʶ
data.append("��9�����յ���")
last9_eng = ["00" + item + "0009" for item in eng_type]
for id in last9_eng:
  data.append(psend(":get-energy " + id))

# ��10�����ճ����������ݱ�ʶ
data.append("��10�����յ���")
last10_eng = ["00" + item + "000a" for item in eng_type]
for id in last10_eng:
  data.append(psend(":get-energy " + id))

# ��11�����ճ����������ݱ�ʶ
data.append("��11�����յ���")
last11_eng = ["00" + item + "000b" for item in eng_type]
for id in last11_eng:
  data.append(psend(":get-energy " + id))

# ��12�����ճ����������ݱ�ʶ
data.append("��12�����յ���")
last12_eng = ["00" + item + "000c" for item in eng_type]
for id in last12_eng:
  data.append(psend(":get-energy " + id))

for d in data:
  print(d)

