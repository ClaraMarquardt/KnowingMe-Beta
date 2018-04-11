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

# Globals
global user_setting, app_setting, key_var, insight_data, insight_text, insight_title

user_setting                                   = user_setting_initialization()
app_setting                                    = app_setting_initialization()
key_var                         			   = var_initialization()
insight_data, insight_text, insight_title      = insight_initialization()

# Dependency settings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

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
app = flask_initialize(debug=app_setting['app_debug'], secret_key=secret_key, 
	app_static=app_static, app_template=app_template)

# ------------------------------------------------------------------------ #
# Functions
# ------------------------------------------------------------------------ #

# reset
# ---------------------------------------------#
def reset(reset_user=True):

	# define globals
	global user_setting, app_setting, key_var, insight_data, insight_text, insight_title, feature_data

	# display reset message
	flask.flash('App Resetting ('+str(user_setting['output_dir'])+') - OK?')
	
	# redefine variables
	user_setting               				  = user_setting_initialization()
	app_setting                			      = app_setting_initialization()
	key_var      			   			      = var_initialization(reset_user=reset_user, key_var_old=key_var)
	insight_data, insight_text, insight_title = insight_initialization()

	# clear user data
	user_data_dir_clear(user_setting['output_dir'])

	# clear data in memory
	if 'feature_data' in globals():
		del feature_data

	# display reset message
	flask.flash('App Successfully Reset.')


# access checks
# ---------------------------------------------#

# access_check
# --------------------------------#
def access_check(access_level):

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
		
		# perform lovwer level checks
		lower_level_check = []
		lower_level_check.append(access_check(access_level=0))
		lower_level_check.append(access_check(access_level=1))
		lower_level_check.append(access_check(access_level=2))
		lower_level_check.append(access_check(access_level=3))

		# define required objects
		min_object       = ['feature_data', 'insight_data']
		min_object_check = []

		# check existance of required objects
		for obj in min_object:
			if obj in globals():
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
def intro_load_overview_wrapper(offline_mode, service, user, current_date, timelag_day, timelag_overview, overview_day, birthday_day, email_max, min_day,output_dir,timezone_utc_offset,email_earliest_user, email_latest_user, email_diff_user, email_range_user):

	# define globals
	global key_var
	global user_setting

	# initialize
	key_var['api_success'] = 'False'

	# launch process
	try: 
	
		if (offline_mode==False):	

			# email & birthday overview
			overview_email(service, user, current_date, timelag_overview, overview_day, birthday_day, output_dir, timezone_utc_offset)

		# determine analysis timeframe
		user_setting['email_earliest'], user_setting['email_latest'], user_setting['email_diff'], user_setting['email_range']  = timeframe_email(current_date, timelag_day, timelag_overview, min_day, overview_day, email_max, output_dir)
		print(user_setting)
		# modify based on user settings
		if (pd.isnull(user_setting['email_earliest_user'])==False):
			user_setting['email_earliest'] = email_earliest_user
			user_setting['email_latest']   = email_latest_user
			user_setting['email_diff']     = email_diff_user
			user_setting['email_range']    = email_range_user

		# update thread status
		key_var['api_success'] = 'True'

	# error
	except Exception as e: 

		key_var['error']       = e
		key_var['error_msg']   = "Error Generating Email Overview > Try Restarting the App"
		key_var['api_success'] = 'Error'

# intro_load_email_wrapper
# --------------------------------#
def intro_load_email_wrapper(offline_mode, service, user, email_range, output_dir, current_date, user_email, timezone_utc_offset):

	# define globals
	global key_var

	# initialize
	key_var['api_success'] = 'False'

	# launch process
	try: 
		
		if (offline_mode==False):	
		
			# emails
			get_email(service, user, email_range, output_dir, current_date, user_email, timezone_utc_offset)

		# update thread status
		key_var['api_success'] = 'True'

	# error
	except Exception as e: 

		key_var['error']       = e
		key_var['error_msg']   = "Error Extracting Emails > Try Restarting the App"
		key_var['api_success'] = 'Error'

# intro_load_analysis_wrapper
# --------------------------------#
def intro_load_analysis_wrapper(user, user_name, email_range, email_diff, output_dir, current_date, earliest_date, latest_date):

	# define globals
	global key_var
	global feature_data
	global insight_data

	# initialize
	key_var['api_success'] = 'False'

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

			key_var['error']         = "No emails to process - try restarting the app."
			key_var['error_msg']     = "No emails to process - try restarting the app."
			
			return flask.redirect(flask.url_for('error_view'))

		else:
		

			# data preparation 
			# -----------------------
	
			## main data preparation
			feature_data         = analysis(email_array, user, output_dir, current_date, earliest_date, latest_date)
			
			## modify contact df (user settings)
			if (isinstance(key_var['contact_group_user'], pd.DataFrame)):
				contact_df_user_relevant_filter = [x in np.array(feature_data['agg_contact_df']['contact']) for x in np.array(key_var['contact_group_user']['contact'])]
				contact_df_user_relevant        = key_var['contact_group_user'][contact_df_user_relevant_filter]
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
			feature_list                  = insight_data['feature_list']
	
			# generate features
			feature_data['email_link_df'] = feature_wrapper_mod.generate_feature_wrapper(feature_list=feature_list, email_link_df=feature_data['email_link_df'], link_id=feature_data['email_link_df']['link_id'], msg_id=feature_data['email_link_df']['msg_id'], msg_threadid=feature_data['email_link_df']['msg_threadid'], msg_data=feature_data['msg_parsed'], link_data=feature_data['link_parsed'], conver_data=feature_data['conver_parsed'], msg_text_data=feature_data['msg_text_parsed'], contact_data=feature_data['contact_parsed'], email_date_df=feature_data['email_date_df'], current_date=current_date,contact_df=feature_data['agg_contact_df'])
			
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
			insight_list         = insight_data['sample_insight_list']
			
			# generate sample insights
			for insight_name in insight_list: 
				if (insight_name not in insight_data.keys()):
					insight_data[insight_name]   = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=email_diff, contact_df=feature_data['agg_contact_df'], user_name=user_name, user_email=user, email_range=email_range)
	
	
			# update thread status
			key_var['api_success'] = 'True'

	# error
	except Exception as e: 

		key_var['error']       = e
		key_var['error_msg']   = "Error Generating Features/Sample Insights > Try Restarting the App"
		key_var['api_success'] = 'Error'

# ------------------------------------------------------------------------ #
# Views
# ------------------------------------------------------------------------ #

# Onboarding
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# landing 
# ---------------------------------------------#
@app.route('/')
def landing_view():

	## NO ACCESS CHECK (LANDING)

	# create user data folder (if it does not exist)
	if not os.path.exists(user_setting['output_dir']):
		os.makedirs(user_setting['output_dir'])

	# render
	return flask.render_template('onboarding/landing.html',
				scroll_mode=key_var['scroll_mode'])

# home 
# ---------------------------------------------#
@app.route('/home')
def home_view():
	
	# access check
	if (access_check(access_level=1)) == True: 
	
		# define globals
		global user_setting
		global key_var
	
		# create user-specific user data folder (if it does not exist)
		user_setting['output_dir'] = os.path.join(user_setting['output_dir_base'], key_var['user'])
		if not os.path.exists(user_setting['output_dir']):
			os.makedirs(user_setting['output_dir'])
		
		user_data_dir_init(user_setting['output_dir'])

		# render
		return flask.render_template('onboarding/home.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# reset 
# ---------------------------------------------#
@app.route('/reset')
def reset_view():
	
	# access check
	if (access_check(access_level=0)) == True: 

		# initial page
		initial_page = flask.request.args.get('initial_page')
	
		# reset
		reset(reset_user=False)
	
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
def gmail_authentication_view():

	# access check
	if (access_check(access_level=0)) == True: 

		# define globals
		global key_var
	
		# attempt to login
		login_success, login_data = gmail_authentication(offline_mode=app_setting['offline_mode'], output_dir = user_setting['output_dir_base'], current_date=current_date)
	
		# re-route based on login success
		if (login_success=='logged_in'):
	
			key_var['service']    = login_data['service']
			key_var['user']       = login_data['user'] 
			key_var['user_name']  = login_data['user_name']
			key_var['user_photo'] = login_data['user_photo']
	
			print("Logged In - " + key_var['user'])
			return flask.redirect(flask.url_for('home_view'))	
		
		elif (login_success=='logged_out'):
			
			return flask.redirect(flask.url_for('gmail_oauth2callback_view'))
		
		elif (login_success=='error'):
			
			key_var['error']         = login_data[0]
			key_var['error_msg']     = "Gmail Authentication Error > Try (a) Clearing your browser cache and/or (b) Restarting the application in an 'incognito' browser window"
			return flask.redirect(flask.url_for('error_view'))

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# permission 
# ---------------------------------------------#
@app.route('/permission')
def permission_view():
	
	# access check
	if (access_check(access_level=0)) == True: 

		# render
		return flask.render_template('onboarding/permission.html', auth_url=flask.request.args.get('auth_url'),
				scroll_mode=key_var['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# gmail_oauth2callback
# ---------------------------------------------#
@app.route('/gmail_oauth2callback')
def gmail_oauth2callback_view():

	# access check
	if (access_check(access_level=0)) == True: 

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
def logout_view():

	# access check
	if (access_check(access_level=0)) == True: 

		# reset 
		reset(reset_user=True)
	

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
def intro_load_a_view():

	# access check
	if (access_check(access_level=1)) == True: 

		# define globals
		global th
		global global_var
		global insight_data
		global insight_text
	
		# initialize
		global_var['status_overview_load']       = 0
		global_var['status_overview_max']        = 0
	
		# reset insight_data
		insight_data, insight_text, insight_title = insight_initialization()
	
		# reauthenticate
		login_success, login_data = gmail_reauthentication(offline_mode=app_setting['offline_mode'], output_dir = user_setting['output_dir_base'],current_date=current_date)
	
		if (login_success=='logged_in'):
		
			# update credentials
			key_var['service']    = login_data['service']
			key_var['user']       = login_data['user'] 
	
			# launch processing thread
			th = Thread(target=intro_load_overview_wrapper, args=(app_setting['offline_mode'], key_var['service'], 'me', current_date,  
				user_setting['timelag_day'], user_setting['timelag_overview'], user_setting['overview_day'], user_setting['birthday_day'], 
				user_setting['email_max'], user_setting['min_day'],user_setting['output_dir'],timezone_utc_offset,user_setting['email_earliest_user'], 
				user_setting['email_latest_user'], user_setting['email_diff_user'], user_setting['email_range_user']))
			th.start()
	
			return flask.render_template('intro/intro_load_a.html', user=key_var['user_name'],user_email=key_var['user'], 
				user_photo=key_var['user_photo'], release_mode=key_var["intro_release"],
				scroll_mode=key_var['scroll_mode'])
	
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
def intro_load_b_view():

	# access check
	if (access_check(access_level=2)) == True: 

		# define globals
		global th
		global global_var

		# initialize
		global_var['status_email_load']       = 0
		global_var['status_email_max']        = 0

		# reauthenticate
		login_success, login_data = gmail_reauthentication(offline_mode=app_setting['offline_mode'],output_dir = user_setting['output_dir_base'],current_date=current_date)

		if (login_success=='logged_in'):
			print(user_setting)
			# launch processing thread
			th = Thread(target=intro_load_email_wrapper, args=(app_setting['offline_mode'], key_var['service'], 'me', user_setting['email_range'], user_setting['output_dir'], current_date, key_var['user'],timezone_utc_offset))
			th.start()

			return flask.render_template('intro/intro_load_b.html', user=key_var['user_name'],user_email=key_var['user'], 
				user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
				latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
				release_mode=key_var["intro_release"],
				scroll_mode=key_var['scroll_mode'])

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
def intro_load_c_view():

	# access check
	if (access_check(access_level=3)) == True: 

		# define globals
		global th
		global global_var
		global key_var
		
		# initialize
		global_var['status_analysis_load']       = 0
		global_var['status_analysis_max']        = 0
	
		# initialize intro
		key_var['sample_insight_intro_id']       = 0
		insight_intro                            = insight_data['sample_insight_list'][key_var['sample_insight_intro_id']]
		key_var['current_insight']               = ""
		key_var['next_insight']                  = ""
		
		# launch processing thread
		th = Thread(target=intro_load_analysis_wrapper, args=(key_var['user'], key_var['user_name'], user_setting['email_range'], user_setting['email_diff'],user_setting['output_dir'], current_date, user_setting['email_earliest'],user_setting['email_latest']))
		th.start()
	
		return flask.render_template('intro/intro_load_c.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], insight_name=insight_intro, release_mode=key_var["intro_release"],
				scroll_mode=key_var['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# intro_main
# ---------------------------------------------#
@app.route('/intro_main')
def intro_main_view():
	
	global key_var

	# access check
	if (access_check(access_level=4)) == True: 
	
		# initialize
		insight_name      = flask.request.args.get('insight_name')
		insight_current   = flask.request.args.get('insight_current')

		# define next insight
		if (key_var['current_insight']!=insight_current and key_var['next_insight']!="insight"):
		
			key_var['sample_insight_intro_id']  = key_var['sample_insight_intro_id'] + 1
			key_var['current_insight']          = insight_current
		
		if (key_var['sample_insight_intro_id'] < len(insight_data['sample_insight_list'])):
			
			key_var['next_insight']                   = insight_data['sample_insight_list'][key_var['sample_insight_intro_id']]
		
		else: 
			
			key_var['next_insight'] 		          = "insight"

		# if insight exists
		if (insight_name in insight_data.keys()): 
	
			# render
			return flask.render_template('intro/intro_main.html', user=key_var['user_name'],user_email=key_var['user'], 
				user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
				latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
				timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				insight_name = insight_name, 
				insight_name_next = key_var['next_insight'],  
				insight_data = insight_data[insight_name], 
				insight_title = insight_title[insight_name],
				next_page = 'intro_main_view',
				release_mode=key_var["intro_release"],
				scroll_mode=key_var['scroll_mode'])
	
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
def intro_final_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# define globals
		global key_var
	
		# initialize intro
		key_var['insight_mode']     = "intro"
		key_var['insight_intro_id'] = 0
		insight_intro               = insight_data['intro_insight_list'][key_var['insight_intro_id']]
		key_var['current_insight']  = ""
		key_var['next_insight']     = ""
	
		# render
		return flask.render_template('intro/intro_final.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'],insight_intro=insight_intro,
			release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

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
def dashboard_intro_view():

	# define globals
	global key_var

	# update status
	key_var['intro_release'] = True

	# render
	return flask.render_template('explore/dashboard_intro.html',user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'],release_mode=key_var["intro_release"],
		scroll_mode=key_var['scroll_mode'])

# dashboard
# ------------------------------------------------------------------------ #
@app.route('/dashboard')
def dashboard_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# define globals
		global key_var
	
		# reset - intro to explore mode
		key_var['insight_mode'] = "explore"
	
		# render
		return flask.render_template('explore/dashboard.html',user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'],release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

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
def setting_view():

	# access check
	if (access_check(access_level=1)) == True: 

		# min access = 1 > reset OK vs. timeframe_setting require 4 / contact_resetting require 4
		access_level_4 = access_check(access_level=4)

		# render
		return flask.render_template('setting/setting.html',user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], access_level=access_level_4, release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])
	
	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# timeframe_setting
# ------------------------------------------------------------------------ #
@app.route('/timeframe_setting', methods=['POST','GET'])
def timeframe_setting_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# initialize
		insight_name = 'date_dist_setting'
	
		# generate insight
		if (insight_name not in insight_data.keys()):

			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, 
				email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], 
				email_diff=user_setting['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=key_var['user_name'], 
				user_email=key_var['user'], email_range=user_setting['email_range'])
	
		# render
		return flask.render_template('setting/timeframe_setting.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
			latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
			timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			insight_name = insight_name, 
			insight_data = insight_data[insight_name], 
			min_day=user_setting['min_day'], min_email=user_setting['min_email'], 
			max_email=user_setting['email_max'], timelag_min=user_setting['timelag_day'],
			release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))

# timeframe_setting_store
# ------------------------------------------------------------------------ #
@app.route('/timeframe_setting_store', methods=['POST','GET'])
def timeframe_setting_store_view():

	## NO ACCESS CHECK (BACKEND)

	# define globals
	global user_setting, insight_data, insight_text, insight_title

	# obtain user data
	earliest_date_user         				= flask.request.form.get('start_date')
	latest_date_user           				= flask.request.form.get('end_date')
		
	# generate new data		
	email_diff_user, email_range_user       = get_diff_range(earliest_date_user, latest_date_user)

	# update user settings
	user_setting['email_earliest_user']  	= earliest_date_user
	user_setting['email_latest_user']    	= latest_date_user
	user_setting['email_diff_user']      	= email_diff_user
	user_setting['email_range_user']     	= email_range_user

	# reset insights
	insight_data, insight_text, insight_title      = insight_initialization()

	# status
	flask.flash("The timeframe settings have been updated. The analysis will now be re-run.")

	# render
	return flask.redirect(flask.url_for('intro_load_a_view'))

# group_setting
# ------------------------------------------------------------------------ #
@app.route('/contact_group')
def group_setting_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# initialize
		insight_name = 'group_setting'
	
		# generate insight
		if (insight_name not in insight_data.keys()):

			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, 
				email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], 
				email_diff=user_setting['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=key_var['user_name'], 
				user_email=key_var['user'], email_range=user_setting['email_range'])

	
		# render
		return flask.render_template('setting/group_setting.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
			latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
			timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			insight_name = insight_name, 
			insight_data = insight_data[insight_name], 
			min_day=user_setting['min_day'], min_email=user_setting['min_email'], 
			max_email=user_setting['email_max'], timelag_min=user_setting['timelag_day'],
			release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# group_setting_store
# ------------------------------------------------------------------------ #
@app.route('/group_setting_store', methods=['POST','GET'])
def group_setting_store_view():

	## NO ACCESS CHECK (BACKEND)

	# define globals
	global user_setting, insight_data, insight_text, insight_title, key_var

	# obtain user data
	contact_email_user         			= np.array(flask.request.form.get('contact_email_updated').split(","))
	contact_gender_user           		= np.array(flask.request.form.get('contact_gender_updated').split(","))

	map_gender 	                        = {'1':'F','2':'M','3':'I'}	
	contact_gender_user                 = list(np.array(pd.Series(contact_gender_user).map(map_gender)))
	
	# update feature set	
	contact_df_user 				    = pd.DataFrame({'contact':contact_email_user, 'contact_gender_user':contact_gender_user})
	print(contact_df_user)

	if (isinstance(key_var['contact_group_user'], pd.DataFrame)):
		key_var['contact_group_user']  = key_var['contact_group_user'].rename(columns={'contact_gender_user': 'contact_gender'})
		key_var['contact_group_user']  = pd.merge(key_var['contact_group_user'], contact_df_user, on='contact', how='outer')
		key_var['contact_group_user'].ix[~pd.isnull(key_var['contact_group_user']['contact_gender_user']),'contact_gender']=np.array(key_var['contact_group_user'][~pd.isnull(key_var['contact_group_user']['contact_gender_user'])]['contact_gender_user'])
		key_var['contact_group_user']  = key_var['contact_group_user'].drop('contact_gender_user', axis=1)
		key_var['contact_group_user']  = key_var['contact_group_user'].rename(columns={'contact_gender': 'contact_gender_user'})
	else: 
		key_var['contact_group_user']  = contact_df_user

	# reset insights
	insight_data, insight_text, insight_title      = insight_initialization()

	# status
	flask.flash("The groups have been updated. The analysis will now be re-run.")

	# render
	return flask.redirect(flask.url_for('intro_load_c_view'))



# scroll_mode
# ------------------------------------------------------------------------ #
@app.route('/scroll_mode')
def scroll_mode_view():

	# access check
	if (access_check(access_level=1)) == True: 

		# define globals
		global key_var

		# update
		key_var['scroll_mode'] = np.invert(key_var['scroll_mode'])
	
		# status
		if key_var['scroll_mode']==True:
			flask.flash("The display mode has been adjusted. Scroll mode is now turned on.")
		else:
			flask.flash("The display mode has been adjusted. Scroll mode is now turned off.")

		# min access = 1 > reset OK vs. timeframe_setting require 4 / contact_resetting require 4
		access_level_4 = access_check(access_level=4)

		# render
		return flask.render_template('setting/setting.html',user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], access_level=access_level_4, release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

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
def insight_intro_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# define globals
		global insight_data
		
		# initialize
		insight_name = flask.request.args.get('insight_name')
	
		# generate insight
		if (insight_name not in insight_data.keys()):
			insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=user_setting['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=key_var['user_name'], user_email=key_var['user'], email_range=user_setting['email_range'])
	
		# render
		return flask.render_template('insight/insight_intro.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			earliest_date = user_setting["email_earliest"], 
			latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
			insight_text = insight_text[insight_name]['screen_intro'], 
			insight_data = insight_data[insight_name], 
			insight_name = insight_name, 
			insight_mode = key_var['insight_mode'], 
			insight_title = insight_title[insight_name],
			release_mode=key_var["intro_release"],
			scroll_mode=key_var['scroll_mode'])

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))


# insight_a
# ------------------------------------------------------------------------ #
@app.route('/insight_a')
def insight_a_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# initialize
		insight_name = flask.request.args.get('insight_name')
	
		# if insight exists
		if (insight_name in insight_data.keys()):

			if insight_name in insight_data['add_info_list']:
				more_info          = True
				insight_text_extra = insight_text[insight_name]['screen_add']
			else:
				more_info          = False
				insight_text_extra = ""
	
	
			# render
			return flask.render_template('insight/insight_a.html', user=key_var['user_name'],user_email=key_var['user'], 
				user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				earliest_date = user_setting["email_earliest"], 
				latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
				insight_text = insight_text[insight_name]['screen_1'], 
				insight_text_extra = insight_text_extra, 
				insight_data = insight_data[insight_name], 
				insight_name = insight_name, 
				insight_mode = key_var['insight_mode'], 
				insight_title = insight_title[insight_name],
				release_mode = key_var["intro_release"], 
				more_info = more_info,
				scroll_mode=key_var['scroll_mode'])
	
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
def insight_b_view(analysis_data="None",analysis_text_id="None", analysis_data_text="None"):

	# access check
	if (access_check(access_level=4)) == True: 

		# initialize
		insight_name = flask.request.args.get('insight_name')
		if flask.request.args.get('insight_name', None):
			insight_name  	= flask.request.args['insight_name']
	
		if (insight_name not in insight_data['skip_sample_insight_list']):

			# if insight exists
			if (insight_name in insight_data.keys()):
		
				# > FORM SPECIFIC SECTION (PROCESS SAMPLES)
				# form variables & process	
				
				if flask.request.args.get('analysis_text_id', None):
					print(flask.request.args['analysis_text_id'])
					analysis_text_id  = flask.request.args['analysis_text_id']
	
				if flask.request.args.get('analysis_text', None):
					print(flask.request.args['analysis_text'])
					analysis_data_text = flask.request.args['analysis_text']
					analysis_data      = analysis_wrapper(msg_text=analysis_data_text, insight=insight_name)
	
				# render
				return flask.render_template('insight/insight_b.html', user=key_var['user_name'],user_email=key_var['user'], 
					user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
					earliest_date = user_setting["email_earliest"], 
					latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
					insight_text = insight_text[insight_name]['screen_2'], 
					insight_data = insight_data[insight_name], 
					insight_name = insight_name,
					insight_mode = key_var['insight_mode'], 
					insight_title = insight_title[insight_name], 
					analysis_data = analysis_data,
					analysis_text_id = analysis_text_id,
					analysis_data_text = analysis_data_text,
					release_mode=key_var["intro_release"],
					scroll_mode=key_var['scroll_mode'])
		
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
def insight_c_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# initialize
		insight_name = flask.request.args.get('insight_name')
		
		# if insight exists
		if (insight_name in insight_data.keys()):
		
			# render
			return flask.render_template('insight/insight_c.html', user=key_var['user_name'],user_email=key_var['user'], 
				user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
				earliest_date = user_setting["email_earliest"], 
				latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
				insight_data = insight_data[insight_name], 
				insight_name = insight_name,
				insight_name_next = insight_name,
				insight_mode = key_var['insight_mode'], 
				insight_title = insight_title[insight_name], 
				next_page = 'insight_d_view',
				release_mode=key_var["intro_release"],
				scroll_mode=key_var['scroll_mode'])
		
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
def insight_d_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# define globals
		global key_var
	
		# initialize
		insight_name     = flask.request.args.get('insight_name')
		insight_current  = flask.request.args.get('insight_current')
		
		# define next insight
		if (key_var['current_insight']!=insight_current and key_var['next_insight']!="dashboard"):
		
			key_var['insight_intro_id']         = key_var['insight_intro_id'] + 1
			key_var['current_insight']          = insight_current
	
		if (key_var['insight_intro_id'] < len(insight_data['intro_insight_list'])):
			
			key_var['next_insight']             = insight_data['intro_insight_list'][key_var['insight_intro_id']]
		else: 

			key_var['next_insight'] 			= "dashboard"

		if (insight_name not in insight_data['sample_insight_list']):
	
			# if insight exists
			if (insight_name in insight_data.keys()):
	
				# render
				return flask.render_template('insight/insight_d.html', user=key_var['user_name'],user_email=key_var['user'], 
					user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
					earliest_date = user_setting["email_earliest"], 
					latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
					insight_data = insight_data[insight_name], 
					insight_name = insight_name,
					insight_name_next = key_var['next_insight'],
					insight_mode = key_var['insight_mode'], 
					insight_title = insight_title[insight_name],
					release_mode=key_var["intro_release"],
					scroll_mode=key_var['scroll_mode'])
	
			# if insight does not exist
			else:
	
				# render
				return flask.redirect(flask.url_for('insight_intro_view',insight_name = insight_name))
		
		else:
	
			if (key_var['insight_mode']=="intro"):
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
def insight_info_view():

	# access check
	if (access_check(access_level=4)) == True: 

		# define globals
		global key_var
	
		# initialize
		insight_name      = flask.request.args.get('insight_name')
		
		if insight_name in insight_data['add_info_list']:
			more_info          = True
			insight_text_extra = insight_text[insight_name]['screen_add']
		else:
			more_info          = False
			insight_text_extra = ""
	

		# render
		return flask.render_template('insight/insight_info.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'],timezone_utc_offset = timezone_utc_offset, timezone_utc_name = timezone_utc_name,
			earliest_date = user_setting["email_earliest"], 
			latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
			insight_text = insight_text[insight_name]['screen_1'], 
			insight_text_extra = insight_text_extra, 
			insight_name = insight_name, 
			insight_mode = key_var['insight_mode'], 
			insight_title = insight_title[insight_name],
			release_mode = key_var["intro_release"],
			more_info = more_info,
			scroll_mode=key_var['scroll_mode'])
	

	else: 

		# access denied 
		access_denied_url = access_denied()

		# render
		return flask.redirect(flask.url_for(access_denied_url))



# references
# ------------------------------------------------------------------------ #
@app.route('/references')
def references_view():

	if (access_check(access_level=1)) == True: 

		# render
		return flask.render_template('explore/references.html', 
			user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'],
			scroll_mode=key_var['scroll_mode'])

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
def intro_load_update_view():
	
	## NO ACCESS CHECK (BACKEND)

	# define globals
	global global_var
	global key_var
	
	# thread progress
	return flask.jsonify(
		dict(
			status = {
				'True': 'finished',
				'False': 'running',
				'Error': 'error'
				}[key_var['api_success']],
			status_email_load    = global_var['status_email_load'], 
			status_email_max     = global_var['status_email_max'],
			status_overview_load = global_var['status_overview_load'], 
			status_overview_max  = global_var['status_overview_max'],
			status_analysis_load = global_var['status_analysis_load'], 
			status_analysis_max  = global_var['status_analysis_max']	
		))

# insight_update
# ------------------------------------------------------------------------ #
@app.route('/insight_update')
def insight_update_view():

	## NO ACCESS CHECK (BACKEND)

	# obtain insight name & original page
	insight_name      = flask.request.args.get('insight_name')

	# regenerate insight
	insight_data[insight_name] = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_name, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=feature_data['email_date_df'], email_diff=user_setting['email_diff'], contact_df=feature_data['agg_contact_df'], user_name=key_var['user_name'], user_email=key_var['user'], email_range=user_setting['email_range'])

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
def error_view():

	## NO ACCESS CHECK (ERROR)

	# define globals
	global key_var

	# error message
	print("Error encountered")
	print(key_var['error'])

	# render
	return flask.render_template('misc/error.html', error_msg=key_var['error_msg'], user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'],
		scroll_mode=key_var['scroll_mode'])

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
