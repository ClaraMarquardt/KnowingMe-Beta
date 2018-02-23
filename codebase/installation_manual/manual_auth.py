#----------------------------------------------------------------------------#
# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         manual_auth
# Purpose:      Manually authenticate gmail api (oauth2)
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialisation
# ------------------------------------------------------------------------ #

# Path
import os, sys
app_root =  os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","..","..")))

# Dependencies
sys.path.append(os.path.normpath(os.path.join(app_root, "initialization")))
from __init_setting__ import *

#----------------------------------------------------------------------------#
# Authentication Functions				                 
#----------------------------------------------------------------------------#

# get_credentials
#---------------------------------------------#
def get_credentials():
	
	# Initialise
	try:
	
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
		flags = None

	# Check if credentials stored in system (i.e. previously authenticated)
	home_dir  = os.path.expanduser('~')
	credential_dir = os.path.normpath(os.path.join(home_dir, '.credentials'))
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	application_json = application_name + ".json"
	credential_path = os.path.normpath(os.path.join(credential_dir, application_json))

	store = Storage(credential_path)
	credentials = store.get()

	print('Using preexisting credentials')

	# No preexisting credentials - new authentication
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(api_auth_file, api_auth_scope)
		flow.user_agent = application_name
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: 
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

# log_in
#---------------------------------------------#
def log_in():
	
	# Obtain/generate credentials
	credentials = get_credentials()
	
	# Connect & generate service object
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	print('Successfully authenticated & service created')
	return(service)


# get_user
#---------------------------------------------#
def get_user(service):

	# Obtain/generate credentials
	user = service.users().getProfile(userId='me').execute()['emailAddress']
	
	return(user)

#----------------------------------------------------------------------------#
# Authenticate			                 
#----------------------------------------------------------------------------#
service = log_in()
user    = get_user(service)
user_id = 'me'

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#


