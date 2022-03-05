from scrip import wdglob, binance
import numpy as np
import time, json, websockets, asyncio
import log




# 获取30日价格均价和24小时均价
def arp():
    try:
        days30  = binance.getstick(symbol='ETHUSDT', interval="1d", starttime=None, endtime=None, limit=30)
        arprday = round(np.average([a.close for a in days30]), 2)
        h24 = binance.getstick(symbol='ETHUSDT', interval="1h", starttime=None, endtime=None, limit=24)
        arprh = round(np.average([a.close for a in h24]), 2)
        return arprday, arprh
    except Exception as e:
        log.err('获取均线失败,错误：%s' % e)
        return False


# 获取websocket方式获取biance平台市场实时价格
def webbian():
    async def bian_connect():
        try:
            url = "wss://fstream.binance.com/ws"
            count = 1
            while count < 4:
                async with websockets.connect(url) as ws:
                    trade_param = {"method": "SUBSCRIBE", "params": ["btcusdt@ticker", "ethusdt@ticker"], "id": count}
                    sub_str = json.dumps(trade_param)
                    await ws.send(sub_str)
                    r = await ws.recv()
                    log.info('价格服务器第 %s 次连接,服务器返回：%s' % (count, r))
                    count = 1
                    while True:
                        try:
                            res = await asyncio.wait_for(ws.recv(), timeout=25)
                            if 'result' in res:
                                continue
                            re = eval(res)

                            if re['s'] == 'ETHUSDT':
                                wdglob.ETHBODY['ts'] = re['E']  #时间
                                wdglob.ETHBODY['p'] = re['c']   #市场价
                                wdglob.ETHBODY['pc'] = re['p']  #24小时变动
                                wdglob.ETHBODY['pcp'] = re['P'] #24小时变动百分比
                                wdglob.ETHBODY['hp'] = re['h']  #24小时最高价
                                wdglob.ETHBODY['lp'] = re['l']  #24小时最低价
                                wdglob.ETHBODY['24hv'] = re['v']#24小时成交量
                            elif re['s'] == 'BTCUSDT':
                                wdglob.BTCBODY['ts'] = re['E']
                                wdglob.BTCBODY['p'] = re['c']
                                wdglob.BTCBODY['pc'] = re['p']
                                wdglob.BTCBODY['pcp'] = re['P']
                                wdglob.BTCBODY['hp'] = re['h']
                                wdglob.BTCBODY['lp'] = re['l']
                                wdglob.BTCBODY['24hv'] = re['v']
                            else:
                                continue
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res = await ws.recv()
                                print(res)
                                continue
                            except Exception as e:
                                log.err("连接关闭，正在重连……%s" % e)
                                count = count + 1
                                break
        except Exception as e:
            log.err(e)
            return False
    asyncio.run(bian_connect())
    return False

def webok():

    url = "wss://ws.okex.com:8443/ws/v5/public"
    channels = [{"channel": "mark-price", "instId": "BTC-USDT"}]
    #
    # loop.run_until_complete(subscribe_without_login(url, channels))
    #
    #
    # loop.close()
    return False
# request获取okex平台ETH和BTC的市场实时价格




