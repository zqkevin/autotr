import time, log
import okex_http2.Public_api as Public
from datetime import datetime
# 产品类型
# MARGIN：币币杠杆
# SWAP：永续合约
# FUTURES：交割合约
# OPTION：期权
# 交易函数

def get_server_time():
    publicAPI = Public.PublicAPI(api_key='', api_secret_key='', passphrase='')
    request = publicAPI.get_system_time()
    if request:
        re = request['data'][0]['ts']
        return re
    return False

#获取交易产品基本信息 insttyp:
# SPOT：币币
# MARGIN：币币杠杆
# SWAP：永续合约
# FUTURES：交割合约
# OPTION：期权
def get_instruments(insttype='SWAP',instid='ETH-USDT'):
    try:
        publicAPI = Public.PublicAPI(api_key='', api_secret_key='', passphrase='')
        request = publicAPI.get_instruments(instType=insttype, uly=instid)
        if request['code'] == '0':
            return request['data'][0]
    except:
        return False

#交易下单函数
def trade(tradeapi, parameters):
    try:
        x = 0
        while x < 3:
            result = tradeapi.place_order(**parameters)
            if result:
                scode = result['data'][0]['sCode']
                if scode == '0':
                    return result['data'][0]
                elif scode == '51010':
                    log.acc('账户未开通杠杆模式')
                    return False
                else:
                    x = x + 1
                    log.info('下单失败，尝试重新下单！重试次数 %s'%x)
                    time.sleep(0.5)
                    continue
        if result['data'][0]['sMsg']:
            log.acc(result['data'][0]['sMsg'])
        return False
    except Exception as e:
        log.err(e)
        return False

# 查看订单信息
def get_ord(tradeapi, ordid, instid='ETH-USDT'):
    x = 0
    try:
        while x < 3:
            parameters = {'instId': instid, 'ordId': ordid}
            request = tradeapi.get_orders
            result = request(**parameters)
            scode = result['code']
            if scode == '0':
                b = result['data'][0]
                a = b['fillTime']
                a = int(a[0:10])
                ordertime = datetime.fromtimestamp(a)
                b['fillTime'] = ordertime
                re = {'ordertime': b['fillTime'],
                      'orderid': b['ordId'],
                      'side': b['side'],
                      'avgprice': round(float(b['avgPx']),2),
                      'origqty': round(float(b['accFillSz']),4),
                      'status': b['state'],
                      'fig': round(float(b['pnl']),2)
                      }
                return re
            else:
                x = x + 1
                continue
    except Exception as e:
        log.err('查订单失败：%s'%e)
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



# 查看账户资金以及持仓信息
def get_balance(accountapi, parameters='USDT'):
    x = 0
    while x < 5:
        try:
            result = accountapi.get_account(parameters)
            if result['data'][0]['details']:
                blanace = result['data'][0]['details'][0]
                if blanace:
                    if blanace['availBal'] + blanace['availEq']:
                        acc_ky = round(float(blanace['availBal'] + blanace['availEq']), 2)
                    else: acc_ky = 0
                    if blanace['eq']:
                        acc_zs = round(float(blanace['eq']), 2)
                    else: acc_zs = 0
                    acc_zs = round(float(blanace['eq']), 2)
                    if blanace['frozenBal']:
                        acc_zy = round(float(blanace['frozenBal']), 2)
                    else: acc_zy = 0
                    if blanace['upl']:
                        acc_wsx = blanace['upl']
                    else: acc_wsx = 0
                    lever = int(get_lever(accountapi))
                    if lever > 5:
                        # print('杠杆只能小于5,大于5自动设为5')
                        # lever = okex.setlever(accountapi,lever='5')
                        lever = 5
                    position = get_pos(accountapi)
                    if position:
                        if position['pos']:
                            pos_ccl = round(float(position['pos']), 4)
                        else: pos_ccl = 0
                        if position['avgPx']:
                            pos_ccj = round(float(position['avgPx']), 2)
                        else: pos_ccj = 0
                        if position['posCcy'] == 'ETH':
                            pos_side = 0  # 多头
                        else:
                            pos_side = 1  # 空头
                        if position['uplRatio']:
                            pos_wsxl = round(float(position['uplRatio']), 4)
                        else: pos_wsxl = 0
                        re = {
                            'lever': lever,  # 杠杆
                            'acc_ky': acc_ky,  # 可用余额
                            'acc_zs': acc_zs,  # 总金额
                            'acc_zy': acc_zy,  # 持仓占用金额
                            'acc_wsx': acc_wsx,  # 未实现盈利
                            'pos_ccl': pos_ccl,  # 持仓量多头为ETH，多头为USDT
                            'pos_side': pos_side,  # 当前持仓方向 0 为多头 1 为空头
                            'pos_ccj': pos_ccj,  # 持仓价
                            'pos_wsxl': pos_wsxl  # 未实现盈利
                        }
                        return re
                    else:
                        pos_ccl = 0
                        pos_ccj = 0
                        pos_side = 0
                        pos_wsxl = 0
                        re = {
                            'lever': lever,  # 杠杆
                            'acc_ky': acc_ky,  # 可用余额
                            'acc_zs': acc_zs,  # 总金额
                            'acc_zy': acc_zy,  # 持仓占用金额
                            'acc_wsx': acc_wsx,  # 未实现盈利
                            'pos_ccl': pos_ccl,  # 持仓量多头为ETH，多头为USDT
                            'pos_side': pos_side,  # 当前持仓方向 0 为多头 1 为空头
                            'pos_ccj': pos_ccj,  # 持仓价
                            'pos_wsxl': pos_wsxl  # 未实现盈利
                        }
                        return re
                else:
                    log.acc('账户无资金USDT')
                    return False

            else:
                return False
        except Exception as e:
            x = x + 1
            print('获取账户资金失败，重新连接！重试次数', x,'错误为:',e)
            time.sleep(5)
            continue
        pass
    return False


