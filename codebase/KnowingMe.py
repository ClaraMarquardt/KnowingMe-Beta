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
global user_setting, app_setting, key_var

user_setting = user_setting_initialization()
app_setting  = app_setting_initialization()
key_var      = var_initialization()

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
from gmail_api_mod import get_email, overview_email, timeframe_email
from gmail_api_authentication_mod import gmail_oauth2callback, gmail_authentication, gmail_reauthentication

## analysis functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'analysis')))
from analysis_mod import analysis
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
def reset():

	# define globals
	global user_setting, app_setting, key_var

	# redefine variables
	user_setting = user_setting_initialization()
	app_setting  = app_setting_initialization()
	key_var      = var_initialization()

	# clear user data
	user_data_dir_clear(user_setting['output_dir'])

# intro_load_wrapper
# ---------------------------------------------#

# intro_load_overview_wrapper
# --------------------------------#
def intro_load_overview_wrapper(service, user, current_date, timelag_day, overview_day, birthday_day, email_max, min_day,output_dir):

	# define globals
	global key_var
	global user_setting

	# initialize
	key_var['api_success'] = 'False'

	# launch process
	try: 
	
		# email & birthday overview
		overview_email(service, user, current_date, timelag_day, overview_day, birthday_day, output_dir)

		# determine analysis timeframe
		user_setting['email_earliest'], user_setting['email_latest'], user_setting['email_diff'], user_setting['email_range']  = timeframe_email(current_date, timelag_day, min_day, overview_day, email_max, output_dir)

		# update thread status
		key_var['api_success'] = 'True'

	# error
	except Exception as e: 

		key_var['error']       = e
		key_var['error_msg']   = "Error Generating Email Overview > Try Restarting the App"
		key_var['api_success'] = 'Error'

# intro_load_email_wrapper
# --------------------------------#
def intro_load_email_wrapper(service, user, email_range, output_dir, current_date, user_email):

	# define globals
	global key_var

	# initialize
	key_var['api_success'] = 'False'

	# launch process
	try: 
			
		# emails
		get_email(service, user, email_range, output_dir, current_date, user_email)

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
	global sample_insight_data

	# initialize
	key_var['api_success'] = 'False'

	# launch process
	try: 
			
		# obtain email lists
		email_range_list = [str(datetime.datetime.strptime(x,'%m/%d/%Y').strftime('%m_%d_%Y')) for x in email_range]
		email_range_list = string.join(email_range_list,"|")

		email_array       = np.concatenate((glob.glob(os.path.join(output_dir,'inbox', 'email*.p')), 
			glob.glob(os.path.join(output_dir,'outbox', 'email*.p'))))
		email_array       = [x for x in email_array if bool(re.search(email_range_list,x))==True]
	
		email_array_other = (glob.glob(os.path.join(output_dir,'other', '*.p')))
		email_array_other = [x for x in email_array_other if bool(re.search(datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime('%m_%d_%Y'),x))==True]
		email_array_other = [x for x in email_array_other if bool(re.search('birthday|overview',x))==True]

		# data preparation 
		# -----------------------

		## main data preparation
		feature_data         = analysis(email_array, user, output_dir, current_date, earliest_date, latest_date)
		
		## other data preparation
		email_date_df = dict()
		for i in email_array_other:
			if bool(re.search('birthday',i))==True: 
				with open(i, "rb") as file:
					email_date_df['birthday'] = pickle.load(file)
			if bool(re.search('overview',i))==True: 
				with open(i, "rb") as file:
					email_date_df['overview'] = pickle.load(file)

		# feature generation 
		# -----------------------

		# feature lists
		nlp_feature_list        = ['sentiment', 'politeness', 'coordination']  
		simplelang_feature_list = ['talkative', 'lengthimbalance', 'birthday']
		nonlang_feature_list    = ['responsiveness', 'firstlast']
		feature_list            = [nlp_feature_list, simplelang_feature_list, nonlang_feature_list]
		feature_list            = sum(feature_list, [])

		# generate features
		feature_data['email_link_df'] = feature_wrapper_mod.generate_feature_wrapper(feature_list=feature_list, email_link_df=feature_data['email_link_df'], link_id=feature_data['email_link_df']['link_id'], msg_id=feature_data['email_link_df']['msg_id'], msg_threadid=feature_data['email_link_df']['msg_threadid'], msg_data=feature_data['msg_parsed'], link_data=feature_data['link_parsed'], conver_data=feature_data['conver_parsed'], msg_text_data=feature_data['msg_text_parsed'], contact_data=feature_data['contact_parsed'], email_date_df=email_date_df, current_date=current_date)
		
		# sample insight generation 
		# -----------------------

		# insight lists
		insight_list         = ['date_dist', 'time_dist','network', 'sample_sentiment']
		
		# generate sample insights
		sample_insight_data  = insight_wrapper_mod.generate_insight_wrapper(insight_list=insight_list, email_link_df=feature_data['email_link_df'], current_date=current_date, email_date_df=email_date_df, email_diff=email_diff, contact_df=feature_data['agg_contact_df'], user_name=user_name, user_email=user, email_range=email_range)

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

	# create user data folder (if it does not exist)
	if not os.path.exists(user_setting['output_dir']):
		os.makedirs(user_setting['output_dir'])
	
	# render
	return flask.render_template('onboarding/landing.html')

# home 
# ---------------------------------------------#
@app.route('/home')
def home_view():
	
	# define globals
	global user_setting
	global key_var

	# create user-specific user data folder (if it does not exist)
	user_setting['output_dir'] = os.path.join(user_setting['output_dir_base'], key_var['user'])
	if not os.path.exists(user_setting['output_dir']):
		os.makedirs(user_setting['output_dir'])

	user_data_dir_init(user_setting['output_dir'])

	# initialize contact groupings
	key_var['user_group_name_list_name'], key_var['user_group_name_list_address'] = contact_group_intialization(user_setting['output_dir'], 
		key_var['user_group_name_list_name'], key_var['user_group_name_list_address'])

	# render
	return flask.render_template('onboarding/home.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'])

# reset 
# ---------------------------------------------#
@app.route('/reset')
def reset_view():
	
	# reset
	reset()

	# display reset message
	flask.flash('App Succesfully Reset')

	# render
	return flask.render_template('onboarding/landing.html')


# Authentication
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# gmail_authentication 
# ---------------------------------------------#
@app.route('/gmail_authentication')
def gmail_authentication_view():

	# define globals
	global key_var

	# attempt to login
	login_success, login_data = gmail_authentication()

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
	
	elif (login_success=='Error'):
		
		key_var['error']         = login_data[0]
		key_var['error_msg']     = "Gmail Authentication Error > Try (a) Clearing your browser cache and/or (b) Restarting the application in an 'incognito' browser window"
		return flask.redirect(flask.url_for('error_view'))

# permission 
# ---------------------------------------------#
@app.route('/permission')
def permission_view():
	
	# render
	return flask.render_template('onboarding/permission.html', auth_url=flask.request.args.get('auth_url'))


# gmail_oauth2callback
# ---------------------------------------------#
@app.route('/gmail_oauth2callback')
def gmail_oauth2callback_view():

	# attempt to login
	authentication_success, authentication_data = gmail_oauth2callback()

	# re-route based on login success
	if (authentication_success=='authenticated'):

		return flask.redirect(flask.url_for('gmail_authentication_view'))
	
	elif (authentication_success=='unauthenticated'):
		
		auth_url = authentication_data[0]
		return flask.redirect(flask.url_for('permission_view', auth_url=auth_url))

# logout 
# ---------------------------------------------#
@app.route('/logout')
def logout_view():

	# reset 
	reset()

	# redirect to login page
	redirect_uri = flask.url_for('gmail_oauth2callback_view', _external=True)
	return flask.redirect(api_logout_url+redirect_uri)


# Intro
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# intro_load_a
# ---------------------------------------------#
@app.route('/intro_load_a')
def intro_load_a_view():

	# define globals
	global th
	global global_var

	# initialize
	global_var['status_overview_load']       = 0
	global_var['status_overview_max']        = 0

	# reauthenticate
	login_success, login_data = gmail_reauthentication()

	if (login_success=='logged_in'):
	
		# update credentials
		key_var['service']    = login_data['service']
		key_var['user']       = login_data['user'] 

		# launch processing thread
		th = Thread(target=intro_load_overview_wrapper, args=(key_var['service'], 'me', current_date,  user_setting['timelag_day'], user_setting['overview_day'], user_setting['birthday_day'], user_setting['email_max'], user_setting['min_day'],user_setting['output_dir']))
		th.start()

		return flask.render_template('intro/intro_load_a.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'])

	else:

		# flash message
		flask.flash('It looks like you will need to log-in again.')

		# return to log-in page
		return flask.url_for('gmail_authentication_view')

# intro_load_b
# ---------------------------------------------#
@app.route('/intro_load_b')
def intro_load_b_view():

	# define globals
	global th
	global global_var

	# initialize
	global_var['status_email_load']       = 0
	global_var['status_email_max']        = 0

	# reauthenticate
	login_success, login_data = gmail_reauthentication()

	if (login_success=='logged_in'):
	

		# launch processing thread
		th = Thread(target=intro_load_email_wrapper, args=(key_var['service'], 'me', user_setting['email_range'], user_setting['output_dir'], current_date, key_var['user']))
		th.start()

		return flask.render_template('intro/intro_load_b.html', user=key_var['user_name'],user_email=key_var['user'], 
			user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
			latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"])

	else:

		# flash message
		flask.flash('It looks like you will need to log-in again.')

		# return to log-in page
		return flask.url_for('gmail_authentication_view')

# intro_load_c
# ---------------------------------------------#
@app.route('/intro_load_c')
def intro_load_c_view():

	# define globals
	global th
	global global_var

	# initialize
	global_var['status_analysis_load']       = 0
	global_var['status_analysis_max']        = 0

	# launch processing thread
	th = Thread(target=intro_load_analysis_wrapper, args=(key_var['user'], key_var['user_name'], user_setting['email_range'], user_setting['email_diff'],user_setting['output_dir'], current_date, user_setting['email_earliest'],user_setting['email_latest']))
	th.start()

	return flask.render_template('intro/intro_load_c.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'])

# intro_load_update
# ---------------------------------------------#
@app.route('/intro_load_update')
def intro_load_update_view():
	
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

# intro_a
# ---------------------------------------------#
@app.route('/intro_a')
def intro_a_view():
	
	# prepare data
	email_count = sample_insight_data['date_dist']['graph_email_count']
	email_date  = sample_insight_data['date_dist']['graph_date']
	email_month = sample_insight_data['date_dist']['graph_month']

	email_date_subset           = sample_insight_data['date_dist']['graph_date_subset']
	email_count_subset          = sample_insight_data['date_dist']['graph_email_count_subset']
	email_count_sent_subset     = sample_insight_data['date_dist']['graph_email_count_sent_subset']
	email_count_received_subset = sample_insight_data['date_dist']['graph_email_count_received_subset']

	# render
	return flask.render_template('intro/intro_a.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'], earliest_date = user_setting["email_earliest"], 
		latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"], 
		email_count = email_count, email_date = email_date, email_month = email_month,
		email_date_subset = email_date_subset, email_count_subset = email_count_subset, 
		email_count_sent_subset = email_count_sent_subset, email_count_received_subset = email_count_received_subset)

# intro_b
# ---------------------------------------------#
@app.route('/intro_b')
def intro_b_view():

	print(sample_insight_data['time_dist'])

	# render
	return flask.render_template('intro/intro_b.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'],earliest_date = user_setting["email_earliest"], 
		latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"], 
		insight_dict = sample_insight_data['time_dist'])

# intro_c
# ---------------------------------------------#
@app.route('/intro_c')
def intro_c_view():

	print(sample_insight_data['network'])

	# render
	return flask.render_template('intro/intro_c.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'],earliest_date = user_setting["email_earliest"], 
		latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
		insight_dict = sample_insight_data['network'])

# intro_d
# ---------------------------------------------#
@app.route('/intro_d')
def intro_d_view():

	print(sample_insight_data['sample_sentiment'])

	# render
	return flask.render_template('intro/intro_d.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'],earliest_date = user_setting["email_earliest"], 
		latest_date = user_setting["email_latest"], date_diff=user_setting["email_diff"],
		insight_dict = sample_insight_data['sample_sentiment'])


# intro_final
# ---------------------------------------------#
@app.route('/intro_final')
def intro_final_view():

	# render
	return flask.render_template('intro/intro_final.html', user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'])

# # Explore
# # ------------------------------------------------------------------------ #
# # ------------------------------------------------------------------------ #

# # dashboard_intro
# # ------------------------------------------------------------------------ #
# @app.route('/dashboard_intro')
# def dashboard_intro_view():

# 	# render
# 	return flask.render_template('explore/dashboard_intro.html')

# # dashboard
# # ------------------------------------------------------------------------ #
# @app.route('/dashboard')
# def dashboard_view():

# 	# render
# 	return flask.render_template('explore/dashboard.html')

# # Setting
# # ------------------------------------------------------------------------ #
# # ------------------------------------------------------------------------ #

# # contact_group
# # ------------------------------------------------------------------------ #
# @app.route('/contact_group')
# def contact_group_view():

# 	# render
# 	return flask.render_template('setting/contact_group.html')

# # contact_group_new
# # ------------------------------------------------------------------------ #
# @app.route('/contact_group_new')
# def contact_group_new_view():

# 	# render
# 	return flask.render_template('setting/contact_group_new.html')

# # Insight
# # ------------------------------------------------------------------------ #
# # ------------------------------------------------------------------------ #

# # insight_intro
# # ------------------------------------------------------------------------ #
# @app.route('/insight_intro_<insight_name>')
# def insight_intro_view():

# 	# generate insight

# 	# render
# 	return flask.render_template('explore/insight_intro.html')

# # insight
# # ------------------------------------------------------------------------ #
# @app.route('/insight_<insight_name>')
# def insight_view():

# 	# render
# 	return flask.render_template('explore/insight.html')

# Misc
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# error
# ------------------------------------------------------------------------ #
@app.route('/error')
def error_view():

	# define globals
	global key_var

	# error message
	print("Error encountered")
	print(key_var['error'])

	# render
	return flask.render_template('misc/error.html', error_msg=key_var['error_msg'], user=key_var['user_name'],user_email=key_var['user'], 
		user_photo=key_var['user_photo'])


# ------------------------------------------------------------------------ #
# Launch App                
# ------------------------------------------------------------------------ #

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
