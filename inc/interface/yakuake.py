import subprocess

"""Yakuake interface

Used as a template interface - if you wish to implement an interface
for your own terminal you must implement all the REQUIRED functions.
"""


def createSession(title):
	"""REQUIRED: Creates a new TAB/session
	
	Arguments:
		title {string} -- The label of the tabs
	
	Returns:
		tuple -- The terminal ID identifiying this specific terminal and 
				 the session ID (used for session removal on profile change)!
	"""
	newSessionId = instruct(['/yakuake/sessions', 'org.kde.yakuake.addSession'])
	setSessionTitle(newSessionId, title)
	return getTerminalListForSession(newSessionId)[0], newSessionId

def removeSession(sessionId):
	"""REQUIRED: Removes TAB/session
	
	Arguments:
		sessionId {integer} -- ID of tab/session, not terminal
	"""
	instruct(['/yakuake/sessions', 'removeSession', sessionId])

def sendCommand(termId, command):
	"""REQUIRED: Sends a command to a terminal
	
	Arguments:
		termId {integer} -- ID of terminal to run the command, not TAB!
		command {string}
	"""
	instruct(['/yakuake/sessions', 'runCommandInTerminal', str(termId), command])

def setSessionTitle(sessionId, title):
	instruct(['/yakuake/tabs', 'org.kde.yakuake.setTabTitle', sessionId, title])

def startEmulatorIfNotStarted():
	"""REQUIRED: Starts the terminal emulator
	"""
	instruct(['/yakuake/sessions', 'org.freedesktop.DBus.Peer.Ping'])

#
# Splitting
#

def splitTerminalVertically(terminalId):
	"""REQUIRED: Splits a TERMINAL (not tab) vertically
	
	Arguments:
		terminalId {integer}
	
	Returns:
		integer -- ID of new terminal
	"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.splitTerminalLeftRight', 
			str(terminalId)
		])
	return int(id) # ID of new terminal


def splitTerminalHorizontally(terminalId):
	"""REQUIRED: Splits a TERMINAL (not tab) horizontally
	
	Arguments:
		terminalId {integer}
	
	Returns:
		integer -- ID of new terminal
	"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.splitTerminalTopBottom', 
			str(terminalId)
		])
	return int(id) # ID of new terinal

#
# Terminal growing
#

def growTerminalBottom(terminalId, pixels):
	"""REQUIRED: Grow terminal"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalBottom', 
			str(terminalId),
			str(pixels)
		])

def growTerminalTop(terminalId, pixels):
	"""REQUIRED: Grow terminal"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalTop', 
			str(terminalId),
			str(pixels)
		])

def growTerminalLeft(terminalId, pixels):
	"""REQUIRED: Grow terminal"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalLeft', 
			str(terminalId),
			str(pixels)
		])

def growTerminalRight(terminalId, pixels):
	"""REQUIRED: Grow terminal"""
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalRight', 
			str(terminalId),
			str(pixels)
		])

#
# Getters
#

def getSessionList():
	return instruct(['/yakuake/sessions', 'sessionIdList']).split(',')

def getTerminalList():
	return instruct(['/yakuake/sessions', 'terminalIdList']).split(',')

def getTerminalListForSession(sessionId):
	data = instruct(['/yakuake/sessions', 'terminalIdsForSessionId', sessionId])
	return data.split(',')


#
# Utility
#

def instruct(cmd):
	cmd = ['qdbus', 'org.kde.yakuake'] + cmd
	data = subprocess.check_output(cmd)
	return str(data, 'utf-8').strip()
