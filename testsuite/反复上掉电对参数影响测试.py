# 
# ���⣺ ���ӵ����������ϵ�����֤������������ѭ�ԡ����Բ����ޱ仯
#
import time

# ��Ƽӵ�ѹ
psend(":dut-set uon")
time.sleep(15)

# ���ȳ���һ����Ҫ�Ƚϵ�����
# ������������
e_base = ["000000", "000100", "000200", "000500", "000600", "000700", "000800", "000900", "000A00"]
energy_id = [id + "{0:02X}".format(0) for id in e_base] + [id + "{0:02X}".format(0) for id in e_base] + [id + "{0:02X}".format(1) for id in e_base] + [id + "{0:02X}".format(2) for id in e_base] + [id + "{0:02X}".format(3) for id in e_base] + [id + "{0:02X}".format(4) for id in e_base] + [id + "{0:02X}".format(5) for id in e_base] + [id + "{0:02X}".format(6) for id in e_base] + [id + "{0:02X}".format(7) for id in e_base] + [id + "{0:02X}".format(8) for id in e_base] + [id + "{0:02X}".format(9) for id in e_base] + [id + "{0:02X}".format(10) for id in e_base] + [id + "{0:02X}".format(11) for id in e_base] + [id + "{0:02X}".format(12) for id in e_base]


energy = []
for id in energy_id:
    energy += psend(":get-energy " + id)

# ������������
d_base = ["010100", "010200", "010500", "010600", "010700", "010800", "010900", "010A00"]
demand_id = [id + "{0:02X}".format(0) for id in d_base] + [id + "{0:02X}".format(0) for id in d_base] + [id + "{0:02X}".format(1) for id in d_base] + [id + "{0:02X}".format(2) for id in d_base] + [id + "{0:02X}".format(3) for id in d_base] + [id + "{0:02X}".format(4) for id in d_base] + [id + "{0:02X}".format(5) for id in d_base] + [id + "{0:02X}".format(6) for id in d_base] + [id + "{0:02X}".format(7) for id in d_base] + [id + "{0:02X}".format(8) for id in d_base] + [id + "{0:02X}".format(9) for id in d_base] + [id + "{0:02X}".format(10) for id in d_base] + [id + "{0:02X}".format(11) for id in d_base] + [id + "{0:02X}".format(12) for id in d_base]

demand = []
for id in demand_id:
    demand += psend(":get-demand " + id)

# �����Զ�ѭ������
auto_screen_id = ["040401" + "{0:02X}".format(i) for i in range(1, 64)]
auto_screen = []
for item in auto_screen_id:
    auto_screen += psend(":get-cycle-display " + item)

# ��������ѭ������
screen_id = ["040402" + "{0:02X}".format(i) for i in range(1, 64)]
screen = []
for item in screen_id:
    screen += psend(":get-cycle-display " + item)

# ѭ���ϵ��磬ÿ���ϵ�󳭶�һ��ͬ�����������״γ��������ݽ��бȽ�
# ��ͬ��ϸ񣬲�ͬ�����ʧ��
for times in range(20):
    # ������ʱ
    psend(":dut-set uoff")
    time.sleep(15)
    
    # �ϵ���ʱ
    psend(":dut-set uon")
    time.sleep(15)
    
    # ������������
    energy_new = []
    for id in energy_id:
        energy_new += psend(":get-energy " + id)

    # ������������
    demand_new = []
    for id in demand_id:
        demand_new += psend(":get-demand " + id)
        
    # �����Զ�ѭ������
    auto_screen_new = []
    for item in auto_screen_id:
        auto_screen_new += psend(":get-cycle-display " + item)

    # ��������ѭ������
    screen_new = []
    for item in screen_id:
        screen_new += psend(":get-cycle-display " + item)

    # ǰ������Ա�
    # ���ǰ����ڲ�һ�³���ᱨ��ִֹͣ��
    assert energy == energy_new
    assert demand == demand_new
    assert auto_screen == auto_screen_new
    assert screen == screen

    # ��ӡѭ�������������û�
    print("ѭ����%s��" % times)

print("�������...\n", "���Խ�����ϸ�\n")
