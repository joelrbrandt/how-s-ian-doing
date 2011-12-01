import sys, subprocess, os
from datetime import datetime, timedelta

import log_parser

IMAGE_DIRECTORY = "/home/jbrandt/joelbrandt.org/howsiandoing/i"
IMAGE_URL_BASE = "http://joelbrandt.org/howsiandoing/i/"
PHP_TWEET_SCRIPT = "/home/jbrandt/joelbrandt.org/howsiandoing/tweet.php"

def tweet_if_appropriate(timestamp, t):
    l = log_parser.read_log()
    ld = log_to_dict(l)

    msg = None

    if t in ld:
        msg = "Word count: %s" % ld[t]
        print "gunna tweet"
        just_date = datetime(t.year, t.month, t.day)
        wpd = log_to_dict(log_parser.calc_wpd(l))
        if just_date in wpd:
            print "...with wpd"
            msg = msg + (", so far today: %s" % wpd[just_date])
            possible_img = os.path.join(IMAGE_DIRECTORY, "%s.png" % timestamp)
            if os.path.isfile(possible_img):
                print "...and img"
                msg = msg + (" %s%s.png" % (IMAGE_URL_BASE, timestamp))

    else:
        print "not gunna tweet"
    
    if msg:
        print "tweeting: ", msg
        send_tweet(msg)


def log_to_dict(l):
    d = {}
    for i in l:
        d[i[0]] = i[1]
    return d
        

def send_tweet(msg):
    try:
        subprocess.check_call(["/usr/local/bin/php", PHP_TWEET_SCRIPT, msg])
    except:
        print "didn't work"

if __name__ == '__main__':
    timestamp = None
    
    if len(sys.argv) >= 2:
        try:
            timestamp = int(sys.argv[1])
            t = datetime.fromtimestamp(timestamp)
            tweet_if_appropriate(timestamp, t)
            #send_tweet('this sucks more: %s' % timestamp)
        except:
            print "I can't parse that in the arguments line"
            raise
