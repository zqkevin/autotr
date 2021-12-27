import time

# 产品类型
# MARGIN：币币杠杆
# SWAP：永续合约
# FUTURES：交割合约
# OPTION：期权

# 交易函数
def trade(tradeapi, parameters):
    x = 0
    while x < 3:
        try:
            while x < 3:
                request = tradeapi.place_order
                result = request(**parameters)
                scode = result['data'][0]['sCode']
                if scode == '0':
                    print('下单成功')
                    return result['data'][0]
                elif scode == '51008':
                    print('由于余额不足，下单失败')
                    return result['data'][0]
                else:
                    x = x + 1
                    print('下单失败，尝试重新下单！重试次数', x)
            return 0
        except:
            x = x + 1
            print('连接失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return False

# 查看订单信息
def get_ord(tradeapi, ordid, instid='ETH-USDT'):
    x = 0
    while x < 3:
        try:
            while x < 3:
                parameters = {'instId': instid, 'ordId': ordid}
                request = tradeapi.get_orders
                result = request(**parameters)
                scode = result['code']
                if scode == '0':
                    return result['data'][0]
                else:
                    x = x + 1
                    continue
        except:
            x = x + 1
            print('连接失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
    return False

# 查看杠杆信息
def get_lever(accountapi, instid='ETH-USDT', mgnmode='cross'):
    x = 0
    parameters = {"instId": instid, "mgnMode": mgnmode}
    while x < 3:
        try:
            request = accountapi.get_leverage
            result = request(**parameters)
            if result['data']:
                return result['data'][0]['lever']
            else:
                return 0
        except:
            x = x + 1
            print('获取杠杆信息失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return False
# 查看持仓信息  Get Positions
def get_pos(accountapi, insttype='MARGIN', instid='ETH-USDT'):
    x = 0
    parameters = {"instType": insttype, "instId": instid}
    while x < 3:
        try:
            request = accountapi.get_positions
            result = request(**parameters)
            if result['data']:
                return result['data'][0]
            else:
                return None
        except:
            x = x + 1
            print('获取持仓信息失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return False

# 调整账户杠杆
def setlever(accountapi, lever, instid='ETH-USDT', mgnmode='cross'):
    x = 0
    while x < 5:
        try:
            request = accountapi.set_leverage
            parameters = {'instId': instid, 'lever': lever, 'mgnMode': mgnmode}
            result = request(parameters)
            if result['data'][0]['lever'] == lever:
                return 5
            else:
                return 0
        except:
            x = x + 1
            print('调整杠杆失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return 0



# 查看账户资金信息
def get_balance(accountapi, parameters='USDT'):

    x = 0
    while x < 5:
        try:
            request = accountapi.get_account
            result = request(parameters)
            if result['data'][0]['details']:
                return result['data'][0]['details'][0]
            else:
                return 0
        except:
            x = x + 1
            print('获取账户资金失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return False

