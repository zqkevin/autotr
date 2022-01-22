from scrip import wdglob, database
import log
from test import temptest

def wavesz(acc, a, side):
    p = float(wdglob.ETHBODY['last'])
    arprd = float(wdglob.ETHBODY['arpre'])  # 30天均线价格
    arprh = float(wdglob.ETHBODY['arprh'])
    ky = acc['acc_ky']*a.touru/10
    zs = acc['acc_zs']*a.touru/10
    zy = acc['acc_zy']*a.touru/10
    posccj = acc['pos_ccj']
    posccl = acc['pos_ccl']
    posside = acc['pos_side']
    amp = float(wdglob.ETHBODY['amp'])
    lever = acc['lever']
    share = a.fengxian*40
    # 计算市场价和均价的系数
    p_arprd = (p - arprd)/p/amp/share
    # 持仓情况
    pos_zy = zy/zs
    arprdxs = 1 + abs(p_arprd) - pos_zy
    kybili = 1 + ky/zs
    jysz = round(zs * lever / share, 2)
    if jysz < 10:
        jysz = 10
    if posside == 0:    #持仓方向多
        if side == "buy":
            if ky < 50:
                log.acc('%s账户可用金额不足,暂停交易' % a.user)
                return False
            jysz = jysz*arprdxs
        else:
            jysz = jysz/arprdxs
    else:   #持仓方向空
        if side == "sell":
            if ky < 50:
                log.acc('%s账户可用金额不足,暂停交易' % a.user)
                return False
            jysz = jysz * arprdxs  # 市场价在30日均线下,现在持仓方向多
        else:
            jysz = jysz / arprdxs
    jysz = jysz*kybili
    return jysz
# if __name__ == '__main__':
#     acc = temptest.test()
#     side = 'buy'
#     userlist = database.finduser(flag=1)
#     a = userlist[0]
#     wavesz(acc, a, side)
