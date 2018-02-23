# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         gmail_api_authentication_mod
# Purpose:      Module - Define gmail api authentication functions
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialization
# ------------------------------------------------------------------------ #

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *
from __init_setting__ import *

#----------------------------------------------------------------------------#
#			                     Functions                                   #
#----------------------------------------------------------------------------#

# gmail_authentication
#---------------------------------------------#
def gmail_authentication():

	try: 
		if 'credentials' not in flask.session:
			return("logged_out", [])
		credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
		if credentials.access_token_expired:
			return("logged_out", [])
		else:

			http_auth      = credentials.authorize(httplib2.Http())
			service        = discovery.build('gmail', 'v1', http=http_auth)
			service_people = discovery.build('people', 'v1', http=http_auth)
			user           = service.users().getProfile(userId='me').execute()['emailAddress']
			user_name      = service_people.people().get(resourceName="people/me",personFields='names').execute()['names'][0]['givenName']
			user_photo     = service_people.people().get(resourceName="people/me",personFields='photos').execute()['photos']
			user_photo      = [x['url'] for x in user_photo]
			
			if len(user_photo)>0:
				user_photo_temp = [x for x in user_photo if bool(re.match('.*AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M.*',x))==False]
				if len(user_photo_temp)==0:
					user_photo = user_photo[0]
				else:
					user_photo = user_photo_temp[0]
			else:
				user_photo = user_photo[0]
		
			return("logged_in", dict(service=service, user=user, user_name=user_name, user_photo=user_photo))

	except Exception as e: 
	
			return("error", [e])


# gmail_oauth2callback
#---------------------------------------------#
def gmail_oauth2callback():

	flow = client.flow_from_clientsecrets(
	api_auth_file,
	scope=api_auth_scope,
	redirect_uri=flask.url_for('gmail_oauth2callback_view', _external=True))
	if 'code' not in flask.request.args:
		auth_url = flow.step1_get_authorize_url()
		return ('unauthenticated', [auth_url])
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return ('authenticated', [])

# gmail_reauthentication
#---------------------------------------------#
def gmail_reauthentication():

	try:
		credentials    = client.OAuth2Credentials.from_json(flask.session['credentials'])
		http_auth      = credentials.authorize(httplib2.Http())
		service        = discovery.build('gmail', 'v1', http=http_auth)
		service_people = discovery.build('people', 'v1', http=http_auth)
		user           = service.users().getProfile(userId='me').execute()['emailAddress']
		
		return("logged_in", dict(service=service, user=user))

	except Exception as e: 
	
		return("error", [e])

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

