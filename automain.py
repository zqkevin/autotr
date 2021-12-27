from scrip import wdglob, command, okcommand, analy, trade, makepr
import okex
from datetime import datetime
import threading
import time


exitFlag = 0
threads = []


class Threadticker(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global exitFlag
        print("开启线程：" + self.name)
        while exitFlag == 0:
            a = makepr.dticker()
            if a:
                time.sleep(2)
            else:
                print('获取市场价格失败，停止挂机')
                exitFlag = 1
        print("退出线程：" + self.name)


class Threadanaly(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global exitFlag
        print("开启线程：" + self.name)
        time.sleep(3)
        x = 0
        while x < 5:
            try:
                p1 = float(wdglob.ETHBODY['last'])
                break
            except:
                time.sleep(2)
                x = x + 1
                continue
        x = 0
        while exitFlag == 0:
            time.sleep(5)
            p2 = float(wdglob.ETHBODY['last'])
            a = analy.wave(p1, p2)
            if a == 1:
                x = x+1
                ts = datetime.now().strftime('%H:%M:%S')
                print(ts, '触发交易，交易次数：', x,'con = ', p2-p1)
                b = trade.wavetrade(side='sell')
                p1 = p2
                continue
            elif a == 0:
                x = x + 1
                ts = datetime.now().strftime('%H:%M:%S')
                print(ts, '触发交易，交易次数：', x, 'con = ', p2-p1)
                b = trade.wavetrade(side='buy')
                p1 = p2
                continue
            else:
                continue
        print("退出线程：" + self.name)



def init():
    servertime = int((okex.get_server_time())[0:10])
    loatime = int(time.time())
    # if abs(servertime - loatime) > 5:
    #     print('本地时间与服务器有差，自动根据服务器时间进行调整')
    #     command.onlinetime()
    arprd, arprh = makepr.arp()
    wdglob.arprd = arprd
    wdglob.arprh = arprh
    print(datetime.fromtimestamp(loatime), '较准完毕！')
    return

def start():
    init()
    ticker = Threadticker(1, 'ticker')
    ticker.start()
    threads.append(ticker)
    analyt = Threadanaly(2, 'analy')
    analyt.start()
    threads.append(analyt)
    # x = 0
    # while x < 300:
    #     x = x + 1
    #     time.sleep(1)
    # global exitFlag
    # exitFlag = 1
    # print("退出主线程")
    for t in threads:
        t.join()



if __name__ == '__main__':
    #test()
    start()
