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
current_date        = datetime.datetime.now()
current_date        = current_date.strftime("%m/%d/%Y")

# platform
platform            = sys.platform

# ------------------------------------------------------------------------ #
# Directory
# ------------------------------------------------------------------------ #

# setting directory
user_setting_file  = os.path.normpath(os.path.join(app_root,'configuration','default_setting_user.json'))
app_setting_file   = os.path.normpath(os.path.join(app_root,'configuration','default_setting_app.json'))

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
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy_win','en_core_web_sm','en_core_web_sm-2.0.0'))
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
	
	# insight variables
	key_var['insight_intro_id']              = 0
	key_var['sample_insight_intro_id']       = 0
	
	key_var['insight_mode']                  = "intro"
	key_var['intro_release']                 = False
	
	key_var['current_insight'] 			 	 = ""
	key_var['current_insight'] 			 	 = ""

	# user group variables
	key_var['user_group_1_store']  		     = np.array([])
	key_var['user_group_2_store']  		     = np.array([])
	key_var['user_group_na_store']           = np.array([])
	key_var['user_group_1']  		         = []
	key_var['user_group_2']  		         = []
	key_var['user_group_na']			     = []
	key_var['user_group_name']               = "**Blank_Default"
	key_var['user_group_name_a']             = "Group A"
	key_var['user_group_name_b']             = "Group B"
	key_var['user_group_name_basis']  		 = "**Blank_Default"
	key_var['user_group_name_list_address']  = ['/user_group_load_gender','/user_group_load_blank','/user_group_store_rand']
	key_var['user_group_name_list_name']     = ['**Gender_Default','**Blank_Default','**Random_Default']
	
	if (reset_user == False): 
	
		# user variables
		key_var['user']                		 	 = key_var_old['user']
		key_var['user_name']    				 = key_var_old['user_name']
		key_var['user_photo']          		     = key_var_old['user_photo']
		key_var['service']          		     = key_var_old['service']

	return(key_var)

# initialize insight variables
# ---------------------------------------------#
def insight_initialization():

	# initialize
	insight_data     = {}	
	insight_text     = {}	
	insight_title    = {}		

	# initialize data - insight list
	insight_data['sample_insight_list']   	 = ['date_dist', 'time_dist','network', 'sample_sentiment']
	insight_data['intro_insight_list']    	 = ['talkative','sentiment','politeness']
	insight_data['main_insight_list']        = ['date_dist', 'time_dist','network', 'talkative','reponsiveness', 'firstlast', 'sentiment','politeness','coordination']
	insight_data['setting_insight_list']     = ['date_dist_setting', 'group_setting']

	insight_data['skip_sample_insight_list'] = ['talkative','responsiveness', 'firstlast']
	insight_data['add_info_list']            = ['sentiment','politeness', 'coordination']

	# initialize data - feature list
	nlp_feature_list                      	 = ['sentiment', 'politeness', 'coordination']  
	simplelang_feature_list               	 = ['language', 'talkative', 'lengthimbalance', 'birthday']
	nonlang_feature_list                  	 = ['responsiveness','firstlast','contact']
	feature_list                          	 = [nlp_feature_list, simplelang_feature_list, nonlang_feature_list]
	insight_data['feature_list']          	 = sum(feature_list, [])
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

	return(insight_data, insight_text, insight_title)

# initialize user setting variables
# ---------------------------------------------#
def user_setting_initialization():
	
	# initialize
	user_setting   = {}	

	# user settings (load)
	with open(user_setting_file) as data_file:    
		user_setting_data   = json.load(data_file)
	
	user_setting['min_day']                 = int(user_setting_data['min_day'])
	user_setting['min_email']               = int(user_setting_data['min_email'])
	user_setting['email_max']               = int(user_setting_data['email_max'])

	user_setting['timelag_day']             = int(user_setting_data['timelag_day'])
	user_setting['birthday_day']            = int(user_setting_data['birthday_day'])
	user_setting['overview_day']            = int(user_setting_data['overview_day'])
	user_setting['timelag_overview']        = int(user_setting_data['timelag_overview'])

	user_setting['output_dir']              = os.path.expanduser(str(user_setting_data['output_dir']))
	user_setting['output_dir_base']         = os.path.expanduser(str(user_setting_data['output_dir']))
	user_setting['output_dir_raw']          = str(user_setting_data['output_dir'])

	# Modify user settings (based on execution settings (environment variables))
	user_setting['output_dir']              = str(os.path.expanduser(os.getenv("OUTPUT", user_setting['output_dir'])))
	user_setting['output_dir_base']         = str(os.path.expanduser(os.getenv("OUTPUT", user_setting['output_dir_base'])))

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
	if not os.path.exists(os.path.join(user_data_dir, "contact")):
		os.makedirs(os.path.join(user_data_dir, "contact"))
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

# initialize user-specific contact groupings
# ---------------------------------------------#
def contact_group_intialization(user_data_dir, user_group_name_list_name, user_group_name_list_address):

	contact_path = glob.glob(os.path.join(user_data_dir,'contact', 'contact_df_*.csv'))
	contact_path = [re.sub("(.*(\/)*)(contact_df_)([^$]*)\$([^$]*)\$([^$]*)\$([^$]*)(\.csv)","\\4",x) for x in contact_path]
	contact_path = [x for x in contact_path if bool(re.match("\*",x))==False]

	user_group_name_list_name_temp = []
	for i in contact_path:
		user_group_name_list_name_temp.append(i)

	user_group_name_list_name_temp = [x for x in user_group_name_list_name_temp if x not in user_group_name_list_name]
	
	if (len(user_group_name_list_name_temp)>0):
		user_group_name_list_name_temp = list(set(user_group_name_list_name_temp))
		user_group_name_list_address_temp = ['/user_group_load_' + x for x in user_group_name_list_name_temp]	

		for i in user_group_name_list_name_temp:
			user_group_name_list_name.append(i)
		for i in user_group_name_list_address_temp:
			user_group_name_list_address.append(i)

	return(user_group_name_list_name,user_group_name_list_address)

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #



