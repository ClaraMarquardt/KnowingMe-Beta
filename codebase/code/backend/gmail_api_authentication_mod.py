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
def gmail_authentication(offline_mode, output_dir, current_date):

	try: 

		if (offline_mode==False):

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
		
		elif (offline_mode==True):

			offline_authentication_data = offline_authentication(output_dir=output_dir, reauthenticate=False, current_date=current_date)

			return(offline_authentication_data)
	
	except Exception as e: 
	
			return("error", [e])


# gmail_oauth2callback
#---------------------------------------------#
def gmail_oauth2callback(offline_mode):

	if (offline_mode==False):

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

	elif (offline_mode==True):

		return ('authenticated', [])


# gmail_reauthentication
#---------------------------------------------#
def gmail_reauthentication(offline_mode, output_dir, current_date):

	try:

		if (offline_mode==False):
			
			credentials    = client.OAuth2Credentials.from_json(flask.session['credentials'])
			http_auth      = credentials.authorize(httplib2.Http())
			service        = discovery.build('gmail', 'v1', http=http_auth)
			service_people = discovery.build('people', 'v1', http=http_auth)
			user           = service.users().getProfile(userId='me').execute()['emailAddress']
			
			return("logged_in", dict(service=service, user=user))

		elif (offline_mode==True):

			offline_authentication_data = offline_authentication(output_dir=output_dir, reauthenticate=True, current_date=current_date)
			
			return(offline_authentication_data)

	except Exception as e: 
	
		return("error", [e])


# offline_authentication
#---------------------------------------------#
def offline_authentication(output_dir, reauthenticate, current_date):

	try:

		offline_authentication_check(output_dir, current_date)

		# determine existing user
		existing_user           = [re.sub("(.*)/([^/]*)","\\2", x) for x in glob.glob(os.path.join(output_dir, '*'))]

		# set offline parameters
		user_offline            = existing_user[0]
		service_offline 		= "offline_service"
		user_name_offline       = "Offline User"
		user_photo_offline      = ""

		if (reauthenticate==True):
		
			return("logged_in", dict(service=service_offline, user=user_offline))
		
		else:

			return("logged_in", dict(service=service_offline, user=user_offline, user_name=user_name_offline, user_photo=user_photo_offline))
	
	except Exception as e: 
	
		return("error", [e])


# offline_authentication_check
#---------------------------------------------#
def offline_authentication_check(output_dir, current_date):

	# determine if existing user
	existing_user     = [re.sub("(.*)/([^/]*)","\\2", x) for x in glob.glob(os.path.join(output_dir, '*'))]
	 
	# determine if current overview/birthday
	current_overview  = os.path.exists(os.path.join(output_dir, existing_user[0], 'other', 'overview_'+datetime.datetime.strptime(current_date,"%m/%d/%Y").strftime("%m_%d_%Y")+'.p'))
	current_birthday  = os.path.exists(os.path.join(output_dir, existing_user[0],'other', 'birthday_'+datetime.datetime.strptime(current_date,"%m/%d/%Y").strftime("%m_%d_%Y")+'.p'))

	# determine if at least some emails (50 days before)
	pre_date          = (datetime.datetime.strptime(current_date,'%m/%d/%Y') - datetime.timedelta(days=50)).strftime("%m_%d_%Y")
	email_array       = np.concatenate((glob.glob(os.path.join(output_dir,existing_user[0],'inbox', 'email*.p')), 
		glob.glob(os.path.join(output_dir,existing_user[0],'outbox', 'email*.p'))))
	email_array       = [x for x in email_array if bool(re.search(pre_date,x))==True]

	if (len(existing_user)==0):

		offline_error = "Offline mode - Need to have previously logged in online."
		flask.flash(offline_error)

	elif (current_overview==False | current_birthday==False):

		offline_error = "Offline mode - Need to have previously generated overview files."
		flask.flash(offline_error)

	elif (len(email_array)==0):

		offline_error = "Offline mode - Need to have previously downloaded emails."
		flask.flash(offline_error)


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

