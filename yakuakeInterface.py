import subprocess
from pprint import pprint

def createSession(title):
	newSessionId = instruct(['/yakuake/sessions', 'org.kde.yakuake.addSession'])
	setSessionTitle(newSessionId, title)

	return getTerminalListForSession(newSessionId)[0]

def removeSessions(sessionId):
	instruct(['/yakuake/sessions', 'removeSession', sessionId])

def sendCommand(sessionId, command):
	instruct(['/yakuake/sessions', 'runCommandInTerminal', str(sessionId), command])

def setSessionTitle(sessionId, title):
	instruct(['/yakuake/tabs', 'org.kde.yakuake.setTabTitle', sessionId, title])

def startEmulatorIfNotStarted():
	instruct(['/yakuake/sessions', 'org.freedesktop.DBus.Peer.Ping'])

#
# Splitting
#

def splitSessionVertically(sessionId):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.splitSessionLeftRight', 
			str(sessionId)
		])
	return int(id) # ID of new terminal


def splitSessionHorizontally(sessionId):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.splitSessionTopBottom', 
			str(sessionId)
		])
	return int(id) # ID of new terinal

def splitTerminalVertically(terminalId):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.splitTerminalLeftRight', 
			str(terminalId)
		])
	return int(id) # ID of new terminal


def splitTerminalHorizontally(terminalId):
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
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalBottom', 
			str(terminalId),
			str(pixels)
		])
	return int(id) # Reports how much it actually grew

def growTerminalTop(terminalId, pixels):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalTop', 
			str(terminalId),
			str(pixels)
		])
	return int(id) # Reports how much it actually grew

def growTerminalLeft(terminalId, pixels):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalLeft', 
			str(terminalId),
			str(pixels)
		])
	return int(id) # Reports how much it actually grew

def growTerminalRight(terminalId, pixels):
	id = instruct([
			'/yakuake/sessions', 
			'org.kde.yakuake.tryGrowTerminalRight', 
			str(terminalId),
			str(pixels)
		])
	return int(id) # Reports how much it actually grew

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
	# pprint("RUNNING INSTRUCT")
	cmd = ['qdbus', 'org.kde.yakuake'] + cmd
	# pprint(cmd)
	data = subprocess.check_output(cmd)
	# pprint("Got command results");
	# pprint(data)
	return str(data, 'utf-8').strip()
