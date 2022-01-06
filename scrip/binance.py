from scrip import database
from scrip.models import User, Ethusdt1m
from binance_f import RequestClient
from datetime import datetime
import time, log, pytz




def getprice(symbol='ETHUSDT'):
    try:
        request_client = RequestClient(api_key='', secret_key='')
        result = request_client.get_ticker_price_change_statistics(symbol=symbol)
        if result:
            return result[0]
        else:
            return False
    except Exception as e:
        return e

def getpostion(request_client, symbol='ETHUSDT'):
    # request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_position(symbol=symbol)
    time.sleep(0.5)
    return result


def getacc(request_client):

    try:
        x = 0
        while x < 3:
            result = request_client.get_balance()
            if result:
                for a in result:
                    if a.asset == 'USDT':
                        acc_ky = round(a.withdrawAvailable,2)
                        acc_zs = round(a.balance, 2)
                        acc_zy = acc_zs - acc_ky
                        result = request_client.get_position_v2(symbol='ETHUSDT')[0]
                        if result:
                            pos_ccl = round(abs(result.positionAmt), 4)
                            pos_ccj = round(result.entryPrice, 2)
                            if result.positionAmt >= 0:
                                pos_side = 0  # 多头
                            else:
                                pos_side = 1  # 空头
                            pos_wsxl = round(result.unrealizedProfit, 2)
                            lever = int(result.leverage)
                            re = {
                                'lever': lever,  # 杠杆
                                'acc_ky': acc_ky,  # 可用余额
                                'acc_zs': acc_zs,  # 总金额
                                'acc_zy': acc_zy,  # 持仓占用金额
                                'acc_wsx': pos_wsxl,  # 未实现盈利
                                'pos_ccl': pos_ccl,  # 持仓量多头为ETH，多头为USDT
                                'pos_side': pos_side,  # 当前持仓方向 0 为多头 1 为空头
                                'pos_ccj': pos_ccj,  # 持仓价
                                'pos_wsxl': pos_wsxl  # 未实现盈利
                            }
                            return re
                    else:
                        continue
                log.acc('账户无USDT')
                return False
            else:
                x = x + 1
                continue
        log.err('bianace查询账户失败')
        return False
    except Exception as e:
        log.err(e)
        return False

# 交易
def trade(request_client, quantity, price, side, symbol="ETHUSDT", ordertype="LIMIT", timeInForce="GTC"):
    try:
        x = 0
        while x < 3:
            result = request_client.post_order(symbol=symbol, side=side, ordertype=ordertype, quantity=quantity,
                                               price=price, timeInForce=timeInForce)
            if result:
                log.info('bianace下单成功')
                return result
            else:
                x = x + 1
                time.sleep(0.5)
                log.info('下单失败，尝试重新下单！重试次数 %s'%x)
        return False
    except Exception as e:
        log.err(e)
        return False


def getorder(request_client):
    result = request_client.get_open_orders()
    rt = []
    for r in result:
        r.updateTime = datetime.fromtimestamp(int(r.updateTime / 1000))
        rt.append(r)
    time.sleep(0.5)
    return rt

def getordered(request_client, ordid, symbol='ETHUSDT'):
    x = 0
    while x < 3:
        try:
            result = request_client.get_order(symbol=symbol, orderId=ordid)
            #result.time = datetime.fromtimestamp(int(result.time / 1000))
            result.updateTime = datetime.fromtimestamp(int(result.updateTime / 1000))
            re = {'ordertime':result.updateTime,
                  'orderid':str(result.orderId),
                  'side': result.side,
                  'avgprice':result.avgPrice,
                  'origqty':result.executedQty,
                  'status': result.status,
                  'fig':0}
            return re
        except Exception as e:
            time.sleep(2)
            x = x + 1
            ex = e
    log.err('确认bianace订单失败,订单号：%s，报错信息：%s'%(ordid, ex))
    return False

def getstick(symbol='ETHUSDT', interval="1m", starttime=None, endtime=None, limit=30):

    if isinstance(starttime,str):
        starttime = datetime.strptime(starttime,'%Y-%m-%dT%H:%M')
        starttime = int(starttime.timestamp()*1000)

    if isinstance(endtime,str):
        endtime = datetime.strptime(endtime,'%Y-%m-%dT%H:%M')
        endtime = int(endtime.timestamp()*1000)

    request_client = RequestClient(api_key='', secret_key='')
    result = request_client.get_candlestick_data(symbol=symbol, interval=interval, startTime=starttime, endTime=endtime,
                                                 limit=limit)
    #PrintMix.print_data(result)
    rt = []
    for r in result:
        r.openTime = datetime.fromtimestamp(int(r.openTime / 1000))
        r.closeTime = datetime.fromtimestamp(int(r.closeTime / 1000))
        r.close = float(r.close)
        r.high = float(r.high)
        r.low = float(r.low)
        r.open = float(r.open)
        r.quoteAssetVolume = float(r.quoteAssetVolume)
        r.takerBuyBaseAssetVolume = float(r.takerBuyBaseAssetVolume)
        r.takerBuyQuoteAssetVolume = float(r.takerBuyQuoteAssetVolume)
        a = (r.close - r.open)
        if a != 0:
            a = abs(a)/a
        r.zhenfu = round((r.high - r.low)/r.close*100*a, 2)
        rt.append(r)
    # print("======= Kline/Candlestick Data =======")
    # PrintMix.print_data(rt)
    # print("======================================")
    time.sleep(0.5)
    return rt



def geteth1m():
    try:
        last = database.get_eth1m_lasttime()
        a = 0
        if not last:
            #endtime = int(now.timestamp() * 1000)
            res = getstick(limit=10)
            last = database.pos_save1m(res)
        last = database.get_eth1m_lasttime()
        now = datetime.now()
        while (now - last).seconds > 60 or (now - last).days > 0:
            starttime = int(last.timestamp()*1000) + 1
            starttime = last
            endtime = int(now.timestamp()*1000)
            res = getstick(starttime=starttime, endtime=endtime, limit=100)
            coun = len(res)
            starstr = last
            #last = database.pos_save1m(res)
            last = database.get_eth1m_lasttime()
            now = datetime.now()
            endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
            starstr = datetime.strftime(starstr, '%Y-%m-%d %H:%M:%S')
            log.info('分钟K线增加时间从：%s 到 %s, 共 %d 条' % (starstr, endstr, coun))
            a = a+coun
        endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
        log.info('最新数据记录是：%s 本次共更新 %d 条数据' % (endstr, a))
        return True
    except Exception as e:
        log.err(e)
        return False


