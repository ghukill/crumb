# models for crumb server

#python modules
import md5
import logging
import os

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
		self.dir_l1 = self.id[0:2]+"/"
		self.dir_l2 = self.id[2:4]+"/"
		self.dir_full = localConfig.fs_root+self.dir_l1+self.dir_l2
		self.fs_full = self.dir_full+self.id

		# group main IO methods
		self.IO = self.IO_proto(self)



	class IO_proto(object):

		def __init__(self, crumb):			
			#pass main crumb self (all values same with 'self.crumb' prefix)
			self.crumb = crumb


		def write(self):
			'''
			write crumb to filesystem
			'''

			# create directory structure if necessary
			# check level 1
			if os.path.exists(localConfig.fs_root+self.crumb.dir_l1) == False:
				os.makedirs(localConfig.fs_root+self.crumb.dir_l1)
			# check level 2
			if os.path.exists(localConfig.fs_root+self.crumb.dir_l2) == False:
				os.makedirs(localConfig.fs_root+self.crumb.dir_l1+self.crumb.dir_l2)

			# write crumb
			fhand = open(self.crumb.fs_full,"w")
			fhand.write(self.crumb.value)
			fhand.close()
			logging.debug("successful write key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))


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
			# delete directory structure if necessary
			
			



