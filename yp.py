#!/user/bin/env python3
"""
	Yakuake profile builder
"""

import yaml
import subprocess
import sys
import yakuakeInterface

from pprint import pprint

def handleSplit(originId, splitConfig):
	primaryType = 'left' if 'left' in splitConfig else 'top'
	nextConfig  = splitConfig[primaryType]
	
	if primaryType == 'left':
		newId = yakuakeInterface.splitTerminalVertically(originId)
	else:
		newId = yakuakeInterface.splitTerminalHorizontally(originId)
	
	if isinstance(nextConfig, dict):
		handleSplit(originId, nextConfig)
	else:
		runCommands(originId, nextConfig)		

	secondaryType = 'right' if primaryType == 'left' else 'bottom'
	nextConfig    = splitConfig[secondaryType]
	if isinstance(nextConfig, dict):
		handleSplit(newId, nextConfig)
	else:
		runCommands(newId, nextConfig)


def runCommands(termId, commandList):
	for command in commandList:
			yakuakeInterface.sendCommand(termId, command)


def main():
	with open("config.yaml", 'r') as stream:
	    try:
	        configData = yaml.safe_load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)

	for tabName, tabConfig in configData['tabs'].items():
		termId = yakuakeInterface.createSession(tabName)

		if type(tabConfig) is dict:
			splitTermId = handleSplit(termId, tabConfig)
		else:
			runCommands(termId, tabConfig)

# Main body
if __name__ == '__main__':
    main()