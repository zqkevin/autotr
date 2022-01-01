from scrip import wdglob, command, okex, analy, trade, makepr, models, binance
from scrip.database import session
from datetime import datetime

import threading
import time
import log

exitFlag = 0
threads = []
check = 0

class Threadmink(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        try:
            binance.geteth1m()
        except Exception as e:
            log.err(e)

class Threadticker(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global exitFlag
        log.info("开启线程：%s"%self.name)
        x = 0
        while exitFlag == 0 and x < 30:
            a = makepr.dticker()
            if a:
                time.sleep(2)
                x = 0
            else:
                x = x + 1
                continue
        log.info('获取市场价格失败，停止挂机')
        exitFlag = 1
        log.info("退出线程：%s"%self.name)


class Threadanaly(threading.Thread):
    def __init__(self, threadID, name, inipr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inipr = inipr
    def run(self):
        global exitFlag
        log.info("开启线程：%s"%self.name)
        if self.inipr:
            p = self.inipr
        else:
            while not wdglob.ETHBODY:
                time.sleep(1)
            p = wdglob.ETHBODY
        x = 0
        while exitFlag == 0:
            time.sleep(5)
            p2 = wdglob.ETHBODY
            a = analy.wave(p)
            ts = datetime.now()
            nowhour = ts.hour
            ts = ts.strftime('%H:%M:%S')
            if a == 1:
                x = x+1
                log.info('触发交易，交易次数：%s'%(x))
                trade.runwave(side='sell')
                p = p2
                continue
            elif a == 0:
                x = x + 1
                log.info('触发交易，交易次数：%s'%(x))
                trade.runwave(side='buy')
                p = p2
                continue
            else:
                # 每24小时对系统数值进行检查矫正
                global check
                if nowhour == 6 and check == 0:
                    init()
                    check = 8
                else:
                    check = 0
                continue
        log.info("退出线程：%s"%self.name)

def init():
    servertime = int((okex.get_server_time())[0:10])
    loatime = int(time.time())
    if abs(servertime - loatime) > 1:
        log.info('本地时间与服务器有差，自动根据服务器时间进行调整')
        command.onlinetime(servertime)
    #计算30天均线价和24小时价
    arprd, arprh = makepr.arp()
    wdglob.arprd = arprd    # 30日均线价
    wdglob.arprh = arprh    # 24小时均线
    # 按最后一条价格数据矫正
    analy = models.Analy
    b = session.query(analy).count()
    a = session.query(analy).filter(analy.id == b).first()
    inipr = {}
    if a:
        inipr['last'] = a.aprice
        inipr['lastSz'] = a.asz
        inipr['vol24h'] = a.a24H
        inipr['ts'] = str(datetime.timestamp(a.atime))
    log.info('%s----较准完毕！'%datetime.fromtimestamp(loatime))
    # 获取分钟K线数据到数据库
    # Threadmink(13,'mink').start()
    return inipr

def start():
    inipr = init()
    ticker = Threadticker(1, 'ticker')
    ticker.start()
    threads.append(ticker)
    analyt = Threadanaly(2, 'analy', inipr)
    analyt.start()
    threads.append(analyt)

    for t in threads:
        t.join()



if __name__ == '__main__':
    #test()
    start()
