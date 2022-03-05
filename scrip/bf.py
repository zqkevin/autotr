from scrip import database, wdglob
from datetime import datetime


def greatord(userid, jyzs, side):
    p = float(wdglob.ETHBODY['p'])
    sz = round(jyzs / p, 4)
    userord = database.getbford(userid).orderid
    orderid = str(int(userord) + 1)
    order = {}
    order['orderid'] = orderid
    order['ordertime'] = datetime.fromtimestamp(int(datetime.timestamp(datetime.now())))
    order['avgprice'] = p
    order['origqty'] = sz
    order['side'] = side
    order['status'] = 'FILLED'
    return order


def getacc(userid):
    re = database.getbfacc(userid)
    p = float(wdglob.ETHBODY['p'])
    acc = {}
    acc['acc_wsx'] = (re.ccp - p)*abs(re.ccl)
    acc['acc_ky'] = re.totalcapital - re.ccp*abs(re.ccl)/re.lever
    acc['acc_zs'] = re.totalcapital
    acc['acc_zy'] = re.ccp*abs(re.ccl)/re.lever
    acc['pos_ccj'] = re.ccp
    acc['pos_ccl'] = re.ccl
    if re.ccl < 0:
        acc['pos_side'] = 1
    else:
        acc['pos_side'] = 0
    acc['lever'] = re.lever
    return acc

getacc(userid=5)
