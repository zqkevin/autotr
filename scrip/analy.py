import datetime
import time
import log
from scrip import database, wdglob, trade


def ethwave():
    try:
        while not wdglob.ETHBODY['ts']:
            time.sleep(1)
        p = wdglob.ETHBODY.copy()
        coun = 0
        x = 0
        y = 0
        while True:
            time.sleep(5)
            p2 = wdglob.ETHBODY.copy()
            priceb = float(p['p'])
            pricenow = float(p2['p'])
            con = round((pricenow - priceb)/pricenow, 4)
            if con >= wdglob.amp:
                database.recordanaly(p, p2, 'sell')
                if check(side='sell'):
                    coun = coun + 1
                    x = x+1
                    log.info('触发卖出交易，价格为：%s，总交易次数：%s次，卖出：%s次，买入：%s次。' % (pricenow, coun, x, y))
                    trade.runwave(side='sell')
                    p = p2.copy()
                continue
            elif con <= -wdglob.amp:
                database.recordanaly(p, p2, 'buy')
                if check(side='buy'):
                    coun = coun + 1
                    y = y + 1
                    log.info('触发买入交易，价格为：%s，总交易次数：%s次，卖出：%s次，买入：%s次。' % (pricenow, coun, x, y))
                    trade.runwave(side='buy')
                    p = p2.copy()
                continue
            else:
                continue
    except Exception as e:
        log.err('ethwave程序出错！', e)
        return False

def check(side):
    nowtime = datetime.datetime.now()
    a = database.lastanyle()
    if a :
        anyletime = a.atime
        anyleside = a.side
        if side == anyleside:
            timec = nowtime - anyletime
            if timec.seconds < 300:
                return False
            else:
                return True
        else:
            return True
    return True


