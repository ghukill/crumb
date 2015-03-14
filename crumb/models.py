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

	Crumb can be instatiated with key AND value, or just key for updating / get / delete
	'''

	def __init__(self, key, value=False, index='def'):

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
		self.io = self.IO(self)



	class IO(object):

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

			# write crumb file
			fhand = open(self.crumb.fs_full,"w")
			fhand.write(self.crumb.value)
			fhand.close()
			logging.debug("successful write key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))


		def get(self):
			'''
			retrieve crumb from filesystem
			'''

			# get and retrieve
			fhand = open(self.crumb.fs_full,"r")
			return fhand.read()
			fhand.close()			
			

		def update(self, new_value):
			'''
			write crumb to filesystem
			'''
			fhand = open(self.crumb.fs_full,"w")
			fhand.write(new_value)
			# set new self.crumb 
			self.crumb.value = new_value
			fhand.close()
			logging.debug("successful update key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
			


		def delete(self):
			'''
			delete crumb from filesystem
			'''
			
			# delete crumb file
			os.remove(self.crumb.fs_full)

			# if l2 empty, remove
			if os.listdir(localConfig.fs_root+self.crumb.dir_l1+self.crumb.dir_l2) == []:
				logging.debug("l2 dir empty, removing")
				os.rmdir(localConfig.fs_root+self.crumb.dir_l1+self.crumb.dir_l2)

			# if l1 empty, remove
			if os.listdir(localConfig.fs_root+self.crumb.dir_l1) == []:
				logging.debug("l1 dir empty, removing")
				os.rmdir(localConfig.fs_root+self.crumb.dir_l1)
			
			



