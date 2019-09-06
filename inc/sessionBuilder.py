import subprocess
import sys
import os

class SessionBuilder:

	terminalInterface = None
	replacementVariables = {}
	sessions = {}

	def buildFromConfig(self, configData):
		if 'terminal' in configData:
			if configData['terminal'] == 'yakuake':
				from inc.interface import yakuake  as terminalInterface
			elif configData['terminal'] == 'guake':
				from inc.interface import guake as terminalInterface 
			else:
				raise NotImplementedError('This terminal is not yet supported!')
		else:
			raise Exception('Terminal type not set in configuration!')

		self.terminalInterface = terminalInterface

		if configData['variables']:
			self.replacementVariables = configData['variables'] 

		if configData['pre']:
			for preCommand in configData['pre']:
				cmd = self.handleReplacementVariables(preCommand)
				os.system(cmd)

		for tabName, tabConfig in configData['tabs'].items():
			termId, sessionId = self.terminalInterface.createSession(tabName)
			self.sessions[tabName] = sessionId
			if type(tabConfig) is dict:
				splitTermId = self.handleSplit(termId, tabConfig)
			else:
				self.runCommands(termId, tabConfig)

	def handleReplacementVariables(self, string):
		for varName, varValue in self.replacementVariables.items():
			string = string.replace('%'+varName+'%', varValue)
		return string

	def handleSplit(self, originId, splitConfig):
		primaryType = 'left' if 'left' in splitConfig else 'top'
		nextConfig  = splitConfig[primaryType]
		
		if primaryType == 'left':
			newId = self.terminalInterface.splitTerminalVertically(originId)
		else:
			newId = self.terminalInterface.splitTerminalHorizontally(originId)
		
		if isinstance(nextConfig, dict):
			self.handleSplit(originId, nextConfig)
		else:
			self.runCommands(originId, nextConfig)		

		secondaryType = 'right' if primaryType == 'left' else 'bottom'
		nextConfig    = splitConfig[secondaryType]
		if isinstance(nextConfig, dict):
			self.handleSplit(newId, nextConfig)
		else:
			self.runCommands(newId, nextConfig)

	def runCommands(self, termId, commandList):
		for command in commandList:
				self.terminalInterface.sendCommand(termId, self.handleReplacementVariables(command))
