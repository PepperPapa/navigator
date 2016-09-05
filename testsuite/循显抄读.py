# ×Ô¶¯Ñ­ÏÔ1¡«24ÆÁ³­¶Á
auto_cycle = ["040401" + "{0:02X}".format(i) for i in range(1, 25)]
for item in auto_cycle:
  psend(":get-cycle-display " + item)

# °´¼üÑ­ÏÔ1¡«24ÆÁ³­¶Á
manual_cycle = ["040402" + "{0:02X}".format(i) for i in range(1, 25)]
for item in manual_cycle:
  psend(":get-cycle-display " + item)
