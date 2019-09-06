#!/user/bin/env python3
"""
	Yakuake profile builder
"""

import yaml
import subprocess
import sys
import os
import yakuakeInterface

from pprint import pprint

# @TODO this should not be a global variable!
replacementVariables = {}

def handleReplacementVariables(string):
	global replacementVariables
	for varName, varValue in replacementVariables.items():
		string = string.replace('%'+varName+'%', varValue)
	return string

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
			yakuakeInterface.sendCommand(termId, handleReplacementVariables(command))

def main():
	with open("config.yaml", 'r') as stream:
	    try:
	        configData = yaml.safe_load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)
	
	if configData['variables']:
		global replacementVariables 
		replacementVariables = configData['variables'] 

	if configData['pre']:
		for preCommand in configData['pre']:
			cmd = handleReplacementVariables(preCommand)
			os.system(cmd)

	for tabName, tabConfig in configData['tabs'].items():
		termId = yakuakeInterface.createSession(tabName)

		if type(tabConfig) is dict:
			splitTermId = handleSplit(termId, tabConfig)
		else:
			runCommands(termId, tabConfig)

# Main body
if __name__ == '__main__':
    main()