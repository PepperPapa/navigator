r = r'.*A0 A0 [\da-fA-F]{2} (\d{2} \d{2} \d{2} \d{2} \d{2} )(.*)AA (.*)AA (.*)AA (.*)AA (.*)AA (.*)AA [\da-fA-F]{2} E5'
# ÿ��������ռ���ֽ����б����ո��������������˳�����ã���һ��Ϊ���ݱ�ʶ
bl = [[5],     # �洢ʱ��
[2, 2, 2, 3, 3, 3, 2],  # ��ѹ��������Ƶ��
[3] * 8, # �С��޹�����
[2] * 4, # ��������
[4] * 4, # �С��޹��ܵ���
[4] * 4, # �������޹��ܵ���
[3] * 4  # �С��޹����������ߵ����������ڹ���
]
# ÿ������������ݸ�ʽ�б�
df = [["YYMMDDhhmm"], # �洢ʱ��
["XXX.X", "XXX.X", "XXX.X", "XXX.XXX", "XXX.XXX", "XXX.XXX",
"XX.XX"], # ��ѹ��������Ƶ��
["XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX", "XX.XXXX",
"XX.XXXX", "XX.XXXX", "XX.XXXX"], # �С��޹�����
["X.XXX", "X.XXX", "X.XXX", "X.XXX"], # ��������
["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # �С��޹��ܵ���
["XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX", "XXXXXX.XX"], # �������޹��ܵ���
["XX.XXXX", "XX.XXXX", "XXX.XXX", "XX.XXXX"] # �С��޹����������ߵ����������ڹ���
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
