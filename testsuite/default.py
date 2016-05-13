r = r'.*A0 A0 [\da-fA-F]{2} (\d{2} \d{2} \d{2} \d{2} \d{2} )(.*)AA (.*)AA (.*)AA (.*)AA (.*)AA (.*)AA [\da-fA-F]{2} E5'
# 每个数据项占用字节数列表，按照负荷曲线数据项的顺序配置，第一项为数据标识
bl = [[5],     # 存储时刻
[2, 2, 2, 3, 3, 3, 2],  # 电压、电流、频率
[3] * 8, # 有、无功功率
[2] * 4, # 功率因数
[4] * 4, # 有、无功总电能
[4] * 4, # 四象限无功总电能
[3] * 4  # 有、无功需量、零线电流、总视在功率
]
# 每个数据项的数据格式列表
df = [["YYMMDDhhmm"], # 存储时刻
["XXX.X", "XXX.X", "XXX.X", "XXX.XXX", "XXX.XXX", "XXX.XXX",
"XX.XX"], # 电压、电流、频率
["XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX",
"XX.XXXX", "XX.XXXX", "XX.XXXX"], # 有、无功功率
["X.XXX", "X.XXX", "X.XXX", "X.XXX"], # 功率因数
["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # 有、无功总电能
["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # 四象限无功总电能
["XX.XXXX", "XX.XXXX", "XXX.XXX", "XX.XXXX"] # 有、无功需量、零线电流、总视在功率
]

m = meter.minus33H("35 33 33 39 D3 D3 4F 38 33 34 34 4A CC 56 43 57 3A 57 33 33 33 33 33 33 33 33 33 33 83 DD DD DD DD DD DD 14 18".split())
m = " ".join(m)

m = re.match(r, m).groups()
m = list(m)

for i in range(len(m)):
  m[i] = m[i].split()
  m[i] = meter.splitByLen(m[i], bl[i])
  for j in range(len(m[i])):
    m[i][j].reverse()

for i in range(len(m)):
  if m[i]:
    for j in range(len(m[i])):
      m[i][j] = meter.id.format("".join(m[i][j]), df[i][j])



print(m)
