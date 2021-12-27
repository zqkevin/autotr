# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, INT, Float, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    username = Column(String(20))
    analy = Column(INT, default=0)
    analy1 = Column(INT, default=0)
    analy2 = Column(INT, default=0)
    share = Column(INT, default=100)
    pt_name = Column(String(128))
    pt_flag = Column(INT)
    pt_api_key = Column(String(128))
    pt_secret_key = Column(String(128))
    pt_passphrase = Column(String(128))
    pt_other = Column(String(128))
    flag = Column(INT, default=1)



class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(60))
    year = Column(String(4))


class Ethusdt1m(Base):
    __tablename__ = 'ethusdt1m'
    id = Column(Integer, primary_key=True)
    opentime = Column(Float)
    openpr = Column(Float)
    hightpr = Column(Float)
    lowpr = Column(Float)
    closepr = Column(Float)
    bustur = Column(Float)
    closetime = Column(Float)
    busvolu = Column(Float)
    busnum = Column(Integer)
    actbustur = Column(Float)
    actbusvolu = Column(Float)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    userid = Column(INT)  # 下单用户
    ordertime = Column(DateTime)  # 成交时间
    avgprice = Column(Float)  # 成交均价
    orderid = Column(String(30))  # 订单id
    side = Column(String(30))  # 订单方向
    price = Column(Float)  # 下单价格
    origqty = Column(Float)  # 成交数量
    status = Column(String(30))  # 订单状态
    fig = Column(Float)  # 盈亏
