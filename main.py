import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
from config import DATABASE_URI
from datetime import datetime
from sqlalchemy import extract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrip import models, wdglob
import numpy as np
pymysql.install_as_MySQLdb()

# DBINIT
db = create_engine(DATABASE_URI, echo=False, pool_size=8, pool_recycle=60 * 30)
DbSession = sessionmaker(bind=db)
session = DbSession()
Base = declarative_base()
app = FastAPI()
class psymbo(BaseModel):
    userid: int
    name: str = None
    username: str = None
    pt_name: str = 'bf'
    pt_flag: int = 0


class gsymbo(BaseModel):
    stime: datetime

@app.get('/user{uid}')
async def user(uid: int):
    try:
        user = session.query(models.User).filter_by(userid=uid).first()
        if user:
            return {'message': user, 'code': 1}
        return {'message': 'nofind userstatus', 'code': 0}
    except:
        return {'message': 'sever err', 'code': 0}

@app.get('/userstatus{uid}')
async def userstatus(uid: int):
    try:
        userstatu = session.query(models.User_status).filter_by(userid=uid).first()
        if userstatu:
            return {'message': userstatu, 'code': 1}
        return {'message': 'nofind userstatus', 'code': 0}
    except:
        return {'message': 'sever err', 'code': 0}
@app.post('/adduser{uid}')
async def adduser(uid: int, userid, name, username, pt: str = 'bf'):
    try:
        user = models.User()
        user.userid = userid
        user.name = name
        user.username = username
        user.pt_name = pt
        session.add(user)
        status = models.User_status()
        status.userid = userid
        status.name = name
        session.add(status)
        session.commit()
        conuser = session.query(models.User).filter_by(userid=userid).first()
        if conuser:
            return {'message': 'add success', 'code': 1}
        return {'message': 'add Flase', 'code': 0}
    except:
        return {'message': 'sever err', 'code': 0}


@app.post('/rootset{uid}')
async def rootset(uid, lever: int, fengxian: int):
    try:
        user = session.query(models.User).filter_by(userid=uid).first()
        user.fengxian = fengxian
        user.touru = lever
        statu = session.query(models.User_status).filter_by(userid=uid).first()
        statu.lever = lever
        session.commit()
        return {'message': 'success', 'code': 1}
    except:
        return {'message': 'sever err', 'code': 0}

@app.post('/deluser{uid}')
async def deluser(uid, delid: int):
    try:
        user = session.query(models.User).filter_by(userid = delid).first()
        user.flag = 0
        session.commit()
        return {'message': 'delsuccess', 'code': 1}
    except:
        return {'message': 'sever err', 'code': 0}

@app.post('/setkey{uid}')
async def setkey(uid: int, apikey: str, secretkey: str, pt: str = 'bianace'):
    try:
        user = session.query(models.User).filter_by(userid=uid).first()
        if user:
            user.pt_name = pt
            user.pt_api_key = apikey
            user.pt_secret_key = secretkey
            session.commit()
            return {'message': 'change success', 'code': 1}
        return {'message': 'user unfind', 'code': 0}
    except:
        return {'message': 'sever err', 'code': 0}
@app.get('/order{uid}')
async def order(uid: int, year, month, day='%'):
    try:
        order = models.Orders
        list = session.query(order).filter(order.userid == uid, extract('year', order.ordertime).like(year), extract('month', order.ordertime).like(month),
                                               extract('day', order.ordertime).like(day)).all()
        if list:
            return {'message': list,'code':1}
        else:
            return {'message':'无数据','code':0}
    except:
        return {'message': 'sever err', 'code': 0}
@app.get('/totalfig{uid}')
async def totalfig(uid: int, year, month, day='%'):
    try:
        order = models.Orders
        if day == '%':
            nowday = datetime.now().day
            days = np.arange(1, nowday)
            figs = []
            for a in days:
                list = session.query(order).filter(order.userid == uid, extract('year', order.ordertime).like(year),
                                                   extract('month', order.ordertime).like(month),
                                                   extract('day', order.ordertime).like(a)).all()
                if list:
                    fig = 0
                    for b in list:
                        fig = fig + b.fig
                    figs.append(fig)
            return {'message': figs, 'code': 2}
        else:
            list = session.query(order).filter(order.userid == uid, extract('year', order.ordertime).like(year), extract('month', order.ordertime).like(month),
                                                   extract('day', order.ordertime).like(day)).all()
            if list:
                fig = 0
                for a in list:
                    fig = fig + a.fig
                return {'message': fig, 'code':1}
            else:
                return {'message':'无数据','code':0}
    except:
        return {'message': 'sever err', 'code': 0}
@app.post('/setrun{uid}')
async def setrun(uid: int):
    try:
        userid = uid
        user = session.query(models.User).filter_by(userid=userid).first()
        if user.pt_name and user.pt_secret_key and user.pt_api_key:
            if user.pt_flag == 0:
                user.pt_flag = 1
            else:
                user.pt_flag = 0
            session.commit()
            return {'message': 'success', 'code': 1}
        else:
            return {'message': 'nokey', 'code': 0}
    except:
            return {'message': 'False', 'code': 0}


