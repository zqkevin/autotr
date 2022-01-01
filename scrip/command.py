import sys, os, pytz, time
import log
from datetime import datetime
import win32api
import ntplib

def onlinetime(stime):
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
