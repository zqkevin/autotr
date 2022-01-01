# -*- coding: utf-8 -*-
import time
import log
import pymysql
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrip import models, wdglob
pymysql.install_as_MySQLdb()


# DBINIT
db = create_engine('mysql://root:pety93033@localhost:3306/autotr', echo=False, pool_size=8, pool_recycle=60 * 30)
DbSession = sessionmaker(bind=db)
session = DbSession()
Base = declarative_base()


def finduser(flag=1):
    try:
        a = session.query(models.User).filter(and_(models.User.pt_flag == flag, models.User.flag == 1)).all()
        return a
    except Exception as e:
        log.err('查找用户连接失败;%s'%e)
        return False
def recordorder(userid, ordertime, orderid, side, avgprice, origqty, status, fig, amount, pt):
    order = models.Orders(userid=userid, ordertime=ordertime, orderid=orderid, side=side,
                         avgprice=avgprice,  origqty=origqty, status=status, fig=fig, amount=amount, pt=pt)
    session.add(order)
    session.commit()
    log.info('记录：userid = %s'%userid)

def recordanaly(p,side):
    try:
        bp = p
        ap = wdglob.ETHBODY
        a = ap['ts']
        atime = int(a[0:10])
        b = bp['ts']
        btime = int(b[0:10])
        analy = models.Analy(btime = datetime.fromtimestamp(btime), atime = datetime.fromtimestamp(atime), side = side,  bprice = float(bp['last']), aprice = float(ap['last']),
                             bsz = float(bp['lastSz']), asz = float(ap['lastSz']), b24H = float(bp['vol24h']), a24H = float(ap['vol24h']))
        session.add(analy)
        session.commit()
    except Exception as e:
        log.err(e)

def get_eth1m_lasttime():
    eth1m = models.Ethusdt1m
    coun = session.query(eth1m).count()
    last = session.query(models.Ethusdt1m).filter(eth1m.id == coun).first()
    if last:
        last = last.closetime
    return last

def pos_save1m(res):
    for r in res:
        eth = models.Ethusdt1m(opentime=r.openTime, openpr=r.open, hightpr=r.high, lowpr=r.low, closepr=r.close,
                        bustur=r.quoteAssetVolume, closetime=r.closeTime, busvolu=r.numTrades, busnum=r.volume,
                        actbustur=r.takerBuyBaseAssetVolume, actbusvolu=r.takerBuyQuoteAssetVolume)
        session.add(eth)
        lasttime = r.closeTime
    session.commit()
    return lasttime

def test():
    import makepr
    p = makepr.dticker()
    time.sleep(5)
    b = makepr.dticker()
    recordanaly(p,'buy')
    print('ok order')


