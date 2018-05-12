# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         KnowingMe
# Purpose:      Flask App Structure
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
app_root = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))   
print(app_root)

# Initialize 
sys.path.append(os.path.normpath(os.path.join(app_root,'initialization')))
from __init_lib__ import *
from __init_global__ import *
from __init_setting__ import *

# Dependency settings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Initialize globals
global app_setting, insight_meta_data, insight_text, insight_title

app_setting                                    		= app_setting_initialization()
insight_meta_data, insight_text, insight_title      = insight_meta_initialization()

# Initialize authentication variables
global username, password, app_auth_data

username, password, app_auth_data 			= auth_initialization()


# ------------------------------------------------------------------------ #
# Initialization - Internal Dependencies
# ------------------------------------------------------------------------ #

## app init functions 
sys.path.append(os.path.normpath(os.path.join(app_root,'code','app_setup')))
from app_init_mod import flask_initialize

## backend functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'backend')))
from gmail_api_mod import get_email, overview_email, timeframe_email, get_diff_range
from gmail_api_authentication_mod import gmail_oauth2callback, gmail_authentication, gmail_reauthentication

## analysis functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'analysis')))
from analysis_mod import analysis
from analysis_wrapper_mod import analysis_wrapper
from analysis_helper import *

## frontend functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'frontend')))
from frontend_insight import *
from frontend_feature import *

## global functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
# Initialization - Servers & App
#----------------------------------------------------------------------------#

## server/browser initialization
if (((os.environ.get("WERKZEUG_RUN_MAIN")==False) or (pd.isnull(os.environ.get("WERKZEUG_RUN_MAIN")))) and (app_setting['app_debug']==True)):
	
	print("Launching")
	
else:

	print("Restarting")
	url = 'http://localhost:' + str(app_setting['app_port'])

	webbrowser.open_new(url)
	
## app initialization
print("Initializing")
app  = flask_initialize(debug=app_setting['app_debug'], secret_key=secret_key, 
	app_static=app_static, app_template=app_template)


## authentication initialization
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return app_auth_data.get(username) == password

# ------------------------------------------------------------------------ #
# Functions
# ------------------------------------------------------------------------ #

# reset
# ---------------------------------------------#
def reset(reset_user=True, session_id_old='', session_id_new=''):

	# define globals
	global global_var, setting_var

	# display reset message
	flask.flash('App Resetting ('+str(setting_var[session_id_old]['user_setting']['output_dir'])+') - OK?')
	
	# store old
	key_var_old                                                 = setting_var[session_id_old]['key_var']

	# redefine variables
	setting_var[session_id_new] 								= dict()
	global_var[session_id_new] 									= dict()

	setting_var[session_id_new]['user_setting']             	= user_setting_initialization(session_id_new)	
	setting_var[session_id_new]['key_var']      			    = var_initialization(reset_user=reset_user, key_var_old=key_var_old)	
	global_var[session_id_new]   			   					= global_initialization()
	
	# clear old user data
	user_data_dir_clear(setting_var[session_id_old]['user_setting']['output_dir'])
	# del setting_var[session_id_old]
	# del global_var[session_id_old]

	# display reset message
	flask.flash('App Successfully Reset.')


# access checks
# ---------------------------------------------#

# access_check
# --------------------------------#
def access_check(access_level, output_dir):

	if (access_level==0):

		## >> App initialized

		return(True)

	elif (access_level==1):

		## >> Authenticated

		return(True)

	elif (access_level==2):

		## >> Load_a completed (overview + timerange)

		return(True)

	elif (access_level==3):

		## >> Load_b completed (emails)

		return(True)

	elif (access_level==4):

		## >> Load_c completed (features, basic insights > ready for further insight generation)
		
		# perform lower level checks
		lower_level_check = []
		lower_level_check.append(access_check(access_level=0, output_dir=output_dir))
		lower_level_check.append(access_check(access_level=1, output_dir=output_dir))
		lower_level_check.append(access_check(access_level=2, output_dir=output_dir))
		lower_level_check.append(access_check(access_level=3, output_dir=output_dir))

		# define required objects
		min_object       = ['feature_data.p', 'insight_data.p']
		min_object_check = []

		# check existance of required objects
		for obj in min_object:
			if os.path.join(output_dir,'other', obj) in glob.glob(os.path.join(output_dir,'other/*')): 
				min_object_check.append(True)
			else: 
				min_object_check.append(False)

		# perform access check
		if (all(lower_level_check) and all(min_object_check)):
			
			return(True)

		else: 

			return(False)


# access_denied
# --------------------------------#
def access_denied():

	# update
	flask.flash("It looks like you tried to open a page that you are not authorized to access. You will now be redirected to the landing page.")

	# return page
	return_page = "landing_view"

	return(return_page)



# intro_load_wrapper
# ---------------------------------------------#

# intro_load_overview_wrapper
# --------------------------------#
def intro_load_overview_wrapper(session_id, offline_mode, service, user, current_date, timelag_day, timelag_overview, overview_day, birthday_day, email_max, min_day,output_dir,timezone_utc_offset,email_earliest_user, email_latest_user, email_diff_user, email_range_user, safe_mode):

	# define globals
	global global_var, setting_var

	# initialize
	setting_var[session_id]['key_var']['api_success'] = 'False'

	# launch process
	try: 
	
		if (offline_mode==False):	

			# email & birthday overview
			overview_email(session_id, service, user, current_date, timelag_overview, overview_day, birthday_day, output_dir, timezone_utc_offset, safe_mode)

		# determine analysis timeframe
		setting_var[session_id]['user_setting']['email_earliest'], setting_var[session_id]['user_setting']['email_latest'], setting_var[session_id]['user_setting']['email_diff'], setting_var[session_id]['user_setting']['email_range']  = timeframe_email(current_date, timelag_day, timelag_overview, min_day, overview_day, email_max, output_dir)

		# modify based on user settings
		if (pd.isnull(setting_var[session_id]['user_setting']['email_earliest_user'])==False):
			setting_var[session_id]['user_setting']['email_earliest'] = email_earliest_user
			setting_var[session_id]['user_setting']['email_latest']   = email_latest_user
			setting_var[session_id]['user_setting']['email_diff']     = email_diff_user
			setting_var[session_id]['user_setting']['email_range']    = email_range_user

		# update thread status
		setting_var[session_id]['key_var']['api_success'] = 'True'

	# error
	except Exception as e: 

		setting_var[session_id]['key_var']['error']       = e
		setting_var[session_id]['key_var']['error_msg']   = "Error Generating Email Overview > Try Restarting the App"
		setting_var[session_id]['key_var']['api_success'] = 'Error'

# intro_load_email_wrapper
# --------------------------------#
def intro_load_email_wrapper(session_id, offline_mode, service, user, email_range, output_dir, current_date, user_email, timezone_utc_offset, safe_mode):

	# define globals
	global global_var, setting_var

	# initialize
	setting_var[session_id]['key_var']['api_success'] = 'False'

	# launch process
	try: 
		
		if (offline_mode==False):	
		
			# emails
			get_email(session_id, service, user, email_range, output_dir, current_date, user_email, timezone_utc_offset, safe_mode)

		# update thread status
		setting_var[session_id]['key_var']['api_success'] = 'True'

	# error
	except Exception as e: 

		setting_var[session_id]['key_var']['error']       = e
		setting_var[session_id]['key_var']['error_msg']   = "Error Extracting Emails > Try Restarting the App"
		setting_var[session_id]['key_var']['api_success'] = 'Error'

# intro_load_analysis_wrapper
# --------------------------------#
def intro_load_analysis_wrapper(session_id, user, user_name, email_range, email_diff, output_dir, current_date, earliest_date, latest_date):

	# define globals
	global global_var, setting_var

	# initialize
	setting_var[session_id]['key_var']['api_success'] = 'False'

	# launch process
	try: 
			
		# obtain email lists
		email_range_list  = [str(datetime.datetime.strptime(x,'%m/%d/%Y').strftime('%m_%d_%Y')) for x in email_range]
		email_range_list  = string.join(email_range_list,"|")

		email_array       = np.concatenate((glob.glob(os.path.join(output_dir,'inbox', 'email*.p')), 
			glob.glob(os.path.join(output_dir,'outbox', 'email*.p'))))
		email_array       = [x for x in email_array if bool(re.search(email_range_list,x))==True]
	
		email_array_other = (glob.glob(os.path.join(output_dir,'other', '*.p')))
		email_array_other = [x for x in email_array_other if bool(re.search(datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime('%m_%d_%Y'),x))==True]
		email_array_other = [x for x in email_array_other if bool(re.search('birthday|overview',x))==True]

		if (len(email_array)==0):

			setting_var[session_id]['key_var']['error']         = "No emails to process - try restarting the app."
			setting_var[session_id]['key_var']['error_msg']     = "No emails to process - try restarting the app."


			return flask.redirect(flask.url_for('error_view'))

		else:
		

			# data preparation 
			# -----------------------
	
			## main data preparation
			feature_data         = analysis(session_id, email_array, user, output_dir, current_date, earliest_date, latest_date)
			
			## modify contact df (user settings)
			if (isinstance(setting_var[session_id]['key_var']['contact_group_user'], pd.DataFrame)):
				contact_df_user_relevant_filter = [x in np.array(feature_data['agg_contact_df']['contact']) for x in np.array(setting_var[session_id]['key_var']['contact_group_user']['contact'])]
				contact_df_user_relevant        = setting_var[session_id]['key_var']['contact_group_user'][contact_df_user_relevant_filter]
				if (len(contact_df_user_relevant)>0): 
					feature_data['agg_contact_df'] = pd.merge(feature_data['agg_contact_df'], contact_df_user_relevant,on='contact', how='outer')
					feature_data['agg_contact_df'].ix[~pd.isnull(feature_data['agg_contact_df']['contact_gender_user']),'contact_gender']=np.array(feature_data['agg_contact_df'][~pd.isnull(feature_data['agg_contact_df']['contact_gender_user'])]['contact_gender_user'])
					feature_data['agg_contact_df'] = feature_data['agg_contact_df'].drop('contact_gender_user', axis=1)
			
			## other data preparation
			feature_data['email_date_df'] = dict()
			for i in email_array_other:
				if bool(re.search('overview',i))==True: 
					with open(i, "rb") as file:
						feature_data['email_date_df']['overview'] = pickle.load(file)
	
			# feature generation 
			# -----------------------
	
			# feature lists
			feature_list                  = insight_meta_data['feature_list']
	
			# generate features
			feature_data['email_link_df'] = feature_wrapper_mod.generate_feature_wrapper(feature_list=feature_list, email_link_df=feature_data['email_link_df'], link_id=feature_data['email_link_df']['link_id'], msg_id=feature_data['email_link_df']['msg_id'], msg_threadid=feature_data['email_link_df']['msg_threadid'], msg_data=feature_data['msg_parsed'], link_data=feature_data['link_parsed'], conver_data=feature_data['conver_parsed'], msg_text_data=feature_data['msg_text_parsed'], contact_data=feature_data['contact_parsed'], email_date_df=feature_data['email_date_df'], current_date=current_date,contact_df=feature_data['agg_contact_df'])
			
			# save features
			with open(os.path.join(output_dir, 'other', 'feature_data.p'), 'wb') as out_file:
				pickle.dump(feature_data, out_file)

			# save final dataset
			try: 
				feature_data['email_link_df'].to_csv(os.path.join(output_dir,'dev', 'feature_dataset_temp.csv'), encoding='utf-8')
				print("Saved Dataset")
			
			except Exception as e: 
	
				print("Could Not Save Dataset")
				print(e)
	
			# sample insight generation 
			# -----------------------
	
			# insight lists
			insight_list         = insight_meta_data['sample_insight_list']
			insight_data         = dict()

			# generate sample insights
			for insight_name in insight_list: 
				if (insight_name not in insight_data.keys()):
					insight_data[insight_name]   = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=email_diff, contact_df=feature_data['agg_contact_df'], user_name=user_name, user_email=user, email_range=email_range)
	
			# save insights
			with open(os.path.join(output_dir, 'other', 'insight_data.p'), 'wb') as out_file:
				pickle.dump(insight_data, out_file)

			# update thread status
			setting_var[session_id]['key_var']['api_success'] = 'True'


	# error
	except Exception as e: 

		setting_var[session_id]['key_var']['error']       = e
		setting_var[session_id]['key_var']['error_msg']   = "Error Generating Features/Sample Insights > Try Restarting the App"
		setting_var[session_id]['key_var']['api_success'] = 'Error'

# ------------------------------------------------------------------------ #
# Views
# ------------------------------------------------------------------------ #

# Onboarding
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# landing 
# ---------------------------------------------#
@app.route('/')
@auth.login_required
def landing_view():
	
	# define globals
	global global_var, setting_var

	## initialize global variables
	user_setting_temp = user_setting_initialization('')
	
	if (('session_id' not in flask.session.keys()) or (flask.session['session_id'] not in glob.glob(user_setting_temp['output_dir']))):
		flask.session['session_id']                    				= session_initialization()
		setting_var[flask.session['session_id']]                    = dict()
		global_var[flask.session['session_id']]                     = dict()
	
		setting_var[flask.session['session_id']]['user_setting']    = user_setting_initialization(flask.session['session_id'])
		setting_var[flask.session['session_id']]['key_var']         = var_initialization()
		global_var[flask.session['session_id']]        				= global_initialization()
		flask.session.modified = True

	## NO ACCESS CHECK (LANDING)

	# create user data folder (if it does not exist)
	if not os.path.exists(setting_var[flask.session['session_id']]['user_setting']['output_dir']):
		os.makedirs(setting_var[flask.session['session_id']]['user_setting']['output_dir'])

	# render
	return flask.render_template('onboarding/landing.html',
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

# home 
# ---------------------------------------------#
@app.route('/home')
@auth.login_required
def home_view():

	# define globals
	global global_var, setting_var
	
	# access check
	if (access_check(access_level=1, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
	

		# create user-specific user data folder (if it does not exist)
		setting_var[flask.session['session_id']]['user_setting']['output_dir'] = os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir_base'], setting_var[flask.session['session_id']]['key_var']['user'])

		if not os.path.exists(setting_var[flask.session['session_id']]['user_setting']['output_dir']):
			os.makedirs(setting_var[flask.session['session_id']]['user_setting']['output_dir'])
		
		user_data_dir_init(setting_var[flask.session['session_id']]['user_setting']['output_dir'])

		# render
		return flask.render_template('onboarding/home.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# reset 
# ---------------------------------------------#
@app.route('/reset')
@auth.login_required
def reset_view():
	
	# access check
	if (access_check(access_level=0,output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# initial page
		initial_page = flask.request.args.get('initial_page')
	
		# reset
		session_id_old 				= flask.session['session_id']
		session_id_new 				= flask.session['session_id']
		flask.session['session_id'] = session_id_new
		flask.session.modified = True

		reset(reset_user=False, session_id_old=session_id_old, session_id_new=session_id_new)
	
		# render
		return flask.redirect(flask.url_for(initial_page))
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# Authentication
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# gmail_authentication 
# ---------------------------------------------#
@app.route('/gmail_authentication')
@auth.login_required
def gmail_authentication_view():

	# define globals
	global global_var, setting_var


	# access check
	if (access_check(access_level=0, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
	
		# attempt to login
		login_success, login_data = gmail_authentication(offline_mode=app_setting['offline_mode'], output_dir = setting_var[flask.session['session_id']]['user_setting']['output_dir_base'], current_date=current_date)
	
		# re-route based on login success
		if (login_success=='logged_in'):
	
			setting_var[flask.session['session_id']]['key_var']['user']       = login_data['user'] 
			setting_var[flask.session['session_id']]['key_var']['user_name']  = login_data['user_name']
			setting_var[flask.session['session_id']]['key_var']['user_photo'] = login_data['user_photo']
	
			print("Logged In - " + setting_var[flask.session['session_id']]['key_var']['user'])
			return flask.redirect(flask.url_for('home_view'))	
		
		elif (login_success=='logged_out'):
			
			return flask.redirect(flask.url_for('gmail_oauth2callback_view'))
		
		elif (login_success=='error'):
			
			setting_var[flask.session['session_id']]['key_var']['error']         = login_data[0]
			setting_var[flask.session['session_id']]['key_var']['error_msg']     = "Gmail Authentication Error > Try (a) Clearing your browser cache and/or (b) Restarting the application in an 'incognito' browser window"

			return flask.redirect(flask.url_for('error_view'))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# permission 
# ---------------------------------------------#
@app.route('/permission')
@auth.login_required
def permission_view():
	
	# access check
	if (access_check(access_level=0, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# render
		return flask.render_template('onboarding/permission.html', auth_url=flask.request.args.get('auth_url'),
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# gmail_oauth2callback
# ---------------------------------------------#
@app.route('/gmail_oauth2callback')
@auth.login_required
def gmail_oauth2callback_view():

	# access check
	if (access_check(access_level=0, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# attempt to login
		authentication_success, authentication_data = gmail_oauth2callback(offline_mode=app_setting['offline_mode'])
	
		# re-route based on login success
		if (authentication_success=='authenticated'):
	
			return flask.redirect(flask.url_for('gmail_authentication_view'))
		
		elif (authentication_success=='unauthenticated'):
			
			auth_url = authentication_data[0]
			return flask.redirect(flask.url_for('permission_view', auth_url=auth_url))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# logout 
# ---------------------------------------------#
@app.route('/logout')
@auth.login_required
def logout_view():

	# access check
	if (access_check(access_level=0, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# reset 
		session_id_old 				= flask.session['session_id']
		session_id_new 				= session_initialization()
		flask.session['session_id'] = session_id_new
		flask.session.modified = True

		reset(reset_user=True, session_id_old=session_id_old, session_id_new=session_id_new)	

		if (app_setting['offline_mode']==False):

			# redirect to login page
			redirect_uri = flask.url_for('gmail_oauth2callback_view', _external=True)
			return flask.redirect(api_logout_url+redirect_uri)
		
		else: 

			# redirect to home page
			return flask.redirect(flask.url_for(home_view))
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# Intro
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# intro_load_a
# ---------------------------------------------#
@app.route('/intro_load_a')
@auth.login_required
def intro_load_a_view():

	# define globals
	global th
	global global_var, setting_var

	# access check
	if (access_check(access_level=1, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

	
		# initialize
		global_var[flask.session['session_id']]['status_overview_load']       = 0
		global_var[flask.session['session_id']]['status_overview_max']        = 0

		# reset insight_data
		if os.path.exists(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p')):
			os.remove(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'))
	
		# reauthenticate
		login_success, login_data = gmail_reauthentication(offline_mode=app_setting['offline_mode'], output_dir = setting_var[flask.session['session_id']]['user_setting']['output_dir_base'],current_date=current_date)
	
		if (login_success=='logged_in'):
		
			# update credentials
			service                               							  = login_data['service']
			setting_var[flask.session['session_id']]['key_var']['user']       = login_data['user'] 

			# launch processing thread
			th = Thread(target=intro_load_overview_wrapper, args=(flask.session['session_id'], app_setting['offline_mode'], service, 'me', current_date,  
				setting_var[flask.session['session_id']]['user_setting']['timelag_day'], setting_var[flask.session['session_id']]['user_setting']['timelag_overview'], setting_var[flask.session['session_id']]['user_setting']['overview_day'], setting_var[flask.session['session_id']]['user_setting']['birthday_day'], 
				setting_var[flask.session['session_id']]['user_setting']['email_max'], setting_var[flask.session['session_id']]['user_setting']['min_day'],setting_var[flask.session['session_id']]['user_setting']['output_dir'],timezone_utc_offset,setting_var[flask.session['session_id']]['user_setting']['email_earliest_user'], 
				setting_var[flask.session['session_id']]['user_setting']['email_latest_user'], setting_var[flask.session['session_id']]['user_setting']['email_diff_user'], setting_var[flask.session['session_id']]['user_setting']['email_range_user'], 
				setting_var[flask.session['session_id']]['user_setting']['safe_mode']))
			th.start()
	
			return flask.render_template('intro/intro_load_a.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
				user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
		else:
	
			# flash message
			flask.flash('It looks like you will need to log-in again.')
	
			# return to log-in page
			return flask.redirect(flask.url_for('gmail_authentication_view'))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# intro_load_b
# ---------------------------------------------#
@app.route('/intro_load_b')
@auth.login_required
def intro_load_b_view():

	# define globals
	global th
	global global_var, setting_var

	# access check
	if (access_check(access_level=2, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
		
		# initialize
		global_var[flask.session['session_id']]['status_email_load']       = 0
		global_var[flask.session['session_id']]['status_email_max']        = 0

		# reauthenticate
		login_success, login_data = gmail_reauthentication(offline_mode=app_setting['offline_mode'],output_dir = setting_var[flask.session['session_id']]['user_setting']['output_dir_base'],current_date=current_date)

		if (login_success=='logged_in'):
			
			# update credentials
			service                                = login_data['service']
	
			# launch processing thread
			th = Thread(target=intro_load_email_wrapper, args=(flask.session['session_id'], app_setting['offline_mode'], service, 'me', setting_var[flask.session['session_id']]['user_setting']['email_range'], setting_var[flask.session['session_id']]['user_setting']['output_dir'], current_date, setting_var[flask.session['session_id']]['key_var']['user'],timezone_utc_offset, setting_var[flask.session['session_id']]['user_setting']['safe_mode']))
			th.start()

			return flask.render_template('intro/intro_load_b.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
				user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
				latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
				release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

		else:

			# flash message
			flask.flash('It looks like you will need to log-in again.')

			# return to log-in page
			return flask.redirect(flask.url_for('gmail_authentication_view'))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# intro_load_c
# ---------------------------------------------#
@app.route('/intro_load_c')
@auth.login_required
def intro_load_c_view():

	# define globals
	global th
	global global_var, setting_var

	# access check
	if (access_check(access_level=3, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
		
		# initialize
		global_var[flask.session['session_id']]['status_analysis_load']       = 0
		global_var[flask.session['session_id']]['status_analysis_max']        = 0

		# initialize intro
		setting_var[flask.session['session_id']]['key_var']['sample_insight_intro_id']       = 0
		insight_intro                            				                             = insight_meta_data['sample_insight_list'][0]
		setting_var[flask.session['session_id']]['key_var']['current_insight']               = ""
		setting_var[flask.session['session_id']]['key_var']['next_insight']                  = ""

		# launch processing thread
		th = Thread(target=intro_load_analysis_wrapper, args=(flask.session['session_id'], setting_var[flask.session['session_id']]['key_var']['user'], setting_var[flask.session['session_id']]['key_var']['user_name'], setting_var[flask.session['session_id']]['user_setting']['email_range'], setting_var[flask.session['session_id']]['user_setting']['email_diff'],setting_var[flask.session['session_id']]['user_setting']['output_dir'], current_date, setting_var[flask.session['session_id']]['user_setting']['email_earliest'],setting_var[flask.session['session_id']]['user_setting']['email_latest']))
		th.start()
	
		return flask.render_template('intro/intro_load_c.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], insight_name=insight_intro, release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# intro_main
# ---------------------------------------------#
@app.route('/intro_main')
@auth.login_required
def intro_main_view():


	# define globals
	global global_var, setting_var

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
	
		# load insights
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)

		# initialize
		insight_name      = flask.request.args.get('insight_name')
		insight_current   = flask.request.args.get('insight_current')

		# define next insight
		if (setting_var[flask.session['session_id']]['key_var']['current_insight']!=insight_current and setting_var[flask.session['session_id']]['key_var']['next_insight']!="insight"):
		
			setting_var[flask.session['session_id']]['key_var']['sample_insight_intro_id']  = setting_var[flask.session['session_id']]['key_var']['sample_insight_intro_id'] + 1
			setting_var[flask.session['session_id']]['key_var']['current_insight']          = insight_current

		if (setting_var[flask.session['session_id']]['key_var']['sample_insight_intro_id'] < len(insight_meta_data['sample_insight_list'])):
			
			setting_var[flask.session['session_id']]['key_var']['next_insight']             = insight_meta_data['sample_insight_list'][setting_var[flask.session['session_id']]['key_var']['sample_insight_intro_id']]
		else: 
			
			setting_var[flask.session['session_id']]['key_var']['next_insight'] 		     = "insight"
		

		# if insight exists
		if (insight_name in insight_data.keys()): 
	
			# render
			return flask.render_template('intro/intro_main.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
				user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
				latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
				timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				insight_name = insight_name, 
				insight_name_next = setting_var[flask.session['session_id']]['key_var']['next_insight'],  
				insight_data = insight_data[insight_name], 
				insight_title = insight_title[insight_name],
				next_page = 'intro_main_view',
				release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
		# if insight does not exist
		else:
	
			# render
			return flask.redirect(flask.url_for('intro_load_c_view'))
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# intro_final
# ---------------------------------------------#
@app.route('/intro_final')
@auth.login_required
def intro_final_view():

	# define globals
	global global_var, setting_var

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 


		# initialize intro
		setting_var[flask.session['session_id']]['key_var']['insight_mode']     = "intro"
		setting_var[flask.session['session_id']]['key_var']['insight_intro_id'] = 0
		insight_intro               				 							= insight_meta_data['intro_insight_list'][setting_var[flask.session['session_id']]['key_var']['insight_intro_id']]
		setting_var[flask.session['session_id']]['key_var']['current_insight']  = ""
		setting_var[flask.session['session_id']]['key_var']['next_insight']     = ""

		# render
		return flask.render_template('intro/intro_final.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],insight_intro=insight_intro,
			release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# Explore
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# dashboard_intro
# ------------------------------------------------------------------------ #
@app.route('/dashboard_intro')
@auth.login_required
def dashboard_intro_view():

	# define globals
	global global_var, setting_var

	# update status
	setting_var[flask.session['session_id']]['key_var']['intro_release'] = True

	# render
	return flask.render_template('explore/dashboard_intro.html',user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
		user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
		scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

# dashboard
# ------------------------------------------------------------------------ #
@app.route('/dashboard')
@auth.login_required
def dashboard_view():

	# define globals
	global global_var, setting_var

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 


		# reset - intro to explore mode
		setting_var[flask.session['session_id']]['key_var']['insight_mode'] = "explore"

		# render
		return flask.render_template('explore/dashboard.html',user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# Setting
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# setting
# ------------------------------------------------------------------------ #
@app.route('/setting')
@auth.login_required
def setting_view():

	# access check
	if (access_check(access_level=1, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# min access = 1 > reset OK vs. timeframe_setting require 4 / contact_resetting require 4
		access_level_4 = access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])

		# render
		return flask.render_template('setting/setting.html',user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], access_level=access_level_4, release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# timeframe_setting
# ------------------------------------------------------------------------ #
@app.route('/timeframe_setting', methods=['POST','GET'])
@auth.login_required
def timeframe_setting_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# load insights & features
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'feature_data.p'), 'rb') as file:
			feature_data = pickle.load(file)

		# initialize
		insight_name = 'date_dist_setting'
	
		# generate insight
		if (insight_name not in insight_data.keys()):

			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, 
				email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], 
				email_diff=setting_var[flask.session['session_id']]['user_setting']['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=setting_var[flask.session['session_id']]['key_var']['user_name'], 
				user_email=setting_var[flask.session['session_id']]['key_var']['user'], email_range=setting_var[flask.session['session_id']]['user_setting']['email_range'])
	
			# save insights
			with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'wb') as file:
				pickle.dump(insight_data, file)

		# render
		return flask.render_template('setting/timeframe_setting.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
			latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
			timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			insight_name = insight_name, 
			insight_data = insight_data[insight_name], 
			min_day=setting_var[flask.session['session_id']]['user_setting']['min_day'], min_email=setting_var[flask.session['session_id']]['user_setting']['min_email'], 
			max_email=setting_var[flask.session['session_id']]['user_setting']['email_max'], timelag_min=setting_var[flask.session['session_id']]['user_setting']['timelag_day'],
			release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# timeframe_setting_store
# ------------------------------------------------------------------------ #
@app.route('/timeframe_setting_store', methods=['POST','GET'])
@auth.login_required
def timeframe_setting_store_view():

	## NO ACCESS CHECK (BACKEND)

	# define globals
	global global_var, setting_var

	# obtain user data
	earliest_date_user         				= flask.request.form.get('start_date')
	latest_date_user           				= flask.request.form.get('end_date')
		
	# generate new data		
	email_diff_user, email_range_user       = get_diff_range(earliest_date_user, latest_date_user)

	# update user settings
	setting_var[flask.session['session_id']]['user_setting']['email_earliest_user']  	= earliest_date_user
	setting_var[flask.session['session_id']]['user_setting']['email_latest_user']    	= latest_date_user
	setting_var[flask.session['session_id']]['user_setting']['email_diff_user']      	= email_diff_user
	setting_var[flask.session['session_id']]['user_setting']['email_range_user']     	= email_range_user

	# reset insight_data
	if (os.path.exists(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'))):
		os.remove(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'))

	# status
	flask.flash("The timeframe settings have been updated. The analysis will now be re-run.")

	# render
	return flask.redirect(flask.url_for('intro_load_a_view'))

# group_setting
# ------------------------------------------------------------------------ #
@app.route('/contact_group')
@auth.login_required
def group_setting_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# load insights & features
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'feature_data.p'), 'rb') as file:
			feature_data = pickle.load(file)

		# initialize
		insight_name = 'group_setting'
	
		# generate insight
		if (insight_name not in insight_data.keys()):

			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, 
				email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], 
				email_diff=setting_var[flask.session['session_id']]['user_setting']['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=setting_var[flask.session['session_id']]['key_var']['user_name'], 
				user_email=setting_var[flask.session['session_id']]['key_var']['user'], email_range=setting_var[flask.session['session_id']]['user_setting']['email_range'])

			# save insights
			with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'wb') as file:
				pickle.dump(insight_data, file)


		# render
		return flask.render_template('setting/group_setting.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
			latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
			timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			insight_name = insight_name, 
			insight_data = insight_data[insight_name], 
			min_day=setting_var[flask.session['session_id']]['user_setting']['min_day'], min_email=setting_var[flask.session['session_id']]['user_setting']['min_email'], 
			max_email=setting_var[flask.session['session_id']]['user_setting']['email_max'], timelag_min=setting_var[flask.session['session_id']]['user_setting']['timelag_day'],
			release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# group_setting_store
# ------------------------------------------------------------------------ #
@app.route('/group_setting_store', methods=['POST','GET'])
@auth.login_required
def group_setting_store_view():

	## NO ACCESS CHECK (BACKEND)

	# define globals
	global global_var, setting_var

	# obtain user data
	contact_email_user         			= np.array(flask.request.form.get('contact_email_updated').split(","))
	contact_gender_user           		= np.array(flask.request.form.get('contact_gender_updated').split(","))

	map_gender 	                        = {'1':'F','2':'M','3':'I'}	
	contact_gender_user                 = list(np.array(pd.Series(contact_gender_user).map(map_gender)))
	
	# update feature set	
	contact_df_user 				    = pd.DataFrame({'contact':contact_email_user, 'contact_gender_user':contact_gender_user})

	if (isinstance(setting_var[flask.session['session_id']]['key_var']['contact_group_user'], pd.DataFrame)):
		setting_var[flask.session['session_id']]['key_var']['contact_group_user']  = setting_var[flask.session['session_id']]['key_var']['contact_group_user'].rename(columns={'contact_gender_user': 'contact_gender'})
		setting_var[flask.session['session_id']]['key_var']['contact_group_user']  = pd.merge(setting_var[flask.session['session_id']]['key_var']['contact_group_user'], contact_df_user, on='contact', how='outer')
		setting_var[flask.session['session_id']]['key_var']['contact_group_user'].ix[~pd.isnull(setting_var[flask.session['session_id']]['key_var']['contact_group_user']['contact_gender_user']),'contact_gender']=np.array(setting_var[flask.session['session_id']]['key_var']['contact_group_user'][~pd.isnull(setting_var[flask.session['session_id']]['key_var']['contact_group_user']['contact_gender_user'])]['contact_gender_user'])
		setting_var[flask.session['session_id']]['key_var']['contact_group_user']  = setting_var[flask.session['session_id']]['key_var']['contact_group_user'].drop('contact_gender_user', axis=1)
		setting_var[flask.session['session_id']]['key_var']['contact_group_user']  = setting_var[flask.session['session_id']]['key_var']['contact_group_user'].rename(columns={'contact_gender': 'contact_gender_user'})
	else: 
		setting_var[flask.session['session_id']]['key_var']['contact_group_user']  = contact_df_user

	# reset insight_data
	if (os.path.exists(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'))):
		os.remove(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'))

	# status
	flask.flash("The groups have been updated. The analysis will now be re-run.")

	# render
	return flask.redirect(flask.url_for('intro_load_c_view'))



# scroll_mode
# ------------------------------------------------------------------------ #
@app.route('/scroll_mode')
@auth.login_required
def scroll_mode_view():

	# define globals
	global global_var, setting_var

	# access check
	if (access_check(access_level=1, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 


		# update
		setting_var[flask.session['session_id']]['key_var']['scroll_mode'] = np.invert(setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

		# status
		if setting_var[flask.session['session_id']]['key_var']['scroll_mode']==True:
			flask.flash("The display mode has been adjusted. Scroll mode is now turned on.")
		else:
			flask.flash("The display mode has been adjusted. Scroll mode is now turned off.")

		# min access = 1 > reset OK vs. timeframe_setting require 4 / contact_resetting require 4
		access_level_4 = access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])

		# render
		return flask.render_template('setting/setting.html',user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'], access_level=access_level_4, release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# Insight
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# insight_intro
# ------------------------------------------------------------------------ #
@app.route('/insight_intro')
@auth.login_required
def insight_intro_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
		
		# load insights & features
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'feature_data.p'), 'rb') as file:
			feature_data = pickle.load(file)

		# initialize
		insight_name = flask.request.args.get('insight_name')
	
		# generate insight
		if (insight_name not in insight_data.keys()):
			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=setting_var[flask.session['session_id']]['user_setting']['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=setting_var[flask.session['session_id']]['key_var']['user_name'], user_email=setting_var[flask.session['session_id']]['key_var']['user'], email_range=setting_var[flask.session['session_id']]['user_setting']['email_range'])
	
			# save insights
			with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'wb') as file:
				pickle.dump(insight_data, file)

		# render
		return flask.render_template('insight/insight_intro.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
			latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
			insight_text = insight_text[insight_name]['screen_intro'], 
			insight_data = insight_data[insight_name], 
			insight_name = insight_name, 
			insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
			insight_title = insight_title[insight_name],
			release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# insight_a
# ------------------------------------------------------------------------ #
@app.route('/insight_a')
@auth.login_required
def insight_a_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# load insights
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)

		# initialize
		insight_name = flask.request.args.get('insight_name')
	
		# if insight exists
		if (insight_name in insight_data.keys()):

			if insight_name in insight_meta_data['add_info_list']:
				more_info          = True
				insight_text_extra = insight_text[insight_name]['screen_add']
			else:
				more_info          = False
				insight_text_extra = ""
	
	
			# render
			return flask.render_template('insight/insight_a.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
				user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
				latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
				insight_text = insight_text[insight_name]['screen_1'], 
				insight_text_extra = insight_text_extra, 
				insight_data = insight_data[insight_name], 
				insight_name = insight_name, 
				insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
				insight_title = insight_title[insight_name],
				release_mode = setting_var[flask.session['session_id']]['key_var']["intro_release"], 
				more_info = more_info,
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
		# if insight does not exist
		else:
	
			# render
	
			return flask.redirect(flask.url_for('insight_intro_view', insight_name = insight_name)) 

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# insight_b
# ------------------------------------------------------------------------ #
@app.route('/insight_b',methods=['POST','GET'])
@auth.login_required
def insight_b_view(analysis_data="None",analysis_text_id="None", analysis_data_text="None"):

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# load insights
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)

		# initialize
		insight_name = flask.request.args.get('insight_name')
		
		if flask.request.args.get('insight_name', None):
			insight_name  	= flask.request.args['insight_name']
	
		if (insight_name not in insight_meta_data['skip_sample_insight_list']):

			# if insight exists
			if (insight_name in insight_data.keys()):
		
				# > FORM SPECIFIC SECTION (PROCESS SAMPLES)
				# form variables & process	
				
				if flask.request.args.get('analysis_text_id', None):
					analysis_text_id  = flask.request.args['analysis_text_id']
	
				if flask.request.args.get('analysis_text', None):
					analysis_data_text = flask.request.args['analysis_text']
					analysis_data      = analysis_wrapper(msg_text=analysis_data_text, insight=insight_name)
	
				# render
				return flask.render_template('insight/insight_b.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
					user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
					earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
					latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
					insight_text = insight_text[insight_name]['screen_2'], 
					insight_data = insight_data[insight_name], 
					insight_name = insight_name,
					insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
					insight_title = insight_title[insight_name], 
					analysis_data = analysis_data,
					analysis_text_id = analysis_text_id,
					analysis_data_text = analysis_data_text,
					release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
					scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
		
			# if insight does not exist
			else:
		
				# render
				return flask.redirect(flask.url_for('insight_intro_view', insight_name = insight_name))

		else: 

			return flask.redirect(flask.url_for('insight_c_view', insight_name = insight_name))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# insight_c
# ------------------------------------------------------------------------ #
@app.route('/insight_c')
@auth.login_required
def insight_c_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# load insights
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)

		# initialize
		insight_name = flask.request.args.get('insight_name')
		
		# if insight exists
		if (insight_name in insight_data.keys()):
		
			# render
			return flask.render_template('insight/insight_c.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
				user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
				latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
				insight_data = insight_data[insight_name], 
				insight_name = insight_name,
				insight_name_next = insight_name,
				insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
				insight_title = insight_title[insight_name], 
				next_page = 'insight_d_view',
				release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
				scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
		
		# if insight does not exist
		else:
		
			# render
			return flask.redirect(flask.url_for('insight_intro_view', insight_name = insight_name))
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# insight_d
# ------------------------------------------------------------------------ #
@app.route('/insight_d')
@auth.login_required
def insight_d_view():

	# define globals
	global global_var, setting_var

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 
		
		# load insights
		with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
			insight_data = pickle.load(file)

		# initialize
		insight_name     = flask.request.args.get('insight_name')
		insight_current  = flask.request.args.get('insight_current')
		
		# define next insight
		if (setting_var[flask.session['session_id']]['key_var']['current_insight']!=insight_current and setting_var[flask.session['session_id']]['key_var']['next_insight']!="dashboard"):
		
			setting_var[flask.session['session_id']]['key_var']['insight_intro_id']         = setting_var[flask.session['session_id']]['key_var']['insight_intro_id'] + 1
			setting_var[flask.session['session_id']]['key_var']['current_insight']          = insight_current

		if (setting_var[flask.session['session_id']]['key_var']['insight_intro_id'] < len(insight_meta_data['intro_insight_list'])):
			
			setting_var[flask.session['session_id']]['key_var']['next_insight']             = insight_meta_data['intro_insight_list'][setting_var[flask.session['session_id']]['key_var']['insight_intro_id']]
		else: 

			setting_var[flask.session['session_id']]['key_var']['next_insight'] 			= "dashboard"

		if (insight_name not in insight_meta_data['sample_insight_list']):
	
			# if insight exists
			if (insight_name in insight_data.keys()):
	
				# render
				return flask.render_template('insight/insight_d.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
					user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
					earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
					latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
					insight_data = insight_data[insight_name], 
					insight_name = insight_name,
					insight_name_next = setting_var[flask.session['session_id']]['key_var']['next_insight'],
					insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
					insight_title = insight_title[insight_name],
					release_mode=setting_var[flask.session['session_id']]['key_var']["intro_release"],
					scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	
			# if insight does not exist
			else:
	
				# render
				return flask.redirect(flask.url_for('insight_intro_view',insight_name = insight_name))
		
		else:
	
			if (setting_var[flask.session['session_id']]['key_var']['insight_mode']=="intro"):
				if (insight_name_next == "dashboard"):
					return flask.redirect(flask.url_for('dashboard_intro_view'))
				else:
					return flask.redirect(flask.url_for('insight_intro_view', insight_name=insight_name_next))
			else:
				return flask.redirect(flask.url_for('dashboard_view'))
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# insight_info
# ------------------------------------------------------------------------ #
@app.route('/insight_info')
@auth.login_required
def insight_info_view():

	# access check
	if (access_check(access_level=4, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# initialize
		insight_name      = flask.request.args.get('insight_name')
		
		if insight_name in insight_meta_data['add_info_list']:
			more_info          = True
			insight_text_extra = insight_text[insight_name]['screen_add']
		else:
			more_info          = False
			insight_text_extra = ""
	

		# render
		return flask.render_template('insight/insight_info.html', user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			earliest_date = setting_var[flask.session['session_id']]['user_setting']["email_earliest"], 
			latest_date = setting_var[flask.session['session_id']]['user_setting']["email_latest"], date_diff=setting_var[flask.session['session_id']]['user_setting']["email_diff"],
			insight_text = insight_text[insight_name]['screen_1'], 
			insight_text_extra = insight_text_extra, 
			insight_name = insight_name, 
			insight_mode = setting_var[flask.session['session_id']]['key_var']['insight_mode'], 
			insight_title = insight_title[insight_name],
			release_mode = setting_var[flask.session['session_id']]['key_var']["intro_release"],
			more_info = more_info,
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])
	

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# references
# ------------------------------------------------------------------------ #
@app.route('/references')
@auth.login_required
def references_view():

	if (access_check(access_level=1, output_dir=setting_var[flask.session['session_id']]['user_setting']['output_dir'])) == True: 

		# render
		return flask.render_template('explore/references.html', 
			user=setting_var[flask.session['session_id']]['key_var']['user_name'],user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
			user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],
			scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# Update
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# intro_load_update
# ---------------------------------------------#
@app.route('/intro_load_update')
@auth.login_required
def intro_load_update_view():
	

	## NO ACCESS CHECK (BACKEND)	

	# thread progress
	return flask.jsonify(
		dict(
			status = {
				'True': 'finished',
				'False': 'running',
				'Error': 'error'
				}[setting_var[flask.session['session_id']]['key_var']['api_success']],
			status_email_load    = global_var[flask.session['session_id']]['status_email_load'], 
			status_email_max     = global_var[flask.session['session_id']]['status_email_max'],
			status_overview_load = global_var[flask.session['session_id']]['status_overview_load'], 
			status_overview_max  = global_var[flask.session['session_id']]['status_overview_max'],
			status_analysis_load = global_var[flask.session['session_id']]['status_analysis_load'], 
			status_analysis_max  = global_var[flask.session['session_id']]['status_analysis_max']	
		))

# insight_update
# ------------------------------------------------------------------------ #
@app.route('/insight_update')
@auth.login_required
def insight_update_view():

	## NO ACCESS CHECK (BACKEND)

	# load insights & features
	with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'rb') as file:
		insight_data = pickle.load(file)
	with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'feature_data.p'), 'rb') as file:
		feature_data = pickle.load(file)

	# obtain insight name & original page
	insight_name      = flask.request.args.get('insight_name')

	# regenerate insight
	insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=setting_var[flask.session['session_id']]['user_setting']['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=setting_var[flask.session['session_id']]['key_var']['user_name'], user_email=setting_var[flask.session['session_id']]['key_var']['user'], email_range=setting_var[flask.session['session_id']]['user_setting']['email_range'])

	# save insights
	with open(os.path.join(setting_var[flask.session['session_id']]['user_setting']['output_dir'], 'other', 'insight_data.p'), 'wb') as file:
		pickle.dump(insight_data, file)

	# redirect to original insight page
	return flask.jsonify(
		dict(
			insight_data    = insight_data[insight_name] 
		))

# Misc
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# error
# ------------------------------------------------------------------------ #
@app.route('/error')
@auth.login_required
def error_view():

	## NO ACCESS CHECK (ERROR)

	# error message
	print("Error encountered")
	print(setting_var[flask.session['session_id']]['key_var']['error'])

	# render
	return flask.render_template('misc/error.html', 
		error_msg=setting_var[flask.session['session_id']]['key_var']['error_msg'], 
		user=setting_var[flask.session['session_id']]['key_var']['user_name'],
		user_email=setting_var[flask.session['session_id']]['key_var']['user'], 
		user_photo=setting_var[flask.session['session_id']]['key_var']['user_photo'],
		scroll_mode=setting_var[flask.session['session_id']]['key_var']['scroll_mode'])

# ------------------------------------------------------------------------ #
# Launch App                
# ------------------------------------------------------------------------ #
if __name__ == "__main__":
	
	# Non-Debug Mode
	if (app_setting['app_debug']==False):
		print("Starting")
		http_server = WSGIServer(('', app_setting['app_port']), app)
		http_server.serve_forever()

	# Debug Mode
	elif (app_setting['app_debug']==True):	
		print("Starting - Debug")
		app.run(host='0.0.0.0', port=app_setting['app_port'])

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
