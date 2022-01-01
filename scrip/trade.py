import okex_http2.Trade_api as Trade
import okex_http2.Account_api as Account
from binance_f import RequestClient
from scrip import database as db
from scrip import okex, wdglob, binance
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
        global exitFlag
        orderecord(self.orderlist)


#(userid, ordered, amount):
# order = models.Orders(userid=userid, ordertime=ordertime, orderid=ordered['ordId'], side=ordered['side'],
#                          avgprice=ordered['avgPx'],  origqty=round(float(ordered['accFillSz']), 4), status=ordered['state'],
#                           fig=ordered['pnl'], amount=amount)

def orderecord(tradelist):
    for a in tradelist:
        try:
            if a['pt'] == 'okex':
                pt = 1
                record = okex.get_ord(tradeapi=a['tradeapi'], ordid=a['ordid'])
                db.recordorder(userid=a['userid'], ordertime=record['fillTime'], orderid=record['ordId'],
                               side=record['side'], avgprice=round(float(record['avgPx']), 2), origqty=round(float(record['accFillSz']), 4),
                               status=record['state'], fig=round(float(record['pnl']), 2), amount=a['amount'], pt=pt)
            elif a['pt'] == 'bianace':
                pt = 2
                record = binance.getordered(request_client=a['tradeapi'], ordid=a['ordid'])

                db.recordorder(userid=a['userid'], ordertime=record.updateTime, orderid=str(record.orderId),
                               side=record.side, avgprice=record.avgPrice, origqty=record.origQty, status=record.status,
                               fig=0, amount=a['amount'], pt=pt)
            continue
        except Exception as e:
            log.err(e)
            continue

def oktrade(acc,side,tradeapi,share,user=''):
    try:
        p = float(wdglob.ETHBODY['last'])
        sz = round(acc['acc_zs'] * acc['lever'] / share, 4)

        if side == 'buy':
            if sz > acc['acc_ky'] * acc['lever'] or sz < 10:
                log.acc('%s账户可用金额不足,暂停交易'%user)
                return False
        else:
            sz = round(sz / p, 4)
        log.info( '进入交易:  %s %s %sETH 价格：%s'%(user, side, sz, wdglob.ETHBODY['last']))
        parameters = {'side': side, 'sz': sz, 'ccy': 'USDT', 'px': '', 'instId': 'ETH-USDT', 'ordType': 'market',
                      'tdMode': 'cross'}
        order = okex.trade(tradeapi, parameters)
        if order:
            log.info('okex下单成功！')
            return order['ordId']
        else:
            return False
    except:
        return False

def biantrade(acc, side, request_client, share, name=''):
    try:
        p = float(wdglob.ETHBODY['last'])
        sz = round(acc['acc_zs'] * acc['lever'] / share, 4)

        if sz > acc['acc_ky'] * acc['lever'] or sz < 10:
                return False
        sz = round(sz / p, 3)
        if side == 'sell':
            side = 'SELL'
        else:
            side = 'BUY'
        print( '进入交易: ','user=', name, 'side=', side, '数量：', sz, '价格：', wdglob.ETHBODY['last'])
        order = binance.trade(request_client, ordertype='MARKET', price=None, side=side, quantity=sz, timeInForce=None)
        if order:
            return order.orderId
        else:
            return False
    except Exception as e:
        print(e)
        return False

def runwave(side):
    userlist = db.finduser(flag=1)
    if not userlist:
        log.info('无用户采用wave')
        return
    orderlist = []
    for a in userlist:
        userid = a.id
        api_key = a.pt_api_key
        secret_key = a.pt_secret_key
        passphrase = a.pt_passphrase
        share = a.share
        name = a.name
        pt = a.pt_name
        if pt == 'okex':
            accountapi = Account.AccountAPI(api_key, secret_key, passphrase, False, flag='0')
            tradeapi = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag='0')
            # 获取账户信息
            acc = okex.get_balance(accountapi)
            if not acc:
                log.info('账户信息错误')
                continue
            # 进行交易
            ordid = oktrade(acc, side, tradeapi, share, name)

            if ordid:
                odic = {'userid': userid, 'ordid': ordid, 'tradeapi': tradeapi, 'amount': acc['acc_zs'], 'pt': pt}
                orderlist.append(odic)
            else:
                continue
        elif pt == 'bianace':
            request_client = RequestClient(api_key=api_key, secret_key=secret_key)
            # 获取账户信息
            acc = binance.getacc(request_client)
            # 进行交易
            ordid = biantrade(acc, side, request_client, share, name)
            if ordid:
                odic = {'userid': userid, 'ordid': ordid, 'tradeapi': request_client, 'amount': acc['acc_zs'], 'pt': pt}
                orderlist.append(odic)
            else:
                continue
        else:
            continue

    threadrecord = Threadrecord(1, 'record', orderlist)
    threadrecord.start()

    return


