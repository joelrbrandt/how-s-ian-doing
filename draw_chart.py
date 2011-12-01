from datetime import datetime, timedelta

import log_parser

GOOGLE_CHART_BASE_URL="http://chart.googleapis.com/chart?"

ONE_DAY = timedelta(1)
HALF_DAY = ONE_DAY / 2


"""
CHART PARAMETERS

cht=s
chs=500x300
chtt=Ian's+Dissertation
chts=676767,20

chd=t:0,10,20,30,40,50,60,70,80,90,100,60,60,80,80
    9,98,60,27,34,56,79,58,74,18,76,0,50,0,20

chm=o,000000,0,-1,0
    D,0033ff,0,0:10,1,1
    D,A0BAE9,0,11:12,50,1
    D,A0BAE9,0,13:14,50,1

chxt=x,y,r
chxr=0,0,40|1,0,50|2,0,80
chxl=0:|Sept|Oct|Nov
chxp=0,10,20,30
"""
def build_chart():
    l = log_parser.read_log()

    if len(l) > 0: # add current time's value, which is the same as the last update
        l.append((datetime.now(), l[-1][1])) 

    wpd = log_parser.calc_wpd(l)

    params = {}
    params['cht'] = 's'
    params['chs'] = '500x300'
    params['chtt'] = 'Ian\'s+Dissertation'
    params['chts'] = '000000,20'
    params['chxt'] = 'y,r'

    # get line chart data

    first = min(l[0][0], wpd[0][0])
    first = datetime(first.year, first.month, first.day) # change first to beginning of first day

    # insert a point to make the chart meet up correctly at the 0
    x = [0]
    y = [l[0][1]]
    
    for i in l:
        x.append(time_delta_to_minutes(i[0]-first))
        y.append(i[1])

    # make the chart (but not the graph) go through the end of the current day (so last bar fits on)
    n = datetime.now()
    last = datetime(n.year, n.month, n.day) + ONE_DAY

    # get wpd chart data

    dx = []
    dy = []
    for i in wpd:
        dx.append(time_delta_to_minutes((i[0]+HALF_DAY)-first))
        dy.append(i[1])
        
    # scale everything to 100

    xmin = 0
    xmax = time_delta_to_minutes(last-first)

    ymin = min(y)
    ymax = max(y)

    dymin = min(dy)
    dymax = max(dy)

    yrange = ymax-ymin
    addition = 0.1*yrange
    ymin = ymin - addition
    ymax = ymax + addition

    dyrange = dymax-dymin
    addition = 0.1*dyrange
    dymin = dymin - addition
    dymax = dymax + addition

    xscale = 100.0/(xmax-xmin)
    yscale = 100.0/(ymax-ymin)
    dyscale = 100.0/(dymax-dymin) 

    for i in range(len(x)):
        x[i] = (x[i]-xmin) * xscale
        y[i] = (y[i]-ymin) * yscale

    for i in range(len(dx)):
        dx[i] = (dx[i]-xmin) * xscale
        dy[i] = (dy[i]-dymin) * dyscale

    dyzero = (0-dymin) * dyscale

    # double up the wpd points to make bars
    a = []
    b = []
    for i in range(len(dx)):
        a.append(dx[i])
        a.append(dx[i])
        b.append(dyzero)
        b.append(dy[i])

    a.extend(x)
    b.extend(y)

    xpoints = ",".join(map(one_decimal,a))
    ypoints = ",".join(map(one_decimal,b))

    params['chd'] = 't:' + xpoints + '|' + ypoints

    # make the stupid bar marks
    barmarks = []
    barwidth = max((440 / (last-first).days) - 2, 1)
    for i in range(len(dx)):
        barmarks.append('D,A0BAE9,0,'+ str(i*2) + ':' + str(i*2+1) +',' + str(barwidth) + ',1')
    
    params['chm'] = 'o,000000,0,-1,0|' + '|'.join(barmarks) + '|H,A0BAE9,0,0,1|D,ff9900,0,' + str(len(dx)*2) +  ':' + str(len(a)-1) + ',2,1'
    
    # figure out axes

    params['chxr'] = '0,' + str(ymin) + ',' + str(ymax) + '|1,' + str(dymin) + ',' + str(dymax)

    # output it

    q = []
    for k in params.keys():
        q.append(k + '=' + str(params[k]))

    return "&".join(q)


def time_delta_to_minutes(td):
    return int(td.days*60*24 + td.seconds/60)

def one_decimal(f):
    return ('%2.1f' % f)

if __name__ == '__main__':
    print build_chart()
