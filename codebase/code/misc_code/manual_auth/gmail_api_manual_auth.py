#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Manually authenticate (Gmail API)
# Date:        August 2017
# Language:    Python (.py) [Python 2.7]

#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Path
import os, sys
app_root =  os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","..","..")))
print(app_root)

# Dependencies - External
#---------------------------------------------#
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init__ import *

# Control Parameters [DEFAULT SETTINGS]
#--------------------------------#

# oauth2 settings
api_auth_file = os.path.normpath(os.path.join(app_root,'code', 'app', 'static','auth','client_secret_manual.json'))
api_auth_scope = ['https://www.googleapis.com/auth/gmail.readonly','profile','https://www.googleapis.com/auth/contacts.readonly']
application_name = "KnowingMe"

#----------------------------------------------------------------------------#
#				                  Code                                       #
#----------------------------------------------------------------------------#

# Function definition
#--------------------------------------------

## get_credentials
def get_credentials():
	
	"""Load user credentials (if stored) otherwise create new credentials (OAuth2).
	Returns:
		credentials, the obtained credential.
	"""
	
	## Initialise
	try:
	
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
		flags = None

	## Check if credentials stored in system (i.e. previously authenticated)
	home_dir  = os.path.expanduser('~')
	credential_dir = os.path.normpath(os.path.join(home_dir, '.credentials'))
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	application_json = application_name + ".json"
	credential_path = os.path.normpath(os.path.join(credential_dir, application_json))

	store = Storage(credential_path)
	credentials = store.get()

	print('Using preexisting credentials')

	## No preexisting credentials - new authentication
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(api_auth_file, api_auth_scope)
		flow.user_agent = application_name
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # (Python 2.6 compatibility)
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

## log_in
def log_in():
	
	"""Obtain/generate credentials and establish connection.
	Returns:
		service, the generated connection object.
	"""

	## Obtain/generate credentials
	credentials = get_credentials()
	
	## Connect & generate service object
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	print('Successfully authenticated & service created')
	return(service)


## get_user
def get_user(service):
	
	"""Return the email address of the authenticated user.
	Returns:
		user, the user's email address.
	"""

	## Obtain/generate credentials
	user = service.users().getProfile(userId='me').execute()['emailAddress']
	
	return(user)

# function execution
#--------------------------------------------
service=log_in()
user=get_user(service)
user_id='me'

#----------------------------------------------------------------------------#
#				                   End                                       #
#----------------------------------------------------------------------------#


