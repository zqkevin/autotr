import sys, os, pytz, time
import log
from datetime import datetime
import win32api
import ntplib
import struct, socket

def servertime(stime):
    now = datetime.now()
    now = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
    log.info('现在时间是：%s'%now)

    ti = datetime.fromtimestamp(stime, pytz.timezone('Asia/Shanghai'))
    sy = sys.platform
    if sy == 'win32':
        dat = "date %u-%02u-%02u" % (ti.year, ti.month, ti.day)
        tm = "time %02u:%02u:%02u" % (ti.hour,ti.minute,ti.second)
        os.system(dat)
        os.system(tm)
        now = datetime.now()
        now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        log.info('更新后的时间是：%s'%now)
    else:
        pass
        # tm='date -s "%u-%u-%u %u:%u:%u"'%(ti.year, ti.month, ti.day, ti.hour,ti.minute,ti.second)
        # hw="/sbin/clock -w"
        # os.system(tm)
        # os.system(hw)
        # now = datetime.now()
        # now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        # log.info('更新后的时间是：%s'%now)
    return
def onlinetime():
    now = datetime.now()
    now = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
    print('现在时间是：',now)
    TimeServer = 'time.windows.com'  # 国家授时中心ip
    Port = 123
    def getTime():
        TIME_1970 = 2208988800
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '\x1b' + 47 * '\0'
        data = bytes(data, 'utf-8')
        client.sendto(data, (TimeServer, Port))
        data, address = client.recvfrom(1024)
        data_result = struct.unpack('!12I', data)[10]
        data_result -= TIME_1970
        return data_result

    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(getTime())
    win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)
    now = datetime.now()
    now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    print('更新后的时间是：', now)

def to_dict(objj):
    is_list = objj.__class__ == [].__class__
    is_set = objj.__class__ == set().__class__
    x = 0
    if is_list or is_set:
        obj_arr = {}
        for o in objj:
            # 把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr[x] = dict
            x = x + 1
        return obj_arr
    else:
        print('2')
        dict = {}
        dict.update(objj.__dict__)
        return dict

