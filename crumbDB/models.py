# models for crumbDB

#python modules
import md5
import logging
import os

#crumb modules
import localConfig
import utilities


class Crumb(object):
	'''
	Class for individual crumb.
		- defines, writes, updates, deletes

	Crumb can be instatiated with key AND value, or just key for updating / get / delete
	'''

	@utilities.timing
	def __init__(self, key, value=False, index='def'):

		# convert both to string
		key = str(key)
		if value != False:
			value = str(value)

		#derive id from key
		self.id = md5.new(key).hexdigest()
		self.key = key		
		self.value = value
		self.index = index

		# derive fs location
		self.dir_l1 = self.id[0:2]+"/"
		self.dir_full = localConfig.fs_root+self.dir_l1
		self.fs_full = self.dir_full+self.id

		# instantiate rollback object before IO methods created
		self.rollback = Rollback(self)

		# group main IO methods
		self.io = self.IO(self)



	class IO(object):

		def __init__(self, crumb):			
			#pass main crumb self (all values same with 'self.crumb' prefix)
			self.crumb = crumb


		@utilities.timing
		def write(self):
			'''
			write crumb to filesystem
			'''			

			# check first if exists, then suggest update
			if os.path.exists(self.crumb.fs_full) == True:
				logging.info("crumb exists, consider using update() method")
				raise IOError("crumb exists")

			# check level 1, create if neccessary
			if os.path.exists(localConfig.fs_root+self.crumb.dir_l1) == False:
				logging.debug("creating l1 dir {l1}".format(l1=self.crumb.dir_l1))
				os.makedirs(localConfig.fs_root+self.crumb.dir_l1)			
			
			# write crumb file
			fhand = open(self.crumb.fs_full,"w")
			fhand.write(self.crumb.value)
			fhand.close()
			logging.info("successful write key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
			return True		
			


		@utilities.timing
		def get(self):
			'''
			retrieve crumb from filesystem
			'''
			# get and retrieve
			if os.path.exists(self.crumb.fs_full) == True:
				fhand = open(self.crumb.fs_full,"r")
				# set to self.crumb
				self.crumb.value = fhand.read()
				fhand.close()
				logging.info("successful get key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
				return self.crumb.value

			else:
				raise IOError("crumb does not exist")
			
			
			

		@utilities.timing
		def update(self, new_value):
			'''
			write crumb to filesystem
			'''
			if os.path.exists(self.crumb.fs_full) == True:
				fhand = open(self.crumb.fs_full,"w")				
				fhand.write(new_value)
				# set new self.crumb 
				self.crumb.value = new_value
				fhand.close()
				logging.info("successful update key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
				return True
			else:
				raise IOError("crumb does not exist")



		@utilities.timing
		def delete(self):
			'''
			delete crumb from filesystem
			'''
			if os.path.exists(self.crumb.fs_full) == True:
				# delete crumb file
				os.remove(self.crumb.fs_full)
				# cleanup dirs (this is why Rollback might not good name)
				self.crumb.rollback.rollback_dir_creation()			
				logging.info("successful crumb deletion: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
				return True
			else:
				raise IOError("crumb does not exist")
			


class Rollback(object):
	'''
	Rollback class is a wrapper for functions and data for each crumb transaction, crumb passed as argument
	'''

	@utilities.timing
	def __init__(self, crumb):
		# pull in values from crumb
		self.__dict__.update(crumb.__dict__)


	@utilities.timing
	def rollback_dir_creation(self):
		# if l1 empty, remove
		l1_full = localConfig.fs_root+self.dir_l1
		if os.path.exists(l1_full) and os.listdir(l1_full) == []:
			logging.debug("l1 dir empty, removing")
			os.rmdir(l1_full)
				




class CrumbDB(object):
	'''
	Consider raw methods to write / get, etc. from here
	'''
	pass