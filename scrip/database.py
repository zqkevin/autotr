# -*- coding: utf-8 -*-
import time
import log
import pymysql
from config import DATABASE_URI
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrip import models, wdglob
pymysql.install_as_MySQLdb()


# DBINIT
db = create_engine(DATABASE_URI, echo=False, pool_size=8, pool_recycle=60 * 30)
DbSession = sessionmaker(bind=db)
session = DbSession()
Base = declarative_base()

def lastanyle():
    analy = models.Analy
    b = session.query(analy).count()
    return session.query(analy).filter(analy.id == b).first()

def upuser_status(userid, p, sz, side, acc):
    update = session.query(models.User_status).filter_by(userid=userid).first()
    if update:
        old_totalcapital = update.totalcapital
        old_ccp = update.ccp
        old_ccl = update.ccl
        if side == 'sell' or 'SELL':
            update.ccl = old_ccl - sz
            if update.ccl > 0 and old_ccl > 0:
                fig = (p - old_ccp) * sz * (1 - 0.001)
            elif old_ccl < 0 and update.ccl < 0:
                fig = -sz * p * 0.001
            else:
                fig = (p-old_ccp) * old_ccl * (1 - 0.001)
        else:
            update.ccl = old_ccl + sz
            if update.ccl < 0 and old_ccl < 0:
                fig = (p - old_ccp) * sz * (1 - 0.001)
            elif update.ccl > 0 and old_ccl > 0:
                fig = -sz * p * 0.001
            else:
                fig = (p - old_ccp) * old_ccl * (1 - 0.001)
        update.ccp = (old_ccp * abs(old_ccl) + sz * p) / (abs(old_ccl) + sz)
        update.totalcapital = old_totalcapital + fig
        update.totalpl = update.totalpl + fig
        session.commit()
        return fig
    else:
        adduser = models.User_status()
        adduser.userid = userid
        adduser.name = userid
        adduser.totalcapital = acc['acc_zs']
        adduser.totalpl = 0
        adduser.ccl = acc['pos_ccl']
        adduser.ccp = acc['pos_ccj']
        adduser.lever = acc['lever']
        session.add(adduser)
        session.commit()
        fig = 0
        return fig

def getbfacc(userid):
    re = session.query(models.User_status).filter_by(userid=userid).first()
    return re

def getbford(userid):
    re = session.query(models.Orders).filter(models.Orders.userid == userid).order_by(models.Orders.id.desc()).first()
    if not re:
        re = models.Orders
        re.orderid = "1"
    return re

def finduser(flag=1):
    try:
        a = session.query(models.User).filter(and_(models.User.pt_flag == flag, models.User.flag == 1)).all()
        return a
    except Exception as e:
        log.err('查找用户连接失败;%s'%e)
        return False
def recordorder(rt):
    order = models.Orders(userid=rt['userid'], pt=rt['pt'],
                          ordertime=rt['ordertime'], avgprice=rt['avgprice'],
                          orderid=rt['orderid'], side=rt['side'],
                          origqty=rt['origqty'], status=rt['status'],
                          fig=rt['fig'], lever=rt['lever'],
                          acc_ky=rt['acc_ky'], acc_zy=rt['acc_zy'],
                          acc_wsx=rt['acc_wsx'], pos_ccl=rt['pos_ccl'],
                          pos_ccj=rt['pos_ccj'], pos_side=rt['pos_side'],
                          amount=rt['amount'])
    session.add(order)
    session.commit()
    log.info('记录：userid = %s' % rt['userid'])

def recordanaly(p, nowp, side):
    try:
        bp = p
        ap = nowp
        a = ap['ts']
        atime = int(a/1000)
        b = bp['ts']
        btime = int(b/1000)
        analy = models.Analy(btime = datetime.fromtimestamp(btime), atime = datetime.fromtimestamp(atime), side = side,  bprice = float(bp['p']), aprice = float(ap['p']),
                             bsz = float(bp['pc']), asz = float(ap['pc']), b24H = float(bp['24hv']), a24H = float(ap['24hv']))
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




