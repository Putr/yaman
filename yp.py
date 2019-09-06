#!/user/bin/env python3
"""
	Yakuake profile builder
"""

import yaml
from inc.sessionBuilder import SessionBuilder

from pprint import pprint

def main():
	with open("config.yaml", 'r') as stream:
	    try:
	        configData = yaml.safe_load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)

	builder = SessionBuilder()
	builder.buildFromConfig(configData)	
	

# Main body
if __name__ == '__main__':
    main()