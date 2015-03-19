#utilities

#python core
import time

# small decorator to time functions
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms, %0.3f s' % (f.func_name, (time2-time1)*1000.0, (time2-time1))
        return ret
    return wrap




