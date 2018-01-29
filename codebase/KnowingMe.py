#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Setup & Main Interface Script
# Date:        August 2017
# Language:    Python (.py) [ Python 2.7 ]

#----------------------------------------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))   
print(app_root)

user_setting_file  = os.path.normpath(os.path.join(app_root,'setup','user_setting.json'))

# Dependencies - External
#---------------------------------------------#

## ignore warnings
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="Not importing directory '/KnowingMe/codebase/code/misc'")

## import
from __init__ import *
from __init_var__ import *

user_setting, sample_setting  = user_setting_initialization()
api_success, feature_success, user_name, user_photo, internal_email_id, link_id_store, user, user_group_1_store, user_group_2_store,user_group_na_store,user_group_1,user_group_2,user_group_na,user_group_name,user_group_name_a,user_group_name_b,user_group_name_basis, user_group_name_list_address, user_group_name_list_name= var_initialization(user_setting)

## app setting
app_setting = dict()
app_setting['app_port']  = int(os.getenv("PORT", "8000"))
app_setting['app_debug'] = int(str(os.getenv("DEBUG", "False"))=='True')


# Dependencies - Internal
#---------------------------------------------#

## setup 
sys.path.append(os.path.normpath(os.path.join(app_root,'code','setup')))
from server import flask_initialize

## backend functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'backend')))
from gmail_api_fun import get_email_batch

## nlp functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'nlp')))
from insight_fun import insight_generation
from nlp_helper import *

## frontend functions
sys.path.append(os.path.normpath(os.path.join(app_root,'code', 'frontend')))
from insight_agg_fun import insight_agg
from frontend_helper import *

## global 
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

#----------------------------------------------------------------------------#
# Start Servers, etc. (ONLY UPON INITIAL LOADING)
#----------------------------------------------------------------------------#

if (((os.environ.get("WERKZEUG_RUN_MAIN")==False) or (pd.isnull(os.environ.get("WERKZEUG_RUN_MAIN")))) and (app_setting['app_debug']==True)):
	
	print("Launching")
	
else:

	print("Restarting")
	url = 'http://localhost:' + str(app_setting['app_port'])

	webbrowser.open_new(url)
	

#----------------------------------------------------------------------------#
# Initialize & Launch Application
#----------------------------------------------------------------------------#

print("Initialize & Launching Application - KnowingMe")
app = flask_initialize(debug=app_setting['app_debug'], secret_key=secret_key, app_static=app_static, app_template=app_template)

#----------------------------------------------------------------------------#
#                           OAuth2 Authentication                            #
#----------------------------------------------------------------------------#

### PERSONAL EMAIL MODE

## landing
@app.route('/gmail_authentication')
def gmail_authentication():

	# global variable initialization
	global service
	global user
	global user_name
	global user_photo
	
	# function
	try: 
		if 'credentials' not in flask.session:
			return flask.redirect(flask.url_for('oauth2callback'))
		credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
		if credentials.access_token_expired:
			return flask.redirect(flask.url_for('oauth2callback'))
		else:
			http_auth      = credentials.authorize(httplib2.Http())
			service        = discovery.build('gmail', 'v1', http=http_auth)
			service_people = discovery.build('people', 'v1', http=http_auth)
			user      = service.users().getProfile(userId='me').execute()['emailAddress']
			print(user)	
			user_name = service_people.people().get(resourceName="people/me",personFields='names').execute()['names'][0]['givenName']
			user_photo = service_people.people().get(resourceName="people/me",personFields='photos').execute()['photos']
			user_photo = [x['url'] for x in user_photo]
			if len(user_photo)>0:
				user_photo_temp = [x for x in user_photo if bool(re.match('.*AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M.*',x))==False]
				if len(user_photo_temp)==0:
					user_photo = user_photo[0]
				else:
					user_photo = user_photo_temp[0]
			else:
				user_photo = user_photo[0]
		
			return flask.redirect(flask.url_for('welcome'))	

	except Exception as e: 

		print('Error Encountered')
		print(e)

		error_msg = "Gmail Authentication Error > Try (a) Clearing your browser cache and/or (b) Restarting the application in an 'incognito' browser window"
	
		return flask.render_template('error.html', error_msg=error_msg)


## oauth2
@app.route('/oauth2callback')
def oauth2callback():
	flow = client.flow_from_clientsecrets(
	api_auth_file,
	scope=api_auth_scope,
	redirect_uri=flask.url_for('oauth2callback', _external=True))
	if 'code' not in flask.request.args:
		auth_url = flow.step1_get_authorize_url()
		return flask.redirect(auth_url)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return flask.redirect(flask.url_for('gmail_authentication'))

## landing
@app.route('/gmail_reauthentication')
def gmail_reauthentication():

	# global variable initialization
	global service
	global user
	global user_name
	global user_photo
	
	# function
	try: 

		credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
		http_auth = credentials.authorize(httplib2.Http())
		service   = discovery.build('gmail', 'v1', http=http_auth)
		service_people = discovery.build('people', 'v1', http=http_auth)
		user      = service.users().getProfile(userId='me').execute()['emailAddress']
		print(user)	
		user_name  = service_people.people().get(resourceName="people/me",personFields='names').execute()['names'][0]['givenName']		
		user_photo = service_people.people().get(resourceName="people/me",personFields='photos').execute()['photos']
		user_photo = [x['url'] for x in user_photo]
		if len(user_photo)>0:
			user_photo_temp = [x for x in user_photo if bool(re.match('.*AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M.*',x))==False]
			if len(user_photo_temp)==0:
				user_photo = user_photo[0]
			else:
				user_photo = user_photo_temp[0]
		else:
			user_photo = user_photo[0]		
		return flask.redirect(flask.url_for('launch'))	

	except Exception as e: 

		print('Error Encountered')
		print(e)

		error_msg = "Gmail Authentication Error > Try (a) Clearing your browser cache and/or (b) Restarting the application in an 'incognito' browser window"
	
		return flask.render_template('error.html', error_msg=error_msg)


	
## landing
@app.route('/gmail_authentication_sample')

def gmail_authentication_sample():

	# global variable initialization
	global user

	# function
	user = user_setting['sample_user']

	return flask.redirect(flask.url_for('launch'))

#----------------------------------------------------------------------------#
#                           Helper Functions                                 #
#----------------------------------------------------------------------------#
## get_email_batch_wrapper
def get_email_batch_wrapper(service, user_id, earliest_date, latest_date, output_dir, excl_non_personal_email, excl_archived_email, extract_email_lim, mode="data"):

	# global variable initialization
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global feat_df_dict
	global agg_contact_df
	global volume_df
	global api_success
	global feature_success
	global run_time_feature
	global user_setting
	global error_msg
	global email_array
	global email_array_other

	api_success = 'False'

	try: 
	
		# function
		email_batch_data = get_email_batch(service, 'me', earliest_date, 
			latest_date, user_setting['output_dir'],user_setting['excl_non_personal_email'], user_setting['excl_archived_email'], user_setting['extract_email_lim'], mode)
	
		# parse data returned
		error_count    = email_batch_data[0]
		excluded_count = email_batch_data[1]
		run_time       = email_batch_data[2]

		## feature creation 
		email_array=np.concatenate((glob.glob(os.path.join(user_setting['output_dir'],'inbox', 'email*.json')), 
			glob.glob(os.path.join(user_setting['output_dir'],'outbox', 'email*.json'))))
		email_array_date = [datetime.datetime.strptime(user_setting['latest_date'],'%m/%d/%Y') - datetime.timedelta(days=x) for x in range(0,user_setting['date_diff']+1)]
		email_array_date = [x.strftime('%m_%d_%Y') for x in email_array_date]
		email_array_date = string.join(email_array_date,"|")
		email_array = [x for x in email_array if bool(re.search(email_array_date,x))==True]
		email_array_other=glob.glob(os.path.join(user_setting['output_dir'],'other', 'date*.json'))

		if user_setting["process_email_lim"]!='False':
			lim = np.min([len(email_array),int(user_setting["process_email_lim"])])
			random.shuffle(email_array)
			email_array=email_array[0:lim]

		# check that emails exist
		if len(email_array)==0:
		
			error_msg = "No extracted emails to process (* Try rerunning with 'use_stored'=False)"
			api_success = 'error'

		else:
		
			## print status update
			print('Number of Emails - Parsed Successfully: ' + str(len(email_array)))
			api_success = 'True'

	except Exception as e: 

		error_msg = e
		api_success = 'error'

## get_email_batch_wrapper
def get_email_batch_wrapper_overview(service, user_id, earliest_date, latest_date, output_dir, excl_non_personal_email, excl_archived_email, extract_email_lim, mode="data"):

	# global variable initialization
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global feat_df_dict
	global agg_contact_df
	global volume_df
	global api_success
	global feature_success
	global run_time_feature
	global user_setting
	global error_msg
	global email_array
	global email_array_other

	api_success = 'False'

	try: 
	
		# function
		email_batch_data = get_email_batch(service, 'me', earliest_date, 
			latest_date, user_setting['output_dir'],user_setting['excl_non_personal_email'], user_setting['excl_archived_email'], user_setting['extract_email_lim'], mode)

		## feature creation 
		email_array_other=glob.glob(os.path.join(user_setting['output_dir'],'other', 'date_year*.json'))

		# check that emails exist
		if len(email_array_other)==0:
		
			error_msg = "No extracted emails to process (* Try rerunning with 'use_stored'=False)"
			api_success = 'error'

		else:
		
			## print status update
			print('Number of Emails - Parsed Successfully: )')
			api_success = 'True'

	except Exception as e: 

		error_msg = e
		api_success = 'error'

## get_email_batch_wrapper
def feature_wrapper(email_array, email_array_other, user):

	# global variable initialization
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global feat_df_dict
	global agg_contact_df
	global volume_df
	global api_success
	global feature_success
	global run_time_feature
	global user_setting
	global error_msg

	feature_success = 'False'

	feat_df_all, feat_df_dict, agg_contact_df, volume_df, run_time_feature = insight_generation(email_array,email_array_other, user)
	feat_df = feat_df_all[feat_df_all['excluded']==0]

	if user_setting['dev_mode']=='True':
			
			feat_df.to_csv(os.path.join(user_setting['output_dir'], 'feat_df.csv'), encoding="utf8")
			
			agg_contact_df.to_csv(os.path.join(user_setting['output_dir'], 'agg_contact_df.csv'), encoding="utf8")
			
			volume_df_tmp = pd.DataFrame.from_dict(volume_df, orient="index")
			volume_df_tmp.to_csv(os.path.join(user_setting['output_dir'], 'volume_df.csv'), encoding="utf8")
	
	## format
	agg_contact_df          = agg_contact_df[~agg_contact_df['contact'].str.contains(user)]
	agg_contact_df          = agg_contact_df[~agg_contact_df['contact'].str.contains("//")]

	feature_success = 'True'

## get_email_batch_wrapper_sample
def get_email_batch_wrapper_sample():

	# global variable initialization
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global feat_df_dict
	global agg_contact_df
	global error_msg
	global volume_df
	global api_success
	global feature_success
	global run_time_feature
	global email_array
	global email_array_other

	api_success = 'False'

	if user_setting['personal_email']=='False':

		error_count    = 0
		excluded_count = 0
		run_time       = '/'
		email_array_other    = []
	
	elif user_setting['personal_email']=='True':

		error_count    = "/"
		run_time       = "/"
		email_array_other=glob.glob(os.path.join(user_setting['output_dir'],'other', 'date*.json'))
	
	## feature creation
	email_array=np.concatenate((glob.glob(os.path.join(user_setting['output_dir'],'inbox', 'email*.json')), 
		glob.glob(os.path.join(user_setting['output_dir'],'outbox', 'email*.json'))))
	
	if user_setting["process_email_lim"]!='False':
		lim   = np.min([len(email_array),int(user_setting["process_email_lim"])])
		random.shuffle(email_array)
		email_array=email_array[0:lim]

	# check that emails exist
	if len(email_array)==0:
		
		error_msg = "No extracted emails to process (* Try rerunning with 'use_stored'=False)"
		api_success = 'error'

	else:
		
		## print status update
		print('Number of Emails - Parsed Successfully: ' + str(len(email_array)))
		api_success = 'True'


def reset_all():

	global user_setting
	global sample_setting
	global api_success
	global reset
	global feature_success
	global user_name
	global user_photo
	global internal_email_id
	global link_id_store
	global user
	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis
	global user_group_name_list_address
	global user_group_name_list_name

	reset_path                    = os.path.join(app_root,'setup','exec_reset.sh')
	user_setting, sample_setting  = user_setting_initialization()

	# logout
	api_success, feature_success, user_name, user_photo, internal_email_id, link_id_store, user, user_group_1_store, user_group_2_store,user_group_na_store,user_group_1,user_group_2,user_group_na,user_group_name,user_group_name_a,user_group_name_b,user_group_name_basis, user_group_name_list_address, user_group_name_list_name= var_initialization(user_setting)
	# user reset
	if os.path.exists(user_setting['output_dir']):
		def purge(dir, pattern):
			files = sum([y for x in os.walk(dir) for y in [glob.glob(os.path.join(x[0], '*.'+e)) for e in pattern]],[])
			for f in files:
				os.remove(f)
		purge(user_setting['output_dir'], ["log","json","csv", "txt"])
	
	# system reset
	os.system(reset_path)

	print("reset")



#----------------------------------------------------------------------------#
#                             Main Views                                     #
#----------------------------------------------------------------------------#

@app.route('/')
def home():

	global user_setting
	# create folders

	if not os.path.exists(user_setting['output_dir']):
		os.makedirs(user_setting['output_dir'])
	
	return flask.render_template('home.html')

## welcome
#---------------------------
@app.route('/welcome')
def welcome():
	global user

	global user_setting
	global user_group_name_list_name
	global user_group_name_list_address

	if not os.path.exists(os.path.join(user_setting['output_dir'], user)):
		os.makedirs(os.path.join(user_setting['output_dir'], user))

	user_setting['output_dir'] = os.path.join(user_setting['output_dir_base'], user)

	if not os.path.exists(os.path.join(user_setting['output_dir'], "inbox")):
		os.makedirs(os.path.join(user_setting['output_dir'], "inbox"))
	if not os.path.exists(os.path.join(user_setting['output_dir'], "outbox")):
		os.makedirs(os.path.join(user_setting['output_dir'], "outbox"))
	if not os.path.exists(os.path.join(user_setting['output_dir'], "other")):
		os.makedirs(os.path.join(user_setting['output_dir'], "other"))

	contact_path = glob.glob(os.path.join(user_setting['output_dir'],'contact_df_*.csv'))
	contact_path = [re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4",x) for x in contact_path]
	contact_path = [x for x in contact_path if bool(re.match("\*",x))==False]

	user_group_name_list_name_temp = []
	for i in contact_path:
		user_group_name_list_name_temp.append(i)

	if (len(user_group_name_list_name_temp)>0):
		user_group_name_list_name_temp = list(set(user_group_name_list_name_temp))
		user_group_name_list_address_temp = ['/user_group_load_' + x for x in user_group_name_list_name_temp]	

		for i in user_group_name_list_name_temp:
			user_group_name_list_name.append(i)
		for i in user_group_name_list_address_temp:
			user_group_name_list_address.append(i)
	
	return flask.render_template('welcome.html', user=user_name ,user_email=user, user_photo=user_photo)

# reset
#---------------------------
@app.route('/reset')
def reset():
	
	reset_all()
	flask.flash('App Succesfully Reset')
	return flask.render_template('home.html')

@app.route('/logout')
def logout():

	reset_all()

	return flask.redirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http%3A%2F%2Flocalhost%3A8000%2Foauth2callback')



## user_setting
#---------------------------

@app.route('/user_setting_init', methods=['GET', 'POST'])
def user_setting_init():

	global user_setting
	global sample_setting
	global email_array_other


	current_date                               = datetime.datetime.now().strftime("%m_%d_%Y")
	email_count                   			   = load.load_date(email_array_other, verbose=False,mode="mdy")[current_date]
	[email_count_date, email_count_count]      = freq.date_agg(email_count)
	email_count_count = [x-1 for x in email_count_count]
	email_count_month                          = [parser.parse(x).month-1 for x in email_count_date]

	# form
	return flask.render_template('user_setting.html', 
		personal_email=int(user_setting['personal_email']=='True'), 
		use_stored=int(user_setting['use_stored']=='True'), 
		earliest_date=user_setting['earliest_date'] , 
		latest_date=user_setting['latest_date'] , 
		excl_non_personal_email=int(user_setting['excl_non_personal_email']=='True'),
		excl_archived_email=int(user_setting['excl_archived_email']=='True'), 
		max_contact=user_setting['max_contact'], 
		output_dir=user_setting['output_dir'],
		dev_mode=int(user_setting['dev_mode']=='True'), 
		process_email_lim=user_setting['process_email_lim'],
		extract_email_lim=user_setting['extract_email_lim'], 
		email_count_count=email_count_count,
		email_count_date=email_count_date,
		email_count_month=email_count_month, 
		email_lim=250)

@app.route('/user_setting_store', methods=['POST','GET'])
def user_setting_store():

	# initialize
	global user_setting
	global sample_setting

	# updates settings
	user_setting['earliest_date']           = flask.request.form.get('earliest_date')
	user_setting['latest_date']             = flask.request.form.get('latest_date')


	user_setting['earliest_date']           = re.sub("(.*)( )(\(.*\))$", "\\1",user_setting['earliest_date'])	
	user_setting['latest_date']             = re.sub("(.*)( )(\(.*\))$", "\\1",user_setting['latest_date'])

	user_setting['earliest_date'] 			= parser.parse(user_setting['earliest_date'])
	user_setting['earliest_date'] 			= str(user_setting['earliest_date'].month) + '/' + str(user_setting['earliest_date'].day) + '/' + str(user_setting['earliest_date'].year)
	user_setting['latest_date'] 			= parser.parse(user_setting['latest_date'])
	user_setting['latest_date'] 			= str(user_setting['latest_date'].month) + '/' + str(user_setting['latest_date'].day) + '/' + str(user_setting['latest_date'].year)

	print(user_setting)
	
	## update settings
	user_setting['date_diff']               = int((parser.parse( user_setting['latest_date']) - parser.parse( user_setting['earliest_date'])).days)

	if user_setting['personal_email']=='False':
	
		user_setting['earliest_date']       = sample_setting['earliest_date']
		user_setting['latest_date']         = sample_setting['latest_date']
		user_setting['date_diff']           = sample_setting['date_diff']
		user_setting['sample_user']         = sample_setting['user']   

	# store the updated settings	
	user_setting_tmp                   = dict(user_setting)
	user_setting_tmp['output_dir']     = user_setting_tmp['output_dir_raw']
	del_key = ['sample_user','user', 'date_diff','output_dir_raw']
	for x in del_key:
		if x in user_setting_tmp.keys():
			del user_setting_tmp[x]
	
	with open(user_setting_file_user, 'w') as out_file:
			json.dump(user_setting_tmp, out_file, indent=4)

	# load page
	if user_setting['personal_email']=='True':
		return flask.redirect(flask.url_for('gmail_reauthentication'))
	else: 
		return flask.redirect(flask.url_for('gmail_reauthentication'))

## launch
#---------------------------

@app.route('/launch', methods=['GET', 'POST'])
def launch():

	global th
	global feature_success
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global agg_contact_df
	global user
	global user_setting
	global email_array
	global email_array_other

	api_success = 'False'

	print('Launching Pipeline')
	if  user_setting['personal_email']=='True' and user_setting['use_stored']=='False':
	
		th = Thread(target=get_email_batch_wrapper, args=(service, 'me', user_setting['earliest_date'], 
		user_setting['latest_date'], user_setting['output_dir'],user_setting['excl_non_personal_email'], user_setting['excl_archived_email'], user_setting['extract_email_lim']))
		th.start()

		## redirect
		return flask.render_template('process_email.html', use_stored=user_setting['use_stored'])

	else:

		user_setting['use_stored']='True'
		th = Thread(target=get_email_batch_wrapper_sample, args=())
		th.start()

		## redirect
		return flask.render_template('process_email.html', use_stored=user_setting['use_stored'])


@app.route('/status_email')
def thread_status():
	global global_var
	return flask.jsonify(
		dict(
			status = {
				'True': 'finished',
				'False': 'running',
				'error': 'error'
				}[api_success],
			status_email_load = global_var['status_email_load'], 
			status_email_max = global_var['status_email_max'],
			status_email_max_new = global_var['status_email_max_new']
		))

@app.route('/status_feature')
def feature_status():
	return flask.jsonify(
		dict(
			status = {
				'True': 'finished',
				'False': 'running',
				'error': 'error'
				}[feature_success],
			status_feature = global_var['status_feature']
	))

@app.route('/process_feature')
def process_feature():

	global email_array
	global email_array_other

	global user
	
	th2 = Thread(target=feature_wrapper, args=(email_array, email_array_other, user))
	th2.start()

	## redirect
	return flask.render_template('process_feature.html')

@app.route('/error')
def error():
	
	global error_msg

	## redirect
	return flask.render_template('error.html', error_msg=error_msg)

## launch_overview
#---------------------------

@app.route('/launch_overview', methods=['GET', 'POST'])
def launch_overview():

	global th
	global feature_success
	global error_count
	global excluded_count
	global run_time
	global feat_df
	global feat_df_all
	global agg_contact_df
	global user
	global user_setting
	global email_array
	global email_array_other

	api_success = 'False'

	print('Launching Pipeline')

	now           = datetime.datetime.now()
	date_today    = now.strftime("%m/%d/%Y")
	date_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%m/%d/%Y")

	email_array_other=glob.glob(os.path.join(user_setting['output_dir'],'other', 'date_year*.json'))
	current_date = datetime.datetime.now().strftime("%m_%d_%Y")
	year_date_filename=os.path.normpath(os.path.join(user_setting['output_dir'], "other", 'date_year_'+current_date+'.json'))

	if not os.path.exists(year_date_filename): 
		th = Thread(target=get_email_batch_wrapper_overview, args=(service, 'me',date_year_ago, 
		date_today, user_setting['output_dir'],user_setting['excl_non_personal_email'], user_setting['excl_archived_email'], user_setting['extract_email_lim'], "count"))
		th.start()

		## redirect
		return flask.render_template('process_email_overview.html')

	else: 

		## redirect
		return flask.redirect(flask.url_for('user_setting_init'))

@app.route('/status_email_overview')
def thread_status_overview():
	global global_var
	return flask.jsonify(
		dict(
			status = {
				'True': 'finished',
				'False': 'running',
				'error': 'error'
				}[api_success],
			status_email_overview_load = global_var['status_email_overview_load'], 
			status_email_overview_max = global_var['status_email_overview_max']
		))

## user_group
#---------------------------

@app.route('/user_group_agg', methods=['GET','POST'])
def user_group_agg():
	
	global agg_contact_df
	global user_group_1_store
	global user_group_2_store
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	if (len(user_group_1_store)==0):
		user_group_name        = "**Blank_Default"
		user_group_name_a      = "Group A"
		user_group_name_b      = "Group B"
		user_group_name_basis  = "**Blank_Default"

	# sort
	agg_contact_df          = agg_contact_df.sort_values(by=['freq_agg','contact'], ascending=[False,True])
	agg_contact_df.reset_index(inplace=True,drop=True)
	agg_contact_df_tmp      = agg_contact_df[0:np.min([user_setting['max_contact'], len(agg_contact_df)])]

	user_group_name_list_id = range(0,len(user_group_name_list_name))

	user_group_1_store = [x for x in user_group_1_store if x in agg_contact_df_tmp['contact'].tolist()]
	user_group_2_store = [x for x in user_group_2_store if x in agg_contact_df_tmp['contact'].tolist()]




	# form
	return flask.render_template('user_group.html', contact_id=range(0, len(agg_contact_df_tmp)), contact=agg_contact_df_tmp['contact'].tolist(), 
		freq=agg_contact_df_tmp['freq_agg'], name=agg_contact_df_tmp['contact_name'], order="OVERALL", 
		user_group_1_store=user_group_1_store,user_group_2_store=user_group_2_store, 
		user_group_name=user_group_name, user_group_name_a=user_group_name_a, user_group_name_b=user_group_name_b, 
		user_group_name_list_id=user_group_name_list_id, 
		user_group_name_list_address=user_group_name_list_address, 
		user_group_name_list_name=user_group_name_list_name,
		new_cat='True')

@app.route('/user_group_inbox', methods=['GET','POST'])
def user_group_inbox():
	
	global agg_contact_df
	global user_group_1_store
	global user_group_2_store
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	if (len(user_group_1_store)==0):
		user_group_name        = "**Blank_Default"
		user_group_name_a      = "Group A"
		user_group_name_b      = "Group B"
		user_group_name_basis  = "**Blank_Default"
	
	# sort
	agg_contact_df       = agg_contact_df.sort_values(by=['freq_inbox','contact'], ascending=[False,True])
	agg_contact_df.reset_index(inplace=True,drop=True)
	agg_contact_df_tmp   = agg_contact_df[0:np.min([user_setting['max_contact'], len(agg_contact_df)])]

	user_group_name_list_id = range(0,len(user_group_name_list_name))

	user_group_1_store = [x for x in user_group_1_store if x in agg_contact_df_tmp['contact'].tolist()]
	user_group_2_store = [x for x in user_group_2_store if x in agg_contact_df_tmp['contact'].tolist()]



	# form
	return flask.render_template('user_group.html', contact_id=range(0, len(agg_contact_df_tmp)), contact=agg_contact_df_tmp['contact'].tolist(), 
		freq=agg_contact_df_tmp['freq_inbox'], name=agg_contact_df_tmp['contact_name'], order="INBOX",
		user_group_1_store=user_group_1_store,user_group_2_store=user_group_2_store, 
		user_group_name=user_group_name, user_group_name_a=user_group_name_a, user_group_name_b=user_group_name_b, 
		user_group_name_list_id=user_group_name_list_id, 
		user_group_name_list_address=user_group_name_list_address, 
		user_group_name_list_name=user_group_name_list_name,
		new_cat='True')

@app.route('/user_group_outbox', methods=['GET','POST'])
def user_group_outbox():
	
	global agg_contact_df
	global user_group_1_store
	global user_group_2_store
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	if (len(user_group_1_store)==0):
		user_group_name        = "**Blank_Default"
		user_group_name_a      = "Group A"
		user_group_name_b      = "Group B"
		user_group_name_basis  = "**Blank_Default"
	# sort
	agg_contact_df       = agg_contact_df.sort_values(by=['freq_outbox', 'contact'], ascending=[False,True])
	agg_contact_df.reset_index(inplace=True,drop=True)
	agg_contact_df_tmp   = agg_contact_df[0:np.min([user_setting['max_contact'], len(agg_contact_df)])]

	user_group_name_list_id = range(0,len(user_group_name_list_name))

	user_group_1_store = [x for x in user_group_1_store if x in agg_contact_df_tmp['contact'].tolist()]
	user_group_2_store = [x for x in user_group_2_store if x in agg_contact_df_tmp['contact'].tolist()]



	# form
	return flask.render_template('user_group.html',contact_id=range(0, len(agg_contact_df_tmp)), contact=agg_contact_df_tmp['contact'].tolist(), 
		freq=agg_contact_df_tmp['freq_outbox'], name=agg_contact_df_tmp['contact_name'], order="OUTBOX",
		user_group_1_store=user_group_1_store,user_group_2_store=user_group_2_store, 
		user_group_name=user_group_name, user_group_name_a=user_group_name_a, user_group_name_b=user_group_name_b, 
		user_group_name_list_id=user_group_name_list_id, 
		user_group_name_list_address=user_group_name_list_address, 
		user_group_name_list_name=user_group_name_list_name,
		new_cat='True')

@app.route('/user_group_new', methods=['GET','POST'])
def user_group_new():

	global user_group_1
	global user_group_2

	user_group_1=flask.request.form.getlist('user_group_1')
	user_group_2=flask.request.form.getlist('user_group_2')


	if len(user_group_1)>0 and len(user_group_2)>0 and len([x for x in user_group_1 if x in user_group_2])==0:
		if len(set(user_group_1).symmetric_difference(set(user_group_1_store)))>0 or len(set(user_group_2).symmetric_difference(set(user_group_2_store)))>0:

			user_group_name_temp = re.sub("\*\*","",user_group_name)
			return flask.render_template('user_group_new.html',user_group_name=user_group_name_temp, user_group_name_a=user_group_name_a, user_group_name_b=user_group_name_b, 
				user_group_name_basis=user_group_name_basis)

		else: 

			return flask.redirect(flask.url_for('user_group_store'))

	else:
		flask.flash('Invalid Selection')

		return flask.redirect(flask.url_for('user_group_agg'))


@app.route('/user_group_store_rand', methods=['GET','POST'])
def user_group_store_rand():

	global user_group_1 
	global user_group_2
	global user_group_na
	global user_group_uncat
	global agg_contact_df
	global feat_df
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	user_group_name = "**Random_Default"
	user_group_name_a = "Group A"
	user_group_name_b = "Group B"
	user_group_name_basis = "**Random_Default"

	# sort
	agg_contact_df         = agg_contact_df.sort_values(by=['freq_agg','contact'], ascending=[False,True])
	agg_contact_df.reset_index(inplace=True,drop=True)
	agg_contact_df_contact = np.array(agg_contact_df['contact'].unique())
	agg_contact_df_tmp     = agg_contact_df[0:np.min([user_setting['max_contact'], len(agg_contact_df)])]

	overall_contact        = feat_df['link_contact'].unique()

	# randomise
	user_group_1_set = np.array(random.sample(agg_contact_df_tmp.index, int(math.ceil(np.min([user_setting['max_contact'],len(agg_contact_df)])/2))))
	agg_contact_df_tmp.loc[agg_contact_df_tmp.index.tolist(),'group_tmp'] = 0
	agg_contact_df_tmp.loc[user_group_1_set,'group_tmp'] = 1

	user_group_1     	= np.array(agg_contact_df_tmp[agg_contact_df_tmp['group_tmp']==1]['contact'])
	user_group_2     	= np.array(agg_contact_df_tmp[agg_contact_df_tmp['group_tmp']==0]['contact'])
	user_group_na    	= agg_contact_df_contact[np.array([x not in user_group_1 and x not in user_group_2 for x in agg_contact_df_contact])]
	user_group_uncat    = overall_contact[np.array([x not in user_group_1 and x not in user_group_2 and x not in user_group_na for x in overall_contact])]


	if len(user_group_1)>0 and len(user_group_2)>0:

		# store (for later loading)
		user_group_df_1       = pd.DataFrame({'user_group_1':user_group_1})
		user_group_df_2       = pd.DataFrame({'user_group_2':user_group_2})
		user_group_df_na      = pd.DataFrame({'user_group_na':user_group_na})
		user_group_df_uncat   = pd.DataFrame({'user_group_uncat':user_group_uncat})
		user_group_df         = pd.concat([user_group_df_1,user_group_df_2], ignore_index=True, axis=1)
		user_group_df         = pd.concat([user_group_df,user_group_df_na], ignore_index=True, axis=1)
		user_group_df         = pd.concat([user_group_df,user_group_df_uncat], ignore_index=True, axis=1)
		user_group_df.columns = ['user_group_1','user_group_2','user_group_na','user_group_uncat']
		user_group_df.to_csv(os.path.join(user_setting['output_dir'], 'contact_df.csv'))

		if user_setting['dev_mode']=='True':
			user_group_df.to_csv(os.path.join(user_setting['output_dir'], 'user_group_df.csv') , encoding="utf8")

		return flask.redirect(flask.url_for('birthday'))
	else:
		return flask.redirect(flask.url_for('user_group_agg'))

@app.route('/user_group_update', methods=['GET','POST'])
def user_group_update():
	
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis
	global user_group_name_list_name
	global user_group_name_list_address

	contact_path = glob.glob(os.path.join(user_setting['output_dir'],'contact_df_*.csv'))
	contact_path_stem = [re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4_\\5_\\6_\\7",x) for x in contact_path]
	contact_path_subset = [re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4",x) for x in contact_path]

	user_group_name_temp=flask.request.form.get('user_group_name')
	user_group_name_a_temp=flask.request.form.get('user_group_name_a')
	user_group_name_b_temp=flask.request.form.get('user_group_name_b')
	user_group_name_basis_temp=flask.request.form.get('user_group_name_basis')
	user_group_name_temp_comb = user_group_name_temp+'_'+user_group_name_a_temp+'_'+user_group_name_b_temp+'_'+user_group_name_basis_temp

	print(user_group_name_temp)
	if (bool(re.match(".*\*.*",user_group_name_temp))==False) and (bool(re.match(".* .*",user_group_name_temp))==False) and (bool(re.match(".*\$.*",user_group_name_temp))==False):

		if (user_group_name_temp not in contact_path_subset) or (user_group_name_temp_comb in contact_path_stem): 

			user_group_name=flask.request.form.get('user_group_name')
			user_group_name_a=flask.request.form.get('user_group_name_a')
			user_group_name_b=flask.request.form.get('user_group_name_b')

			if user_group_name not in user_group_name_list_name:
				user_group_address = '/user_group_load_' + user_group_name
				user_group_name_list_name.append(user_group_name)
				user_group_name_list_address.append(user_group_address)

			# form
			return flask.redirect(flask.url_for('user_group_store'))

		else:

			flask.flash('Contact group with this name already exists. \nEither leave all fields unchanged to overwrite OR change the name to create a new contact group.')
			return flask.redirect(flask.url_for('user_group_agg'))

	else: 

		flask.flash('Invalid contact group name. \nNames cannot contain any of the following: " ", "$"" or "*"')
		return flask.redirect(flask.url_for('user_group_agg'))


@app.route('/user_group_load', methods=['GET','POST'])
def user_group_load():

	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_uncat_store
	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	# load (for later loading)

	if os.path.exists(os.path.join(user_setting['output_dir'],'contact_df_recent.txt')):

		with open(os.path.join(user_setting['output_dir'],'contact_df_recent.txt')) as file:  
			recent_path = file.read() 
		if (os.path.exists(os.path.join(user_setting['output_dir'],recent_path)) and len(recent_path)>0):
		
			user_group_df          = pd.read_csv(os.path.join(user_setting['output_dir'],recent_path))
			user_group_1_store     = np.array(user_group_df[user_group_df.columns[1]])
			user_group_2_store     = np.array(user_group_df[user_group_df.columns[2]])
			user_group_na_store    = np.array(user_group_df[user_group_df.columns[3]])
			user_group_uncat_store = np.array(user_group_df[user_group_df.columns[4]])
			user_group_name_basis=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\7",recent_path)
			user_group_name=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4",recent_path)
			user_group_name_a=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\5",recent_path)
			user_group_name_b=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\6",recent_path)
			return flask.redirect(flask.url_for('user_group_agg'))
	
		else:
		
			return flask.redirect(flask.url_for('user_group_agg'))

	else:
		
		return flask.redirect(flask.url_for('user_group_agg'))

@app.route('/user_group_load_<load_category>', methods=['GET','POST'])
def user_group_load_category(load_category):
	
	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_uncat_store
	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	# load (for later loading)

	load_path = glob.glob(os.path.join(user_setting['output_dir'],'contact_df_'+load_category+'$*.csv'))[0]

	if (os.path.exists(os.path.join(user_setting['output_dir'],load_path)) and len(load_path)>0):
	
		user_group_df          = pd.read_csv(os.path.join(user_setting['output_dir'],load_path))
		user_group_1_store     = np.array(user_group_df[user_group_df.columns[1]])
		user_group_2_store     = np.array(user_group_df[user_group_df.columns[2]])
		user_group_na_store    = np.array(user_group_df[user_group_df.columns[3]])
		user_group_uncat_store = np.array(user_group_df[user_group_df.columns[4]])
		user_group_name_basis=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\7",load_path)
		user_group_name=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4",load_path)
		user_group_name_a=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\5",load_path)
		user_group_name_b=re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\6",load_path)

		if (user_group_name_basis=="**Gender_Default"):
			for i in agg_contact_df['contact'].tolist():
				
				if (i not in user_group_1_store) and (i not in user_group_2_store):
					
					if i in agg_contact_df.loc[agg_contact_df['contact_gender']=='M','contact'].tolist():
						user_group_1_store = user_group_1_store.tolist()
						user_group_1_store.append(i)
						user_group_1_store = np.array(user_group_1_store)
					if i in agg_contact_df.loc[agg_contact_df['contact_gender']=='F','contact'].tolist():
						user_group_2_store = user_group_2_store.tolist()
						user_group_2_store.append(i)
						user_group_2_store = np.array(user_group_2_store)
		return flask.redirect(flask.url_for('user_group_agg'))
	
	else:
	
		return flask.redirect(flask.url_for('user_group_agg'))


@app.route('/user_group_load_gender', methods=['GET','POST'])
def user_group_load_gender():

	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_uncat_store
	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global agg_contact_df
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	user_group_1_store     = np.array(agg_contact_df.loc[agg_contact_df['contact_gender']=='M','contact'])
	user_group_2_store     = np.array(agg_contact_df.loc[agg_contact_df['contact_gender']=='F','contact'])
	user_group_na_store    = np.array(agg_contact_df.loc[agg_contact_df['contact_gender']=='I','contact'])
	user_group_uncat_store = np.array([])

	user_group_name = "**Gender_Default"
	user_group_name_a = "Male"
	user_group_name_b = "Female"
	user_group_name_basis = "**Gender_Default"

	return flask.redirect(flask.url_for('user_group_agg'))

@app.route('/user_group_load_blank', methods=['GET','POST'])
def user_group_load_blank():

	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_uncat_store
	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global agg_contact_df
	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	user_group_1_store     = np.array([])
	user_group_2_store     = np.array([])
	user_group_na_store    = np.array(agg_contact_df['contact'])
	user_group_uncat_store = np.array([])

	user_group_name = "**Blank_Default"
	user_group_name_a = "Group A"
	user_group_name_b = "Group B"
	user_group_name_basis = "**Blank_Default"

	return flask.redirect(flask.url_for('user_group_agg'))

@app.route('/user_group_store', methods=['GET', 'POST'])
def user_group_store():

	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global agg_contact_df
	global feat_df

	global user_group_1_store
	global user_group_2_store
	global user_group_na_store
	global user_group_uncat_store

	global user_group_name
	global user_group_name_a
	global user_group_name_b
	global user_group_name_basis

	# reset stored user groups
	user_group_1_store     = np.array([])
	user_group_2_store     = np.array([])
	user_group_na_store    = np.array([])
	user_group_uncat_store = np.array([])


	agg_contact_df_contact = np.array(agg_contact_df['contact'].unique())
	overall_contact        = np.array(feat_df['link_contact'].unique())

	user_group_na    = agg_contact_df_contact[np.array([x not in user_group_1 and x not in user_group_2 for x in agg_contact_df_contact])]
	user_group_uncat = overall_contact[np.array([x not in user_group_1 and x not in user_group_2 and x not in user_group_na for x in overall_contact])]

	if len(user_group_1)>0 and len(user_group_2)>0:

		# store (for later loading)
		user_group_df_1       = pd.DataFrame({'user_group_1':user_group_1})
		user_group_df_2       = pd.DataFrame({'user_group_2':user_group_2})
		user_group_df_na      = pd.DataFrame({'user_group_na':user_group_na})
		user_group_df_uncat   = pd.DataFrame({'user_group_na':user_group_uncat})
		user_group_df         = pd.concat([user_group_df_1,user_group_df_2], ignore_index=True, axis=1)
		user_group_df         = pd.concat([user_group_df,user_group_df_na], ignore_index=True, axis=1)
		user_group_df         = pd.concat([user_group_df,user_group_df_uncat], ignore_index=True, axis=1)

		df_name = 'contact_df_' + str(user_group_name) + "$" + str(user_group_name_a) + '$' + str(user_group_name_b) + '$' + str(user_group_name_basis) + '.csv'
		user_group_df.columns = [user_group_name_a,user_group_name_b,'user_group_na','user_group_uncat']
		user_group_df.to_csv(os.path.join(user_setting['output_dir'], df_name))

		with open(os.path.join(user_setting['output_dir'],'contact_df_recent.txt'),'w') as file:  
			file.write(df_name)

		if user_setting['dev_mode']=='True':
				user_group_df.to_csv(os.path.join(user_setting['output_dir'], 'user_group_df.csv'), encoding="utf8")


		# load page
		return flask.redirect(flask.url_for('birthday'))
	else:
		return flask.redirect(flask.url_for('user_group_agg'))

## birthday
#---------------------------

@app.route('/birthday')
def birthday():

	global feat_df

	#format date
	map_month    	      = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October', 11:'November', 12:'December'}
	birthday_guess        = parser.parse(feat_df['birthday..birthday_guess_1'][0][0])
	birthday_guess_month  = str(pd.Series(int(birthday_guess.strftime('%m'))).map(map_month)[0])
	birthday_guess_day    = str(birthday_guess.strftime('%d'))

	birthday_guess_format = birthday_guess_month + ', ' + birthday_guess_day
	
	# render
	return flask.render_template('sample_insight.html',
		birthday_guess=birthday_guess_format)

@app.route('/birthday_followup')
def birthday_followup():

	global feat_df

	birthday_guess_alt = []

	#format date
	map_month    	      = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October', 11:'November', 12:'December'}
	
	for i in ['birthday..birthday_guess_2','birthday..birthday_guess_3','birthday..birthday_guess_4','birthday..birthday_guess_5']:
		birthday_guess_tmp        = parser.parse(feat_df[i][0][0])
		birthday_guess_month_tmp  = str(pd.Series(int(birthday_guess_tmp.strftime('%m'))).map(map_month)[0])
		birthday_guess_day_tmp    = str(birthday_guess_tmp.strftime('%d'))

		birthday_guess_format_tmp = birthday_guess_month_tmp + ', ' + birthday_guess_day_tmp
		birthday_guess_alt.append(birthday_guess_format_tmp)
	
	# render
	return flask.render_template('sample_insight_followup.html',
		birthday_guess=birthday_guess_alt)


## success
#---------------------------

@app.route('/success')
def success():

	global link_id_store
	global feat_df
	global feat_df_all
	global volume_df
	global global_var
	global agg_contact_df
	global feat_df_dict
	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na
	global user_group_uncat
	global user_group_name_a
	global user_group_name_b
	global user_group_name
	# global user_group_ambig_gender_len
	# global user_group_ambig_gender_len_perc
	# global user_group_unknown_gender_len
	# global user_group_unknown_gender_len_perc

	# resetid
	global internal_email_id
	internal_email_id=0
	link_id_store='-1'

	# group labelling
	contact_xwalk_contact = np.concatenate([user_group_1, user_group_2, user_group_na])
	contact_xwalk_label   = np.concatenate([np.array(global_fun.fill_array(len(user_group_1), "group_a")), np.array(global_fun.fill_array(len(user_group_2), "group_b")), np.array(global_fun.fill_array(len(user_group_na), "group_na"))])

	contact_flag, contact_flag_msg, contact_flag_thread = contact.contact_labeller(contact_xwalk_contact, contact_xwalk_label,
		feat_df['link_contact'] ,feat_df['msg_id'] ,feat_df['msg_threadid'] )
	feat_df['flag.group']        = contact_flag
	feat_df['flag.group_msg']    = contact_flag_msg
	feat_df['flag.group_thread'] = contact_flag_thread

	# gender labelling
	user_group_male           = np.array([])
	user_group_female         = np.array(agg_contact_df.loc[agg_contact_df['contact_gender']=='F','contact'])
	user_group_unknown_gender = np.array(agg_contact_df.loc[agg_contact_df['contact_gender']=='I','contact'])

	contact_xwalk_contact = np.concatenate([user_group_male, user_group_female, user_group_unknown_gender])
	contact_xwalk_label   = np.concatenate([np.array(global_fun.fill_array(len(user_group_male), "group_male")), np.array(global_fun.fill_array(len(user_group_female), "group_female")), np.array(global_fun.fill_array(len(user_group_unknown_gender), "group_unknown_gender"))])

	contact_flag, contact_flag_msg, contact_flag_thread = contact.contact_labeller(contact_xwalk_contact, contact_xwalk_label,
		feat_df['link_contact'] ,feat_df['msg_id'] ,feat_df['msg_threadid'] )
	feat_df['flag.group_gender']        = contact_flag
	feat_df['flag.group_gender_msg']    = contact_flag_msg
	feat_df['flag.group_gender_thread'] = contact_flag_thread

	feat_df_dict['group_col'] = ["flag.group_gender", "flag.group"]

	if user_setting['dev_mode']=='True':
			feat_df.to_csv(os.path.join(user_setting['output_dir'], 'feat_df.csv'), encoding="utf8")

	# counts
	count                          		 = volume_df['overall_email']
	inbox_count                    		 = volume_df['overall_received_email']
	outbox_count                  		 = volume_df['overall_sent_email']

	link_count                     		 = volume_df['overall_link']
	inbox_link_count                     = volume_df['overall_received_link']
	outbox_link_count              		 = volume_df['overall_sent_link']

	user_group_1_len               		 = len(feat_df.loc[(feat_df['flag.group']=='group_a') & ~(feat_df['link_contact'].str.contains('user')),'link_contact'].unique())
	user_group_2_len               		 = len(feat_df.loc[(feat_df['flag.group']=='group_b') & ~(feat_df['link_contact'].str.contains('user')),'link_contact'].unique())
	user_group_uncat_len                 = len(feat_df.loc[(feat_df['flag.group']=='na') & ~(feat_df['link_contact'].str.contains('user')),'link_contact'].unique())
	user_len             		   		 = len(feat_df.loc[~(feat_df['link_contact'].str.contains('user')),'link_contact'].unique())
	user_group_1_inbox_len               = len(feat_df.loc[(feat_df['flag.group']=='group_a') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='inbox'),'link_contact'].unique())
	user_group_2_inbox_len               = len(feat_df.loc[(feat_df['flag.group']=='group_b') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='inbox'),'link_contact'].unique())
	user_group_uncat_inbox_len           = len(feat_df.loc[(feat_df['flag.group']=='na') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='inbox'),'link_contact'].unique())
	user_inbox_len                       = len(feat_df.loc[~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='inbox'),'link_contact'].unique())

	user_group_1_outbox_len        		 = len(feat_df.loc[(feat_df['flag.group']=='group_a') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='outbox'),'link_contact'].unique())
	user_group_2_outbox_len              = len(feat_df.loc[(feat_df['flag.group']=='group_b') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='outbox'),'link_contact'].unique())
	user_group_uncat_outbox_len          = len(feat_df.loc[(feat_df['flag.group']=='na') & ~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='outbox'),'link_contact'].unique())
	user_outbox_len                      = len(feat_df.loc[~(feat_df['link_contact'].str.contains('user')) & (feat_df['flag.inbox_outbox']=='outbox'),'link_contact'].unique())

	# details
	date_range= user_setting['earliest_date'] + ' - ' + user_setting['latest_date']

	# stage error
	if (len([x for x in global_var['status_feature_error'] if x != 'None'])>0):
		stage_error = ' / '.join([x for x in global_var['status_feature_error'] if x != 'None'])
	else:
		stage_error = 'None'

	# render
	return flask.render_template('success.html',date_diff=user_setting['date_diff'], 
		user=user, 
		date_range=date_range, stage_error=stage_error,user_len=user_len, user_group_1_len=user_group_1_len,
		user_group_2_len=user_group_2_len, user_group_uncat_len=user_group_uncat_len, 
		inbox_count=inbox_count, 
		outbox_count=outbox_count, inbox_link_count=inbox_link_count, outbox_link_count=outbox_link_count,
		error_count=error_count, excluded_count=excluded_count, run_time=run_time,
		run_time_feature=run_time_feature,user_inbox_len=user_inbox_len, 
		user_group_1_inbox_len=user_group_1_inbox_len, user_group_2_inbox_len=user_group_2_inbox_len,
		user_group_uncat_inbox_len=user_group_uncat_inbox_len,
		user_outbox_len=user_outbox_len, user_group_1_outbox_len=user_group_1_outbox_len,
		user_group_2_outbox_len=user_group_2_outbox_len,
		user_group_uncat_outbox_len=user_group_uncat_outbox_len, count=count, link_count=link_count,
		user_group_name=user_group_name, 
		user_group_name_a=user_group_name_a,
		user_group_name_b=user_group_name_b)
		# user_group_ambig_gender_len=user_group_ambig_gender_len, 
		# user_group_ambig_gender_len_perc=user_group_ambig_gender_len_perc,
		# user_group_unknown_gender_len=user_group_unknown_gender_len,
		# user_group_unknown_gender_len_perc=user_group_unknown_gender_len_perc)

## insights
#---------------------------

@app.route('/insight_nonlang')
def insight_nonlang():
	

	global user_group_na
	global user_group_name_a
	global user_group_name_b

	user_group_na_indic = int(len(user_group_na)>0)

	# insights
	insight_agg_dict, insight_plot, insight_plot_id = insight_agg(feat_df,user_setting['date_diff'], "nonlang",user_group_na_indic)

	# parse the returned insights
	nonlang_volume_df                              = global_fun.pd_htmlformat_seq(insight_agg_dict['volume'])
	nonlang_firstlast_df                           = global_fun.pd_htmlformat_seq(insight_agg_dict['firstlast'])
	nonlang_responsiveness_df                      = global_fun.pd_htmlformat_seq(insight_agg_dict['responsiveness'])

	# render
	return flask.render_template('insight_nonlang.html', user_id=user_name, 
		nonlang_volume_df=nonlang_volume_df,
		nonlang_firstlast_df=nonlang_firstlast_df, 
		nonlang_responsiveness_df=nonlang_responsiveness_df,
		graphJSON=insight_plot,ids=insight_plot_id, 
		user_group_name_a=user_group_name_a, 
		user_group_name_b=user_group_name_b)


@app.route('/insight_simplelang')
def insight_simplelang():

	global user_group_na
	global user_group_name_a
	global user_group_name_b

	user_group_na_indic = int(len(user_group_na)>0)
	
	# insights
	insight_agg_dict, insight_plot, insight_plot_id = insight_agg(feat_df,user_setting['date_diff'], "simplelang",user_group_na_indic)

	simplelang_talkative_df            = global_fun.pd_htmlformat_seq(insight_agg_dict['talkative'])
	simplelang_lengthimbalance_df      = global_fun.pd_htmlformat_seq(insight_agg_dict['lengthimbalance'])

	# render
	return flask.render_template('insight_simplelang.html', user_id=user_name, 
		simplelang_talkative_df=simplelang_talkative_df,
		simplelang_lengthimbalance_df=simplelang_lengthimbalance_df,
		graphJSON=insight_plot,ids=insight_plot_id, 
		user_group_name_a=user_group_name_a, 
		user_group_name_b=user_group_name_b)


@app.route('/insight_nlp')
def insight_nlp():

	global user_group_na
	global user_group_name_a
	global user_group_name_b

	user_group_na_indic = int(len(user_group_na)>0)

	# insights
	insight_agg_dict, insight_plot, insight_plot_id = insight_agg(feat_df,user_setting['date_diff'], "nlp",user_group_na_indic)

	nlp_politeness_df               = global_fun.pd_htmlformat_seq(insight_agg_dict['politeness'])
	nlp_sentiment_df       			= global_fun.pd_htmlformat_seq(insight_agg_dict['sentiment']) 
	nlp_linguisticcoordination_df   = global_fun.pd_htmlformat_seq(insight_agg_dict['coordination'])

	# render
	return flask.render_template('insight_nlp.html', user_id=user_name,
		nlp_politeness_df=nlp_politeness_df,
		nlp_linguisticcoordination_df=nlp_linguisticcoordination_df,
		nlp_sentiment_df=nlp_sentiment_df,
		graphJSON=insight_plot,ids=insight_plot_id, 
		user_group_name_a=user_group_name_a, 
		user_group_name_b=user_group_name_b)


## browser
#---------------------------

@app.route('/reset_link_id', methods=['POST'])
def reset_link_id():

	global link_id_store
	global browser_mode

	# obtain link id
	link_id_store = flask.request.form.getlist('link_id_store')[0]
	
	if browser_mode == "inbox":
		
		return flask.redirect(flask.url_for('load_inbox'))

	elif browser_mode == "outbox":

		return flask.redirect(flask.url_for('load_outbox'))

@app.route('/load_inbox', methods=['GET', 'POST'])
def load_inbox():
	
	print('Loading')
	
	global internal_email_id
	global link_id
	global link_id_store
	global email_array_browser
	global email_array
	global feat_df
	global feat_df_all
	global feat_df_dict
	global email_meta_df
	global email_text_df
	global email_insight_df
	global link_df
	global browser_mode

	browser_mode="inbox"

	## update
	email_array_browser = glob.glob(os.path.join(user_setting['output_dir'],'inbox', 'email*.json'))
	email_array_browser = np.array([x for x in email_array_browser if x in email_array])

	if (len(email_array_browser)>0):
		
		email_id            = re.sub("(.*email_)([^_]*)(_.*json$)","\\2",email_array_browser[internal_email_id])

		if internal_email_id<len(email_array_browser) and (internal_email_id>=0) and (email_id in np.array(feat_df['msg_id'])):
		
			email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link, link_df, link_id_store = dataprep.prepare_browser_vis(feat_df,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=False)

			return flask.render_template('browser.html',meta=[email_meta_df_link],insight=[email_insight_df_link], text_decomposed=[email_decom_text_df_link], text=[email_text_df_link], link_list=range(0,len(link_df)), link_desc=link_df['link_desc'], link_id=link_df['link_id'], mode="inbox_outbox")

		elif internal_email_id<len(email_array_browser) and internal_email_id>=0 and (email_id not in np.array(feat_df['msg_id'])):

			print('Unable to load > skipping to next email')
			return flask.redirect(flask.url_for('reload_next'))

		else:

			return flask.redirect(flask.url_for('success'))

	else:

			return flask.redirect(flask.url_for('success'))

@app.route('/load_outbox', methods=['GET', 'POST'])
def load_outbox():
	
	print('Loading')
	
	global internal_email_id
	global link_id
	global link_id_store
	global email_array_browser
	global email_array
	global feat_df
	global feat_df_all
	global feat_df_dict
	global email_meta_df
	global email_text_df
	global email_insight_df
	global link_df
	global browser_mode

	browser_mode="outbox"

	## update
	email_array_browser = glob.glob(os.path.join(user_setting['output_dir'],'outbox', 'email*.json'))
	email_array_browser = np.array([x for x in email_array_browser if x in email_array])
	
	if (len(email_array_browser)>0):

		email_id            = re.sub("(.*email_)([^_]*)(_.*json$)","\\2",email_array_browser[internal_email_id])

		if internal_email_id<len(email_array_browser) and (internal_email_id>=0) and (email_id in np.array(feat_df['msg_id'])):

			email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link,link_df, link_id_store = dataprep.prepare_browser_vis(feat_df,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=False)

			return flask.render_template('browser.html',meta=[email_meta_df_link],insight=[email_insight_df_link], text_decomposed=[email_decom_text_df_link], text=[email_text_df_link], link_list=range(0,len(link_df)), link_desc=link_df['link_desc'], link_id=link_df['link_id'], mode="inbox_outbox")


		elif internal_email_id<len(email_array_browser) and internal_email_id>=0 and (email_id not in np.array(feat_df['msg_id'])):

			print('Unable to load > skipping to next email')
			return flask.redirect(flask.url_for('reload_next'))

		else:

			return flask.redirect(flask.url_for('success'))

	else:
		
			return flask.redirect(flask.url_for('success'))



@app.route('/reload_next', methods=['GET', 'POST'])
def reload_next():
	
	print('Re-Loading')
	
	global internal_email_id
	global link_id
	global link_id_store
	global browser_mode
	global email_array_browser
	global email_array
	global feat_df
	global feat_df_all
	global feat_df_dict
	global email_meta_df
	global email_text_df
	global email_insight_df
	global link_df

	## update internal_email_id count
	internal_email_id   = internal_email_id+1
	print(internal_email_id)
	

	if browser_mode == "inbox" or  browser_mode == "outbox":
		feat_df_tmp = feat_df
	elif browser_mode=="exclude":
		feat_df_tmp = feat_df_all
	

	if (internal_email_id<len(email_array_browser)) and (internal_email_id>=0):

		email_id            = re.sub("(.*email_)([^_]*)(_.*json$)","\\2",email_array_browser[internal_email_id])
		print(email_id)

		if (email_id in np.array(feat_df_tmp['msg_id'])):


			if browser_mode == "inbox" or  browser_mode == "outbox":
	
				email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link,link_df, link_id_store = dataprep.prepare_browser_vis(feat_df,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=True)

				return flask.render_template('browser.html',meta=[email_meta_df_link],insight=[email_insight_df_link],text_decomposed=[email_decom_text_df_link],  text=[email_text_df_link], link_list=range(0,len(link_df)), link_desc=link_df['link_desc'], link_id=link_df['link_id'], mode="inbox_outbox")

			elif browser_mode=="exclude":

				email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link,link_df, link_id_store = dataprep.prepare_browser_vis(feat_df_all,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=True)

				return flask.render_template('browser.html',meta=[email_meta_df_link], text=[email_text_df_link], mode=browser_mode)

		elif (email_id not in np.array(feat_df_tmp['msg_id'])):
		
			print('Unable to load > skipping to next email')
			return flask.redirect(flask.url_for('reload_next'))

	else:

		return flask.redirect(flask.url_for('success'))

@app.route('/reload_pre', methods=['GET', 'POST'])
def reload_pre():
	
	print('Re-Loading')
	
	global internal_email_id
	global browser_mode
	global link_id
	global link_id_store
	global email_array_browser
	global email_array
	global feat_df
	global feat_df_all
	global feat_df_dict
	global email_meta_df
	global email_text_df
	global email_insight_df
	global link_df

	## update internal_email_id count
	internal_email_id=internal_email_id-1
	print(internal_email_id)
	

	if browser_mode == "inbox" or  browser_mode == "outbox":
		feat_df_tmp = feat_df
	elif browser_mode=="exclude":
		feat_df_tmp = feat_df_all
	
	if (internal_email_id<len(email_array_browser)) and (internal_email_id>=0):

		email_id            = re.sub("(.*email_)([^_]*)(_.*json$)","\\2",email_array_browser[internal_email_id])
		print(email_id)

		if (email_id in np.array(feat_df_tmp['msg_id'])):


			if browser_mode == "inbox" or  browser_mode == "outbox":
	
				email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link,link_df, link_id_store = dataprep.prepare_browser_vis(feat_df,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=True)

				return flask.render_template('browser.html',meta=[email_meta_df_link],insight=[email_insight_df_link], text_decomposed=[email_decom_text_df_link], text=[email_text_df_link], link_list=range(0,len(link_df)), link_desc=link_df['link_desc'], link_id=link_df['link_id'], mode="inbox_outbox")

			elif browser_mode=="exclude":

				email_meta_df_link, email_insight_df_link, email_text_df_link, email_decom_text_df_link,link_df, link_id_store = dataprep.prepare_browser_vis(feat_df_all,feat_df_dict, email_array_browser, internal_email_id,link_id_store, reload=True)

				return flask.render_template('browser.html',meta=[email_meta_df_link], text=[email_text_df_link], mode=browser_mode)

		elif (email_id not in np.array(feat_df_tmp['msg_id'])):
		
			print('Unable to load > skipping to previous email')
			return flask.redirect(flask.url_for('reload_pre'))

	else:

		return flask.redirect(flask.url_for('success'))


## other - display
#---------------------------

@app.route('/user_group_display', methods=['POST','GET'])
def user_group_display():

	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na	
	global user_group_uncat

	user_group_1_temp= '|'.join(user_group_1)
	user_group_2_temp= '|'.join(user_group_2)

	# table
	user_group_df_1     = pd.DataFrame({'user_group_1':user_group_1})
	user_group_df_2     = pd.DataFrame({'user_group_2':user_group_2})
	user_group_df_na    = pd.DataFrame({'user_group_none':user_group_na})
	user_group_df_uncat = pd.DataFrame({'user_group_uncategorized':user_group_uncat})

	user_group_df       = pd.concat([user_group_df_1,user_group_df_2], ignore_index=True, axis=1)
	user_group_df       = pd.concat([user_group_df,user_group_df_na], ignore_index=True, axis=1)
	user_group_df       = pd.concat([user_group_df,user_group_df_uncat], ignore_index=True, axis=1)

	user_group_df.columns=[user_group_name_a,user_group_name_b,'user_group_none','user_group_uncategorized']
	user_group_df = user_group_df.to_html()

	# render
	return flask.render_template('user_group_display.html',user_group_df=[user_group_df])


@app.route('/user_group_gender_display', methods=['POST','GET'])
def user_group_gender_display():

	global user_group_female
	global user_group_male 
	global user_group_unknown_gender
	global user_group_1
	global user_group_2
	global user_group_na	
	global user_group_uncat

	user_group_df_male              = pd.DataFrame({'user_group_male':user_group_male})
	user_group_df_female            = pd.DataFrame({'user_group_female':user_group_female})
	user_group_df_unknown_gender    = pd.DataFrame({'user_group_unknown_gender':user_group_unknown_gender})

	user_group_gender_df            = pd.concat([user_group_df_male,user_group_df_female], ignore_index=True, axis=1)
	user_group_gender_df            = pd.concat([user_group_gender_df,user_group_df_unknown_gender], ignore_index=True, axis=1)

	user_group_gender_df.columns=['user_group_male','user_group_female','user_group_unknown_gender']
	user_group_gender_df = user_group_gender_df.to_html()

	# render
	return flask.render_template('user_group_display.html',user_group_df=[user_group_gender_df])


#----------------------------------------------------------------------------#
#                       Launch Flask Application                             #
#----------------------------------------------------------------------------#
http_server = WSGIServer(('', app_setting['app_port']), app)
http_server.serve_forever()
	 

#----------------------------------------------------------------------------#
#                               End                                          #
#----------------------------------------------------------------------------#
