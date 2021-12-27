import time
from scrip import wdglob
def wave(p1,p2):
    try:
        con = round((p2 - p1)/p2, 4)
        if con >= wdglob.amp:

            return 1 #做空头sell
        elif con <= -wdglob.amp:

            return 0  # 做多头buy
        else:
            return 'pass'
    except:
        print('err')
        return 'err'

def start(p1,p2):
    a = wave(p1,p2)
    return a
