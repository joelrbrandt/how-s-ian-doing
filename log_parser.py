from datetime import datetime, timedelta

LOGFILE = "/home/jbrandt/joelbrandt.org/howsiandoing/log.txt"

ONE_DAY = timedelta(1)

def read_log():
    result = []
    try:
        last = -1
        
        f = open(LOGFILE)
        for line in f:
            t, c = line.split()
            t = int(t)
            c = int(c)
            if c != 0 and c != last:
                last = c
                t = datetime.fromtimestamp(t)
                result.append((t,c))
        f.close()
    except Exception, e:
        print str(e)
        
    return result

def calc_daily(l):
    daily = []

    t = l[0][0]
    current_day = datetime(t.year, t.month, t.day)
 
    current_count = -1

    for d in l:
        while d[0] > (current_day + ONE_DAY):
            daily.append((current_day, current_count))
            current_day = current_day + ONE_DAY
            
        current_count = d[1]

    # append all the additional days up to today
    today = datetime.now()
    while current_day < today:
            daily.append((current_day, current_count))
            current_day = current_day + ONE_DAY

    return daily


def calc_wpd(l):
    daily = calc_daily(l)
    wpd = []

    last = daily.pop(0)[1]
    for d in daily:
        wpd.append((d[0], d[1]-last))
        last = d[1]

    return wpd
