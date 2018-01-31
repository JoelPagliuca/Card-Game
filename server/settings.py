"""
Server config
Environment variables
	DEPLOYMENT_TYPE
	SERVER_COOKIE_SECRET
"""
import os
import logging

import tornado
from tornado.options import define, options

# read in options from command line
define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
tornado.options.parse_command_line()

# environment
class DeploymentType:
	PRODUCTION = "PRODUCTION"
	DEV = "DEV"
	STAGING = "STAGING"
	dict = {
		PRODUCTION: 1,
		DEV: 2,
		STAGING: 3
	}

# get deployment type from environment
if 'DEPLOYMENT_TYPE' in os.environ:
	DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
	DEPLOYMENT = DeploymentType.DEV

# settings for the server
settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
if 'SERVER_COOKIE_SECRET' in os.environ:
	settings['cookie_secret'] = os.environ['SERVER_COOKIE_SECRET']
else:
	settings['cookie_secret'] = "demo-cookie-secret"
settings['xsrf_cookies'] = True
# set up correct logging
if DEPLOYMENT == DeploymentType.DEV:
	logging.getLogger().setLevel(logging.DEBUG)

if options.config:
	tornado.options.parse_config_file(options.config)
