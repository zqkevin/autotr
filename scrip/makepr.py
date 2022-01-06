from scrip import wdglob, binance
import okex_http2.Market_api as Market
import numpy as np
import time
import log

marketAPI = Market.MarketAPI(api_key='', api_secret_key='', passphrase='', flag='0')


# 获取30日价格均价和24小时均价
def arp():
    x = 0
    while x < 5:
        try:
            request = marketAPI.get_candlesticks
            parameters = {'instId': 'ETH-USDT', 'bar': '1D', 'limit': 30}
            result = request(**parameters)
            days30 = result['data']
            arprday = round(np.average([float(a[4]) for a in days30]), 2)
            time.sleep(1)
            parameters = {'instId': 'ETH-USDT', 'bar': '1H', 'limit': 24}
            result = request(**parameters)
            h24 = result['data']
            arprh = round(np.average([float(a[4]) for a in h24]), 2)
            return arprday, arprh
        except:
            x = x + 1
            print('获取均线失败，重新连接！重试次数', x)
            time.sleep(5)
            continue
        pass
    return False


# 获取ETH和BTC的市场实时价格
def dticker():
    try:
        request = marketAPI.get_ticker
        x = 0
        while x < 3:
            parameters = 'ETH-USDT'
            result = request(parameters)
            if result['data'][0]:
                wdglob.ETHBODY = result['data'][0]
                time.sleep(0.5)
                parameters = 'BTC-USDT'
                result = request(parameters)
                if result['data'][0]:
                    wdglob.BTCBODY = result['data'][0]
                    return True
                else:
                    time.sleep(2)
                    x = x + 1
                    continue
            else:
                x = x + 1
                time.sleep(0.5)
        log.info('切换平台尝试获取')
        y = 0
        while y < 3:
            re = binance.getprice('ETHUSDT')
            if re:
                time.sleep(0.5)
                wdglob.ETHBODY['lsat'] = re.lastPrice
                wdglob.ETHBODY['lastSz'] = re.lastQty
                wdglob.ETHBODY['vol24h'] = re.volume
                rb = binance.getprice('BTCUSDT')
                if rb:
                    wdglob.BTCBODY['lsat'] = re.lastPrice
                    wdglob.BTCBODY['lastSz'] = re.lastQty
                    wdglob.BTCBODY['vol24h'] = re.volume
                    return True
                else:
                    time.sleep(0.5)
                    y = y + 1
                    continue
            else:
                time.sleep(0.5)
                y = y + 1
                continue
    except Exception as e:
        log.err('网络无法连接:%s'%e)
        return False



