import okex_http2.Trade_api as Trade
import okex_http2.Account_api as Account
from scrip import database as db
from scrip import okcommand, wdglob
import time


def accinfo(accountapi):
    blanace = okcommand.get_balance(accountapi=accountapi)
    if blanace:
        acc_ky = round(float(blanace['availBal']+blanace['availEq']), 2)
        acc_zs = round(float(blanace['cashBal']), 2)
        acc_zy = round(float(blanace['frozenBal']), 2)
        acc_wsx = blanace['upl']
        lever = int(okcommand.get_lever(accountapi))
        if lever > 5:
            # print('杠杆只能小于5,大于5自动设为5')
            # lever = okcommand.setlever(accountapi,lever='5')
            lever = 5
        position = okcommand.get_pos(accountapi)
        if position:
            pos_ccl = round(float(position['pos']), 4)
            pos_ccj = round(float(position['avgPx']), 2)
            if position['posCcy'] == 'ETH':
                pos_side = 0  # 多头
            else:
                pos_side = 1  # 空头
            pos_wsxl = round(float(position['uplRatio']), 4)

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
        print('无资金USDT')
        return False

def orderecord(tradelist):
    for a in tradelist:
        try:
            print('jinrurecord')
            record = okcommand.get_ord(tradeapi=a['tradeapi'], ordid=a['ordid'])
            db.recordorder(a['userid'], record)
            print('endorder')
        except:
            print('ordererr')
            continue

def wavetrade(side):

    userlist = db.finduser(flag=1)
    tradelist = []
    if userlist:
        for a in userlist:
            userid = a.id
            api_key = a.pt_api_key
            secret_key = a.pt_secret_key
            passphrase = a.pt_passphrase
            accountapi = Account.AccountAPI(api_key, secret_key, passphrase, False, flag='0')
            tradeapi = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag='0')
            acc = accinfo(accountapi)
            if not acc:
                continue
            p = float(wdglob.ETHBODY['last'])
            sz = round(acc['acc_zs'] * acc['lever'] / a.share, 4)
            if sz < 10:
                print('总金额不足')
                continue
            if side == 'buy':
                if sz > acc['acc_ky'] * acc['lever']:
                    continue
            else:
                sz = round(sz / p, 4)
            print( '进入交易: ','user=', a.name, 'side=', side, '数量：', sz, '价格：', wdglob.ETHBODY['last'])
            parameters = {'side': side, 'sz': sz, 'ccy': 'USDT', 'px': '', 'instId': 'ETH-USDT', 'ordType': 'market',
                          'tdMode': 'cross'}
            order = okcommand.trade(tradeapi, parameters)
            if order:
                dic = {'userid': userid, 'ordid': order['ordId'], 'tradeapi': tradeapi}
                tradelist.append(dic)
            else:
                continue

        if tradelist:
            orderecord(tradelist)
    else:
        print('无用户采用wave')
        return '无用户采用wave'

