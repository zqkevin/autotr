from scrip import wdglob, command, okex, analy, makepr, binance, database
from datetime import datetime
import threading, time, log
exitFlag = 0
threads = []
class Threadtimer(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        try:
            global exitFlag
            log.info("开启线程：%s" % self.name)
            while exitFlag == 0:
                # 每24小时对系统数值进行检查矫正
                ts = datetime.now()
                nowhour = ts.hour
                check = wdglob.check
                if nowhour == 6 and check == 0:
                    init()
                    wdglob.check = 1
                elif nowhour != 6 and check == 1:
                    wdglob.check = 0
                time.sleep(600)
                continue
        except Exception as e:
            log.err('定时器失效，重启程序',e)
            exitFlag = 1
            log.info("退出线程：%s" % self.name)

class Threadticker(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global exitFlag
        log.info("开启线程：%s" % self.name)
        x = 0
        while exitFlag == 0 and x < 3:
            if wdglob.binanceserver or wdglob.okexserver:
                if wdglob.binanceserver == 1:
                    a = makepr.webbian()
                else:
                    a = makepr.webok()
                if not a:
                    x = x + 1
                    time.sleep(10)
                    continue
            else:
                log.info('网络无法连接，获取价格失败，停止挂机')
                exitFlag = 1
                log.info("退出线程：%s" % self.name)
        log.info('获取市场价格失败，停止挂机')
        exitFlag = 1
        log.info("退出线程：%s" % self.name)


class Threadanaly(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global exitFlag
        log.info("开启线程：%s" % self.name)
        x = 0
        while exitFlag == 0 and x < 3:
            analy.ethwave()
            x = x + 1
        exitFlag = 1
        log.info("退出线程：%s"%self.name)

def init():
    #进行服务平台连通性测试
    stime = int(binance.get_server_time()/1000)
    if stime:
        wdglob.binanceserver = 1
        if command.servertime(stime):
            log.info('本地时间与服务器有差，自动根据服务器时间进行调整')
    else:
        wdglob.binanceserver = 0
    okserver = okex.get_instruments()
    if okserver:
        if okserver['state'] == 'live':
            wdglob.okexserver = 1
        else:
            wdglob.okexserver = 0
    #计算30天均线价和24小时价
    arprd, arprh = makepr.arp()
    wdglob.arprd = arprd    # 30日均线价
    wdglob.arprh = arprh    # 24小时均线
    #按最后一条价格数据矫正

    a = database.lastanyle()
    inipr = {}
    if a:
        inipr['p'] = a.aprice
        inipr['pc'] = a.asz
        inipr['24hv'] = a.a24H
        inipr['ts'] = str(datetime.timestamp(a.atime))

    log.info('%s----较准完毕！' % datetime.fromtimestamp(stime))

    return inipr

def start():
    inipr = init()
    ticker = Threadticker(1, 'ticker')
    ticker.start()
    threads.append(ticker)
    analyt = Threadanaly(2, 'analy')
    analyt.start()
    threads.append(analyt)
    timer = Threadtimer(3, 'timer')
    timer.start()
    threads.append(timer)
    for t in threads:
        t.join()



if __name__ == '__main__':
    #test()
    start()
