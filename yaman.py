#!/user/bin/env python3
"""yaman - Terminal Manager"""

import os
import click
import yaml
from inc.sessionBuilder import SessionBuilder
from inc.sessionManager import SessionManager

from pprint import pprint
import sys

APP_NAME = 'yaman'

manager = SessionManager(click.get_app_dir(APP_NAME))

DEFAULT_CONFIG_PATH = manager.getConfigPath()

@click.group()
def cli():
	"""yaman cli"""
	pass

@cli.command()
@click.option('--path', default=DEFAULT_CONFIG_PATH, help='If not specified default system path will be used.')
@click.argument('profile_name')
def open(path, profile_name):
	"""Executes a profile configuration file and creates terminals, runs scripts"""
	configData = loadConfigOrError(path, profile_name)
	builder = SessionBuilder(configData)

	idList = builder.buildFromConfig(configData)
	manager.saveToSessionFile(idList)


@cli.command()
@click.option('--path', default=DEFAULT_CONFIG_PATH, help='If not specified default system path will be used.')
@click.argument('profile_name')
def close(path, profile_name):
	"""Closes a previously started profile"""
	configData = loadConfigOrError(path, profile_name)
	builder = SessionBuilder(configData)

	idList = manager.getFromSessionFile()
	builder.runPreCloseCommands(configData)
	for sid in idList:
		builder.removeSession(sid)
	manager.removeSessionFile()


@cli.command()
@click.option('--path', default=DEFAULT_CONFIG_PATH, help='If not specified default system path will be used.')
@click.argument('profile_name')
def switch(path, profile_name):
	"""Closes a previously opened profile and starts the specified one"""
	configData = loadConfigOrError(path, profile_name)
	builder = SessionBuilder(configData)

	idList = manager.getFromSessionFile()
	builder.runPreCloseCommands(configData)
	for sid in idList:
		builder.removeSession(sid)
	manager.removeSessionFile()

	idList = builder.buildFromConfig(configData)
	manager.saveToSessionFile(idList)

@cli.command()
@click.option('-t', '--template', default=False, help='Use exsisting profile as template.')
@click.argument('profile_name')
def create(template, profile_name):
	"""Creates a new profile configuration file - empty or from an exsisting file"""
	if template == False:
		with open('./template.yaml', 'r') as stream:
			templateData = stream.read()
	else:
		template = manager.getConfigPath() + '/' + template + '.yaml'
		with open(template, 'r') as stream:
			try:
				templateData = stream.read()
			except FileNotFoundError as err:
				click.echo(click.style('Template config file not found!', fg='red'))
				sys.exit()

	newConfig = click.edit(templateData)
	if newConfig is not None:
		configFile = manager.getConfigPath() + '/' + profile_name + '.yaml'
		with open(configFile, 'a') as stream:
			stream.write(newConfig)
	else:
		click.echo("You did not seem to have created a config file - aborting.")

@cli.command()
@click.argument('profile_name')
def edit(profile_name):
	"""Opens the profiles configuration file in the default editor"""
	configFile = manager.getConfigPath() + '/' + profile_name + '.yaml'
	click.edit(filename=configFile)

@cli.command()
@click.option('--path', default=DEFAULT_CONFIG_PATH, help='If not specified default system path will be used.')
def list(path):
	"""List all profiles"""
	profiles = manager.getSessionFiles(path)
	for profile in profiles:
		click.echo(profile)

@cli.command()
def show_path():
	"""Display the default path for configuration files"""
	path = click.get_app_dir(APP_NAME)
	click.echo(click.format_filename(path))

cli.add_command(open)
cli.add_command(close)
cli.add_command(switch)
cli.add_command(create)
cli.add_command(edit)
cli.add_command(list)
cli.add_command(show_path)


def loadConfigOrError(path, profile_name):
	try:
		configData = manager.loadConfig(path, profile_name)
	except yaml.YAMLError as err:
		click.echo(click.style('Session configuration is not valid yaml: {}'.format(err), fg='red'))
		sys.exit()
	except FileNotFoundError as err:
		click.echo(click.style('Session configuration not found!', fg='red'))
		sys.exit()

	return configData