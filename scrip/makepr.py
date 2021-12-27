from scrip import wdglob
import okex_http2.Market_api as Market
import numpy as np
import time

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
    request = marketAPI.get_ticker
    x = 0
    while x < 10:
        try:
            parameters = 'ETH-USDT'
            result = request(parameters)
            boby = result['data'][0]
            #print('ETH:',boby['last'])
            wdglob.ETHBODY = boby
            time.sleep(1)
            parameters = 'BTC-USDT'
            result = request(parameters)
            boby = result['data'][0]
            #print('BTC:',boby['last'])
            wdglob.BTCBODY = boby
            return boby
        except:
            x = x + 1
            print('timeout,retry ', x)
            time.sleep(2)
            continue
    return False



