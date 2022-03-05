from scrip import wdglob
import log
import numpy as np

def wavesz(acc, a, side):
    try:
        p = float(wdglob.ETHBODY['p'])
        arprd = float(wdglob.arprd)  # 30天均线价格
        arprh = float(wdglob.arprh)
        ky = acc['acc_ky']*a.touru/10
        zs = acc['acc_zs']*a.touru/10
        zy = acc['acc_zy']*a.touru/10
        posside = acc['pos_side']
        amp = float(wdglob.amp)
        lever = acc['lever']
        share = a.fengxian*30
        #计算市场价和均价的系数
        p_arprd = (p - arprd)/p/amp/share
        # 持仓情况
        if zs > 100:
            pos_zy = zy / zs
            if zy < (zs * 0.7):
                bili = np.sin(zy / zs * 4)
            else:
                bili = -0.75
        else:
            log.acc('%s账户金额低于100U,暂停交易' % a.name)
            return False
        arprdxs = 1 + abs(p_arprd) - pos_zy
        if arprdxs < 0.5:
            arprdxs = 0.5
        jysz = round(zs * lever / share, 2)
        if jysz < 10:
            jysz = 10
        if posside == 0:    #持仓方向多
            if p_arprd < 0:
                if side == "buy":
                    if ky < 50:
                        log.acc('%s账户可用金额不足,暂停交易' % a.name)
                        return False
                    else:
                        sz = jysz*arprdxs
                else:
                    sz = jysz/arprdxs
            else:
                if side == "buy":
                    if ky < 50:
                        log.acc('%s账户可用金额不足,暂停交易' % a.name)
                        return False
                    else:
                        sz = jysz/arprdxs
                else:
                    sz = jysz*arprdxs

        else:   #持仓方向空
            if p_arprd < 0:
                if side == "sell":
                    if ky < 50:
                        log.acc('%s账户可用金额不足,暂停交易' % a.name)
                        return False
                    sz = jysz / arprdxs
                else:
                    sz = jysz * arprdxs
            else:
                if side == "sell":
                    if ky < 50:
                        log.acc('%s账户可用金额不足,暂停交易' % a.name)
                        return False
                    sz = jysz * arprdxs
                else:
                    sz = jysz / arprdxs
        zzsz = sz + (sz * bili)
        if zzsz < 30:
            log.acc('%s账户可用金额不足,暂停交易' % a.name)
            return False
        return zzsz  # 返回值为在当前杠杆下交易的金额
    except Exception as e:
        log.err(e)
        return False
