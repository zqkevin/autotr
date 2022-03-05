# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, INT, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userid = Column(INT)
    name = Column(String(20))
    username = Column(String(20))
    analy = Column(INT, default=0)
    analy1 = Column(INT, default=0)
    analy2 = Column(INT, default=0)
    share = Column(INT, default=100)
    pt_name = Column(String(128))
    pt_flag = Column(INT, default=0)
    pt_api_key = Column(String(128))
    pt_secret_key = Column(String(128))
    pt_passphrase = Column(String(128))
    pt_other = Column(String(128))
    flag = Column(INT, default=1)
    touru = Column(INT, default=10)
    fengxian = Column(INT, default=5)

class User_status(Base):
    __tablename__ = 'user_status'
    id = Column(Integer, primary_key=True)
    userid = Column(INT)
    name = Column(String(20))
    totalcapital = Column(Float, default=0)
    totalpl = Column(Float, default=0)
    ccl = Column(Float, default=0)
    ccp = Column(Float, default=0)
    lever = Column(INT, default=3)

class User_change(Base):
    __tablename__ = 'user_change'
    id = Column(Integer, primary_key=True)
    userid = Column(INT)
    name = Column(String(20))
    type = Column(String(20))
    quantity = Column(Float, default=0)
    time = Column(DateTime)


class Analy(Base):
    __tablename__ = 'analy'
    id = Column(Integer, primary_key=True)
    btime = Column(DateTime)
    atime = Column(DateTime)
    side = Column(String(32))  # 触发方向
    bprice = Column(Float)  # 前一次市场价
    aprice = Column(Float)  # 本次触发市场价
    bsz = Column(Float)  # 前一条最新成交数
    asz = Column(Float)  # 本次最新成交数
    b24H = Column(Float)    # 前一次总交易量
    a24H = Column(Float)    # 本次总交易量

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    userid = Column(INT)  # 下单用户
    pt = Column(INT)    # 使用平台 1:okex 2:bianace 3:belife
    ordertime = Column(DateTime)  # 成交时间
    avgprice = Column(Float)  # 成交均价
    orderid = Column(String(30))  # 订单id
    side = Column(String(30))  # 订单方向
    price = Column(Float)  # 下单价格
    origqty = Column(Float)  # 成交数量
    status = Column(String(30))  # 订单状态
    fig = Column(Float)  # 盈亏
    lever = Column(INT)  # 杠杆
    acc_ky = Column(Float)  # 可用资金
    acc_zy = Column(Float)  # 占用资金
    acc_wsx = Column(Float)  # 未实现盈利
    pos_ccl = Column(Float)  # 持仓量
    pos_ccj = Column(Float)  # 持仓价
    pos_side = Column(INT)  # 持仓方向
    amount = Column(Float)  # 资金总额
