import sys
import os
import yaml

class SessionManager:

	sessionPath = ''

	def __init__(self, path):
		self.sessionPath = path
		self.createConfigFolders()

	def getSessionFilepath(self):
		return os.path.join(self.sessionPath, 'session_open')

	def getConfigPath(self):
		return os.path.join(self.sessionPath, 'sessions')

	def createConfigFolders(self):
		profile_path = self.sessionPath + '/sessions'
		if not os.path.exists(self.sessionPath):
			os.makedirs(self.sessionPath)
		if not os.path.exists(profile_path):
			os.makedirs(profile_path)

	def getSessionFiles(self, path):
		files = os.listdir(path)
		return [file.replace('.yaml', '') for file in files]


	def getSessionFile(self, readOnly=False):
		sessionFile = self.getSessionFilepath()
		
		openMode = 'r'
		if not readOnly:
			openMode = 'w+'
			if os.path.isfile(sessionFile):
				openMode = 'a+'

		return open(sessionFile, openMode), openMode;

	def saveToSessionFile(self, idList):
		sessionFile, openMode = self.getSessionFile()
		data = ','.join(str(val) for key,val in idList.items())
		if data and openMode == 'a+':
			data = ',' + data
		sessionFile.write(data)	

	def getFromSessionFile(self):
		sessionFile, openMode = self.getSessionFile(readOnly=True)
		return sessionFile.read().split(',')

	def removeSessionFile(self):
		os.remove(self.getSessionFilepath())

	def loadConfig(self, path, profile_name):
		with open(os.path.join(path, profile_name + '.yaml'), 'r') as stream:
			configData = yaml.safe_load(stream)
			return configData

