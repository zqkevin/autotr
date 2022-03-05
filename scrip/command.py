import sys, os
from scrip import binance, okex
import time

import log
from datetime import datetime

def servertime(stime):
    now = datetime.now()
    loatime = int(datetime.timestamp(now))
    r = abs(stime - loatime)
    if r > 500:
        now = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
        log.info('现在时间是：%s'%now)
        ti = datetime.fromtimestamp(stime)
        sy = sys.platform
        if sy == 'win32':
            dat = "date %u-%02u-%02u" % (ti.year, ti.month, ti.day)
            tm = "time %02u:%02u:%02u" % (ti.hour, ti.minute, ti.second)
            os.system(dat)
            os.system(tm)
            now = datetime.now()
            now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
            log.info('更新后的时间是：%s'%now)
        else:
            tm = time.strftime('%Y-%m-%d %H:%M:%S', ti)
            command = 'date -s' + ' "{}"'.format(tm)
            os.system(command)
            now = datetime.now()
            now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
            log.info('更新后的时间是：%s'%now)
        return True
    else:
        return False

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

