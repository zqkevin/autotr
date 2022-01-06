from scrip import wdglob, database
import log
from test import temptest

def wavesz(acc, a, side):
    p = float(wdglob.ETHBODY['last'])
    ky = float(acc['acc_ky'])
    zs = float(acc['acc_zs'])
    posccj = float(acc['pos_ccj'])

    bili = ky/zs
    sz = round(acc['acc_zs'] * acc['lever'] / a.share, 4)

    if side == 'buy':
        if sz > acc['acc_ky'] * acc['lever'] or sz < 10:
            log.acc('%s账户可用金额不足,暂停交易' % a.user)
            return False
    else:
        sz = round(sz / p, 4)

if __name__ == '__main__':
    acc = temptest.test()
    side = 'buy'
    userlist = database.finduser(flag=1)
    a = userlist[0]
    wavesz(acc, a, side)
