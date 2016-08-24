# 
# 标题： 不加电流，反复上掉电验证电量、需量、循显、键显参数无变化
#
import time

# 表计加电压
psend(":dut-set uon")
time.sleep(15)

# 首先抄读一次需要比较的数据
# 抄读电量数据
e_base = ["000000", "000100", "000200", "000500", "000600", "000700", "000800", "000900", "000A00"]
energy_id = [id + "{0:02X}".format(0) for id in e_base] + [id + "{0:02X}".format(0) for id in e_base] + [id + "{0:02X}".format(1) for id in e_base] + [id + "{0:02X}".format(2) for id in e_base] + [id + "{0:02X}".format(3) for id in e_base] + [id + "{0:02X}".format(4) for id in e_base] + [id + "{0:02X}".format(5) for id in e_base] + [id + "{0:02X}".format(6) for id in e_base] + [id + "{0:02X}".format(7) for id in e_base] + [id + "{0:02X}".format(8) for id in e_base] + [id + "{0:02X}".format(9) for id in e_base] + [id + "{0:02X}".format(10) for id in e_base] + [id + "{0:02X}".format(11) for id in e_base] + [id + "{0:02X}".format(12) for id in e_base]


energy = []
for id in energy_id:
    energy += psend(":get-energy " + id)

# 抄读需量数据
d_base = ["010100", "010200", "010500", "010600", "010700", "010800", "010900", "010A00"]
demand_id = [id + "{0:02X}".format(0) for id in d_base] + [id + "{0:02X}".format(0) for id in d_base] + [id + "{0:02X}".format(1) for id in d_base] + [id + "{0:02X}".format(2) for id in d_base] + [id + "{0:02X}".format(3) for id in d_base] + [id + "{0:02X}".format(4) for id in d_base] + [id + "{0:02X}".format(5) for id in d_base] + [id + "{0:02X}".format(6) for id in d_base] + [id + "{0:02X}".format(7) for id in d_base] + [id + "{0:02X}".format(8) for id in d_base] + [id + "{0:02X}".format(9) for id in d_base] + [id + "{0:02X}".format(10) for id in d_base] + [id + "{0:02X}".format(11) for id in d_base] + [id + "{0:02X}".format(12) for id in d_base]

demand = []
for id in demand_id:
    demand += psend(":get-demand " + id)

# 抄读自动循显数据
auto_screen_id = ["040401" + "{0:02X}".format(i) for i in range(1, 64)]
auto_screen = []
for item in auto_screen_id:
    auto_screen += psend(":get-cycle-display " + item)

# 抄读按键循显数据
screen_id = ["040402" + "{0:02X}".format(i) for i in range(1, 64)]
screen = []
for item in screen_id:
    screen += psend(":get-cycle-display " + item)

# 循环上掉电，每次上电后抄读一次同样的数据与首次抄读的数据进行比较
# 相同则合格，不同则测试失败
for times in range(20):
    # 掉电延时
    psend(":dut-set uoff")
    time.sleep(15)
    
    # 上电延时
    psend(":dut-set uon")
    time.sleep(15)
    
    # 抄读电量数据
    energy_new = []
    for id in energy_id:
        energy_new += psend(":get-energy " + id)

    # 抄读需量数据
    demand_new = []
    for id in demand_id:
        demand_new += psend(":get-demand " + id)
        
    # 抄读自动循显数据
    auto_screen_new = []
    for item in auto_screen_id:
        auto_screen_new += psend(":get-cycle-display " + item)

    # 抄读按键循显数据
    screen_new = []
    for item in screen_id:
        screen_new += psend(":get-cycle-display " + item)

    # 前后参数对比
    # 如果前后存在不一致程序会报错停止执行
    assert energy == energy_new
    assert demand == demand_new
    assert auto_screen == auto_screen_new
    assert screen == screen

    # 打印循环次数以提醒用户
    print("循环了%s次" % times)

print("测试完成...\n", "测试结果：合格！\n")
