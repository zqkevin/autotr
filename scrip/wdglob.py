# 市场价参数说明：
# p:市场价，pc:价格变动量， pcp:价格变动百分比，hp：最高价 lp：最低价 24hv:24小时成交量 ts是int 13,其他str
ETHBODY = {'ts': 0, 'p': '0', 'pc': '0', 'pcp': '0', 'hp': '0', 'lp': '0', '24hv': '0'}
BTCBODY = {'ts': 0, 'p': '0', 'pc': '0', 'pcp': '0', 'hp': '0', 'lp': '0', '24hv': '0'}
lastanaly = {}
arprd = 0  # 30天均线价格
arprh = 0  # 24小时均价
amp = 0.003  # 判断基数
check = 0   # 校准参数
binanceserver = 1   # 平台状态
okexserver = 1  # 平台状态
