# 帧头
FSB = '7B'
# 地址
ADB = '01'

# 帧尾
FEB = '7D'
# 结束符
END = '0D 0A'

# read position
POSITION = '7B 01 13 7D 0D 0A 23'
# stop move
STOP = '7B 01 47 7D 0D 0A 57'
# 单轴顺时针转动
ROT_C = ''
# 单轴逆时针转动
ROT_AC = ''

# 驱动上电
INSERT_POWER = '7B 01 41 7D 0D 0A 51'

# 驱动断电
DROP_POWER = '7B 01 40 7D 0D 0A 50'
