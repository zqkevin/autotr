# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrip import models

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
    except:
        print('查找用户连接失败')
        return False
def recordorder(userid, ordered):
    a = ordered['fillTime']
    a = int(a[0:10])
    ordertime = datetime.fromtimestamp(a)

    order = models.Order(userid=userid, ordertime=ordertime, orderid=ordered['ordId'], side=ordered['side'],
                         avgprice=ordered['avgPx'],  origqty=round(float(ordered['accFillSz']), 4), status=ordered['state'], fig=ordered['pnl'])
    session.add(order)
    session.commit()
    print('记录：userid =',userid)
def todb():
    user = models.User()
    user.username = 'Tom'
    user.name = 'Tom.P'
    user.set_password(password='123456')
    user.pt_api_key = "78956841-cd75-40f4-91ec-8f96107f4fbc2"
    user.pt_secret_key = "E3F33AAD8B7F9692CD5114EF7F0B1B982"
    user.pt_passphrase = "23456"
    user.pt_name = 'okex'
    user.pt_flag = 1
    user.flag = 1
    session.add(user)
    session.commit()
    print('ok')
def test():
    a = '1640117202661'
    d = int(a[0:10])
    b = datetime.fromtimestamp(d)
    # c = datetime.isoformat(b)


    order = models.Order(userid=5, ordertime=b, orderid=123456, side='buy',
                             avgprice=4021,  origqty=0.01, status='fill', fig=-0.2)
    session.add(order)
    session.commit()
    print('ok order')


