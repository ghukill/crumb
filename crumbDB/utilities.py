#utilities

#python core
import time

# crumb_lock
crumb_lock = set()


# small decorator to time functions
def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print '%s function took %0.3f ms, %0.3f s' % (f.func_name, (time2-time1)*1000.0, (time2-time1))
		return ret
	return wrap


def crumbLockDec(f):
	def wrap(*args):
		self = args[0]
		# lock crumb
		if self.crumb.crumb_lock_id in crumb_lock:
			raise Exception("crumb is locked")
		else:
			crumb_lock.add(self.crumb.crumb_lock_id)
			ret = f(*args)
			crumb_lock.discard(self.crumb.crumb_lock_id)
			return ret
	return wrap




