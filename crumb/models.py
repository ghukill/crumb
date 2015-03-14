# models for crumb server

#python modules
import md5

#crumb modules
import localConfig



class Crumb(object):
	'''
	Class for individual crumb.
		- defines, writes, updates, deletes
	'''

	def __init__(self, key, value, index='def'):

		#derive id from key
		self.id = md5.new(key).hexdigest()
		self.key = key		
		self.value = value
		self.index = index

		# derive fs location
		self.fs_location = False



	
	def write(self):
		'''
		write crumb to filesystem
		'''
		pass


	def get(self):
		'''
		retrieve crumb from filesystem
		'''
		pass


	def update(self):
		'''
		write crumb to filesystem
		'''
		pass


	def delete(self):
		'''
		write crumb to filesystem
		'''
		pass
