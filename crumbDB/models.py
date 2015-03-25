# models for crumbDB

#python modules
import md5
import logging
import os

#crumb modules
import localConfig
import utilities
from utilities import crumb_lock


class Crumb(object):
	
	'''
	Class for individual crumb.
		- defines, writes, updates, deletes

	Crumb can be instatiated with key AND value, or just key for updating / get / delete

	Considered "DB" class for direct access, but so much would be duplicate figuring from this class.
	So creating optional flag, "DBdirect", that bypasses Rollback features, for minimal i/o processes.
	'''

	@utilities.timing
	def __init__(self, key, value=False, index='default', DBdirect=False):



		# convert both to string
		key = str(key)
		if value != False:
			value = str(value)

		# derive id from key
		self.id = md5.new(key).hexdigest()
		self.index = str(index)
		self.crumb_lock_id = self.index+"|"+self.id

		# set key and value
		self.key = key		
		self.value = value

		# derive fs location
		self.dir_l1 = self.index+"/"+self.id[0:2]+"/"
		self.dir_full = localConfig.fs_root+self.dir_l1
		self.fs_full = self.dir_full+self.id

		# check if exists
		if os.path.exists(self.fs_full) == True:
			self.exists = True
		else:
			self.exists = False

		# instantiate rollback object before IO methods created
		if DBdirect == False:
			self.rollback = Rollback(self)

		# group main IO methods
		self.io = self.IO(self)



	# release crumb_lock
	def release_crumb_lock(self):
		logging.info("releasing {crumb_lock_id}".format(crumb_lock_id=self.crumb_lock_id))
		crumb_lock.discard(self.crumb_lock_id)
		return True
	


	class IO(object):

		def __init__(self, crumb):			
			#pass main crumb self (all values same with 'self.crumb' prefix)
			self.crumb = crumb

		@utilities.crumbLockDec
		@utilities.timing
		def write(self):
			'''
			write crumb to filesystem
			'''		
			# make sure has key
			if self.crumb.key == None:
				logging.info("crumb does not have a key, aborting write")
				raise Exception("no key provided")

			# check first if exists, then suggest update
			if self.crumb.exists == True:
				logging.info("crumb exists, consider using update() method")
				raise IOError("crumb exists")

			# check level 1, create if neccessary
			if os.path.exists(self.crumb.dir_full) == False:
				logging.debug("creating l1 dir {l1}".format(l1=self.crumb.dir_l1))
				os.makedirs(self.crumb.dir_full)			
			
			# write crumb file
			fhand = open(self.crumb.fs_full,"w")
			fhand.write(self.crumb.value)
			fhand.close()
			logging.info("successful write key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
			return True		
			


		@utilities.crumbLockDec
		@utilities.timing
		def get(self):
			'''
			retrieve crumb from filesystem
			'''
			# get and retrieve
			if self.crumb.exists == True:
				fhand = open(self.crumb.fs_full,"r")
				# set to self.crumb
				self.crumb.value = fhand.read()
				fhand.close()
				logging.info("successful get key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
				return self.crumb.value

			else:
				raise IOError("crumb does not exist")
			
			
			
		@utilities.crumbLockDec
		@utilities.timing
		def update(self):
			'''
			write crumb to filesystem
			'''
			if self.crumb.exists == True:
				fhand = open(self.crumb.fs_full,"w")				
				fhand.write(self.crumb.value)
				fhand.close()
				logging.info("successful update key: {key} @ location: {fs_full}".format(key=self.crumb.key,fs_full=self.crumb.fs_full))
				return True
			else:
				raise IOError("crumb does not exist")



		@utilities.crumbLockDec
		@utilities.timing
		def delete(self):
			'''
			delete crumb from filesystem
			'''
			if self.crumb.exists == True:
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
				

