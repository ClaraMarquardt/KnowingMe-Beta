# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         __init_setting__	
# Purpose:      Initialize settings, incl. directories/file paths and
#               define functions to initialize variables
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialize
# ------------------------------------------------------------------------ #

# Path
import os, sys
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *

# ------------------------------------------------------------------------ #
# Generic Variables
# ------------------------------------------------------------------------ #

# date helper function (returns e.g. 6 > 6 hours behind UTC)
def local_time_offset(t=None):
    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return time.altzone
    else:
        return time.timezone

# date
timezone_utc_offset = local_time_offset()/60/60
timezone_utc_name   = time.strftime("%Z", time.gmtime())
timezone_utc_offset = int(os.getenv("TIMEZONE_OFFSET", timezone_utc_offset))
timezone_utc_name   = str(os.getenv("TIMEZONE_NAME", timezone_utc_name))

current_date        = datetime.datetime.now()
current_date        = current_date.strftime("%m/%d/%Y")

# platform
platform            = sys.platform

print(current_date)
print(timezone_utc_offset)
print(platform)

# ------------------------------------------------------------------------ #
# Directory
# ------------------------------------------------------------------------ #

# setting directory
user_setting_file  = os.path.normpath(os.path.join(app_root,'configuration','default_setting_user.json'))
app_setting_file   = os.path.normpath(os.path.join(app_root,'configuration','default_setting_app.json'))
auth_setting_file  = os.path.normpath(os.path.join(app_root,'configuration','default_setting_auth.json'))

# ------------------------------------------------------------------------ #
# Settings
# ------------------------------------------------------------------------ #

# Flask
app_static        	 = os.path.normpath(os.path.join(app_root, 'code','app', 'static'))
app_template      	 = os.path.normpath(os.path.join(app_root, 'code', 'app','template'))
secret_key        	 = 'development key'
redirect_url      	 = '/oauth2callback'
th                	 = Thread()

# OAuth2
api_auth_file        = os.path.normpath(os.path.join(app_root,'code', 'app','static','auth','client_secret_web.json'))
api_auth_file_manual = os.path.normpath(os.path.join(app_root,'code', 'app', 'static','auth','client_secret_manual.json'))
api_auth_scope       = ['https://www.googleapis.com/auth/gmail.readonly','profile','https://www.googleapis.com/auth/contacts.readonly']
api_logout_url       = 'https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue='
application_name     = "KnowingMe"

# NLTK
nltk_dir             = os.path.normpath(os.path.join(app_root, 'dependencies', 'nltk'))
nltk.data.path.append(nltk_dir)

# SPACY
if bool(re.match("win", platform))==True:
	print("App is currently not compatible with Windows (Spacy)")
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy','en_core_web_sm-1.2.0','en_core_web_sm','en_core_web_sm-1.2.0'))
else: 
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy','en_core_web_sm-1.2.0','en_core_web_sm','en_core_web_sm-1.2.0'))
nlp = spacy.load(spacy_dir)

# CORENLP
# core_nlp          =  StanfordCoreNLP("http://localhost" + ":" + "9000")

# VADER
vader_nlp           =  SentimentIntensityAnalyzer()

# Other Paths
pos_dict_path       = os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_model', 'coordination', 'pos_dict.json'))
polite_model_path   = os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_model', 'politeness','politeness_svm.p')) 
sentiment_dict_path = os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_model', 'sentiment', 'sentiment_dict.json'))
gender_path         = os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_model', 'gender','gender_database.csv')) 
insight_text_path   = os.path.normpath(os.path.join(app_root, 'code','app','static', 'text','insight_text.csv')) 
insight_title_path  = os.path.normpath(os.path.join(app_root, 'code','app','static', 'text','insight_title.csv')) 

# ------------------------------------------------------------------------ #
# Variable Initialization Functions
# ------------------------------------------------------------------------ #

# initialize variables
# ---------------------------------------------#
def var_initialization(reset_user=True, key_var_old=np.nan):

	# initialize
	key_var   = {}	

	# user variables
	key_var['user']                		 	 = ''
	key_var['user_name']    				 = ''
	key_var['user_photo']          		     = ''
	key_var['service']          		     = ''

	# status variables
	key_var['api_success']  				 = 'False'
	key_var['feature_success']    			 = 'False'
	
	# error variables
	key_var['error']                		 = ''
	
	# insight variables
	key_var['insight_intro_id']              = 0
	key_var['sample_insight_intro_id']       = 0
	
	key_var['insight_mode']                  = "intro"
	key_var['intro_release']                 = False
	
	key_var['current_insight'] 			 	 = ""
	key_var['current_insight'] 			 	 = ""

	# user group variables
	key_var['contact_group_user']  		     = np.nan
	key_var['scroll_mode']  		         = False

	if (reset_user == False): 
	
		# user variables
		key_var['user']                		 = key_var_old['user']
		key_var['user_name']    		     = key_var_old['user_name']
		key_var['user_photo']          		 = key_var_old['user_photo']
		key_var['service']          		 = key_var_old['service']

	return(key_var)

# initialize insight variables - meta data
# ---------------------------------------------#
def insight_meta_initialization():

	# initialize
	insight_meta_data     = {}	
	insight_text     = {}	
	insight_title    = {}		

	# initialize data - insight list
	insight_meta_data['sample_insight_list']   	  = ['date_dist', 'time_dist','network', 'sample_sentiment']
	insight_meta_data['intro_insight_list']    	  = ['talkative','sentiment','politeness']
	insight_meta_data['main_insight_list']        = ['date_dist', 'time_dist','network', 'talkative','reponsiveness', 'firstlast', 'sentiment','politeness','coordination']
	insight_meta_data['setting_insight_list']     = ['date_dist_setting', 'group_setting']

	insight_meta_data['skip_sample_insight_list'] = ['talkative','responsiveness', 'firstlast']
	insight_meta_data['add_info_list']            = ['sentiment','politeness', 'coordination']

	# initialize data - feature list
	nlp_feature_list                      	 = ['sentiment', 'politeness', 'coordination']  
	simplelang_feature_list               	 = ['language', 'talkative', 'lengthimbalance']
	nonlang_feature_list                  	 = ['responsiveness','firstlast','contact']
	feature_list                          	 = [nlp_feature_list, simplelang_feature_list, nonlang_feature_list]
	insight_meta_data['feature_list']        = sum(feature_list, [])
	## OMIT: sentiment_dict

	# load text
	insight_text_temp = pd.read_csv(insight_text_path)
	
	for i in list(insight_text_temp['insight']):
		insight_text[i] = dict()
		for j in insight_text_temp['screen']:
			try: 
				insight_text[i][j] = unicode(np.array(insight_text_temp.loc[insight_text_temp['insight']==i][insight_text_temp['screen']==j]['text'])[0], errors="ignore")
				insight_text[i][j] = re.sub("\r", "<br>", insight_text[i][j])
			except Exception as e: 
				insight_text[i][j] = ""

	# load title
	insight_title_temp = pd.read_csv(insight_title_path)
	
	for i in list(insight_title_temp['insight']):
		insight_title[i] = np.array(insight_title_temp.loc[insight_title_temp['insight']==i]['title'])[0]

	return(insight_meta_data, insight_text, insight_title)


# initialize user setting variables
# ---------------------------------------------#
def user_setting_initialization(session_id):
	
	# initialize
	user_setting   = {}	

	# user settings (load)
	with open(user_setting_file) as data_file:    
		user_setting_data   = json.load(data_file)
	
	user_setting['min_day']                 = int(user_setting_data['min_day'])
	user_setting['min_day_safe']            = int(user_setting_data['min_day_safe'])

	user_setting['min_email']               = int(user_setting_data['min_email'])
	user_setting['min_email_safe']          = int(user_setting_data['min_email_safe'])

	user_setting['email_max']               = int(user_setting_data['email_max'])
	user_setting['email_max_safe']          = int(user_setting_data['email_max_safe'])

	user_setting['safe_mode']               = str(user_setting_data['safe_mode'])

	user_setting['timelag_day']             = int(user_setting_data['timelag_day'])
	user_setting['birthday_day']            = int(user_setting_data['birthday_day'])
	user_setting['overview_day']            = int(user_setting_data['overview_day'])
	user_setting['timelag_overview']        = int(user_setting_data['timelag_overview'])

	user_setting['output_dir']              = os.path.expanduser(str(user_setting_data['output_dir']))
	user_setting['output_dir_base']         = os.path.expanduser(str(user_setting_data['output_dir']))

	# default variables
	user_setting['email_earliest_user']     = np.nan
	user_setting['email_latest_user']       = np.nan
	user_setting['email_range_user']        = np.nan
	user_setting['email_diff_user']         = np.nan

	# Modify user settings (based on execution settings (environment variables))
	user_setting['output_dir']              = str(os.path.expanduser(os.getenv("OUTPUT", user_setting['output_dir'])))
	user_setting['output_dir_base']         = str(os.path.expanduser(os.getenv("OUTPUT", user_setting['output_dir_base'])))

	user_setting['output_dir']              = os.path.join(user_setting['output_dir'], session_id)
	user_setting['output_dir_base']         = os.path.join(user_setting['output_dir_base'], session_id)

	user_setting['safe_mode']               = str(os.getenv("SAFE_MODE", user_setting['safe_mode']))=='True'
	if (user_setting['safe_mode']==True):
		user_setting['min_day']   = user_setting['min_day_safe']
		user_setting['min_email'] = user_setting['min_email_safe']
		user_setting['email_max'] = user_setting['email_max_safe']
	
	# return
	return(user_setting)

# initialize app setting variables
# ---------------------------------------------#
def app_setting_initialization():
	
	# initialize
	app_setting   = {}	

	# app settings (load)
	with open(app_setting_file) as data_file:    
		app_setting_data   = json.load(data_file)
	app_setting['app_port']                 = str(app_setting_data['app_port'])
	app_setting['app_debug']                = str(app_setting_data['app_debug'])
	app_setting['offline_mode']             = str(app_setting_data['offline_mode'])

	# Modify app settings (based on execution settings (environment variables))
	app_setting['app_port']  	= int(os.getenv("PORT", app_setting['app_port']))
	app_setting['app_debug'] 	= str(os.getenv("DEBUG", app_setting['app_debug']))=='True'
	app_setting['offline_mode'] = str(os.getenv("OFFLINE", app_setting['offline_mode']))=='True'

	# return
	return(app_setting)

# initialize app setting variables
# ---------------------------------------------#
def session_initialization():

	session_id = str(uuid.uuid4())

	return(session_id)

# initialize global variables
# ---------------------------------------------#
def global_initialization():

	# initialize
	global_var = dict()

	# Variables - Track email downloading/overview
	global_var['status_email_load']  		 = 0
	global_var['status_email_max']           = 0

	global_var['status_overview_load']       = 0
	global_var['status_overview_max']        = 0

	global_var['status_analysis_load']       = 0
	global_var['status_analysis_max']        = 0

	# Variables - Errors
	global_var['error']  				     = "General Error"
	global_var['error_msg']                  = "General Error"

	return(global_var)

# initialize authentication variables
# ---------------------------------------------#
def auth_initialization():

	with open(auth_setting_file) as data_file:    
		auth_setting_data   = json.load(data_file)

	app_username = auth_setting_data['app_username']
	app_password = auth_setting_data['app_password']

	app_auth_data = {
    	app_username : app_password
	}

	return(app_username, app_password, app_auth_data)

# ------------------------------------------------------------------------ #
# User Data Initialization Functions
# ------------------------------------------------------------------------ #

# initialize user data directory
# ---------------------------------------------#
def user_data_dir_init(user_data_dir):

	if not os.path.exists(os.path.join(user_data_dir, "inbox")):
		os.makedirs(os.path.join(user_data_dir, "inbox"))
	if not os.path.exists(os.path.join(user_data_dir, "outbox")):
		os.makedirs(os.path.join(user_data_dir, "outbox"))
	if not os.path.exists(os.path.join(user_data_dir, "other")):
		os.makedirs(os.path.join(user_data_dir, "other"))
	if not os.path.exists(os.path.join(user_data_dir, "dev")):
		os.makedirs(os.path.join(user_data_dir, "dev"))

# clear user data directory
# ---------------------------------------------#
def user_data_dir_clear(user_data_dir):

	if os.path.exists(user_data_dir):
		def purge(dir, pattern):
			files = sum([y for x in os.walk(dir) for y in [glob.glob(os.path.join(x[0], '*.'+e)) for e in pattern]],[])
			for f in files:
				os.remove(f)
		purge(user_data_dir, ["log","json","csv", "txt","p"])


# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #



