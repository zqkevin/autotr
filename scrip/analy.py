import log
from scrip import database, wdglob


def wave(p):
    try:
        priceb = float(p['last'])
        pricenow = float(wdglob.ETHBODY['last'])
        con = round((pricenow - priceb)/pricenow, 4)
        if con >= wdglob.amp:
            database.recordanaly(p, 'sell')  # 记录触发数据
            return 1 #做空头sell
        elif con <= -wdglob.amp:
            database.recordanaly(p, 'buy')
            return 0  # 做多头buy
        else:
            return 'pass'
    except Exception as e:
        log.err(e)
        pass

