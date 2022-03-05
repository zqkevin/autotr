import time
import okex_http2.Trade_api as Trade
import okex_http2.Account_api as Account
from scrip.binance_f import RequestClient
from scrip import database as db
from scrip import okex, wdglob, binance, accangly, bf
import log
import threading
thread = 1
class Threadrecord(threading.Thread):
    def __init__(self, threadID, name, orderlist) :
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.orderlist = orderlist
    def run(self):
        orderecord(self.orderlist)


#(userid, ordered, amount):
# order = models.Orders(userid=userid, ordertime=ordertime, orderid=ordered['ordId'], side=ordered['side'],
#                          avgprice=ordered['avgPx'],  origqty=round(float(ordered['accFillSz']), 4), status=ordered['state'],
#                           fig=ordered['pnl'], amount=amount)

def orderecord(tradelist):
    p = float(wdglob.ETHBODY['p'])
    for a in tradelist:
        try:
            if a['pt'] == 'okex':
                pt = 1
                record = okex.get_ord(tradeapi=a['tradeapi'], ordid=a['ordid'])
            elif a['pt'] == 'bianace':
                pt = 2
                record = binance.getordered(request_client=a['tradeapi'], ordid=a['ordid'])
                sz = record['origqty']
                fig = db.upuser_status(userid=a['userid'], p=record['avgprice'], sz=sz, side=record['side'], acc=a['acc'])
            elif a['pt'] == 'bf':
                pt = 3
                record = a['record']
                fig = db.upuser_status(userid=a['userid'], p=record['avgprice'], sz=record['origqty'], side=record['side'],acc=a['acc'])

            rt = {'userid': a['userid'],
                  'ordertime': record['ordertime'],
                  'orderid': record['orderid'],
                  'side': record['side'],
                  'avgprice': record['avgprice'],
                  'origqty': record['origqty'],
                  'status': record['status'],
                  'fig': fig,
                  'lever': a['acc']['lever'],
                  'pt': pt,
                  'acc_ky': a['acc']['acc_ky'],
                  'acc_zy': a['acc']['acc_zy'],
                  'amount': a['acc']['acc_zs'],
                  'acc_wsx': a['acc']['acc_wsx'],
                  'pos_ccl': a['acc']['pos_ccl'],
                  'pos_ccj': a['acc']['pos_ccj'],
                  'pos_side': a['acc']['pos_side']
                  }
            db.recordorder(rt)
            continue
        except Exception as e:
            log.err(e)
            continue

def oktrade(sz, side, tradeapi):
    try:
        p = float(wdglob.ETHBODY['p'])
        if side == 'buy':
            parameters = {'side': side, 'sz': sz, 'ccy': 'USDT', 'px': '', 'instId': 'ETH-USDT', 'ordType': 'market',
                          'tdMode': 'cross'}
        else:
            sz = round(sz / p, 4)

            parameters = {'side': side, 'sz': sz, 'ccy': 'USDT', 'px': '', 'instId': 'ETH-USDT', 'ordType': 'market',
                          'tdMode': 'cross'}
        order = okex.trade(tradeapi, parameters)
        if order:
            log.info('okex下单成功！')
            return order['ordId']
        else:
            log.info('okex下单失败%s'%order)
            return False
    except Exception as e:
        log.err('okex下单失败%s'%e)
        return False

def biantrade(sz, side, request_client):
    try:
        p = float(wdglob.ETHBODY['p'])
        sz = round(sz / p, 3)
        if side == 'sell':
            side = 'SELL'
        else:
            side = 'BUY'
        order = binance.trade(request_client, ordertype='MARKET', price=None, side=side, quantity=sz, timeInForce=None)
        if order:
            return order.orderId
        else:
            log.info('binance下单失败%s' % order)
            return False
    except Exception as e:
        log.err('bianace下单失败%s'%e)
        return False

def runwave(side):
    userlist = db.finduser(flag=1)
    if not userlist:
        log.info('无用户采用wave')
        return
    orderlist = []
    for a in userlist:
        userid = a.userid
        api_key = a.pt_api_key
        secret_key = a.pt_secret_key
        passphrase = a.pt_passphrase
        pt = a.pt_name
        if pt == 'okex':
            accountapi = Account.AccountAPI(api_key, secret_key, passphrase, False, flag='0')
            tradeapi = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag='0')
            # 获取账户信息
            acc = okex.get_balance(accountapi)
            if not acc:
                log.info('账户信息错误')
                continue
            jysz = accangly.wavesz(acc, a, side)
            if jysz:
                # 进行交易
                ordid = oktrade(sz=jysz, side=side, tradeapi=tradeapi)
                if ordid:
                    odic = {'userid': userid, 'ordid': ordid, 'tradeapi': tradeapi, 'acc': acc, 'pt': pt}
                    orderlist.append(odic)
                else:
                    continue
            else:
                continue
        elif pt == 'bianace':
            request_client = RequestClient(api_key=api_key, secret_key=secret_key)
            # 获取账户信息
            acc = binance.getacc(request_client)
            if not acc:
                log.err('账户信息错误')
                continue
            # 进行交易
            jysz = accangly.wavesz(acc, a, side)
            if jysz:
                ordid = biantrade(sz=jysz, side=side, request_client=request_client)
                if ordid:
                    odic = {'userid': userid, 'ordid': ordid, 'tradeapi': request_client, 'acc': acc, 'pt': pt}
                    orderlist.append(odic)
                else:
                    continue
            else:
                continue
        elif pt == 'bf':
            acc = bf.getacc(userid)
            jysz = accangly.wavesz(acc, a, side)
            log.info('进入bf交易，jysz = %s' % jysz)
            record = bf.greatord(userid, jysz, side)
            ordid = record['orderid']
            odic = {'userid': userid, 'ordid': ordid, 'tradeapi': None, 'acc': acc, 'pt': pt, 'record': record}
            orderlist.append(odic)
        else:
            continue

    threadrecord = Threadrecord(1, 'record', orderlist)
    threadrecord.start()

    return


