# SBJ-X15010 ≥≠∂¡ £”‡µÁ¡ø00900100

psend("68 62 48 62 48 62 48 68 11 04 33 34 C3 33 40 16")

remain_power = meter.minus33H(meter.CMD.response()[14:-2][::-1])
print("%s%s%s.%s" % (remain_power[0], remain_power[1], remain_power[2], remain_power[3]))
