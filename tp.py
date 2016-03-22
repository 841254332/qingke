__author__ = 'admin'
import urllib2
import urllib
import time
global count
count = 0


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.clock()
        fn(*args, **kwargs)
        print "%s cost %s second"%(fn.__name__, time.clock() - start)
    return _wrapper

@time_me
def toupiao():
    posturl = 'http://www.winqee.com/interface.php/Tp/tp'
    data = {'id':'7'}
    requestdata = urllib.urlencode(data)
    urllib2.urlopen(posturl, requestdata)

toupiao()


time_me(toupiao)