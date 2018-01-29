## KnowingMeTester - Dependency & Variable Initialization

# path
import os, sys
app_root_init = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__))))  

#----------------------------------------------------------------------------#
#                                Dependencies                                #
#----------------------------------------------------------------------------#

# Warnings
#---------------------------------------------#
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


# Dependencies - External
#---------------------------------------------#

## Generic
import os
import sys
import glob
import base64
import random
import time
import pickle

import math
import pandas as pd
import numpy as np

import json
import re
import string

import datetime
from   dateutil import parser
import pytz

## Vis
import plotly
import plotly.graph_objs as go

## Flask
import webbrowser
import flask 
from   flask_oauth import OAuth
from   urllib2 import Request, urlopen, URLError
from   threading import Thread
from   gevent.wsgi import WSGIServer
from   flask_sqlalchemy import SQLAlchemy
from   sqlalchemy.dialects.postgresql import JSON

## Gmail API & OAuth2
import httplib2
from   googleapiclient import discovery, errors
from   googleapiclient.http import BatchHttpRequest

from   oauth2client import client, tools
from   oauth2client.file import Storage

## Email
import email
from   email.parser import Parser

## NLP
import nltk

## ML & Co
import scipy
import sklearn

# Dependencies - External > Settings
#---------------------------------------------#
pd.options.mode.chained_assignment = None 
pd.options.display.max_colwidth    = 1000 

nltk_dir = os.path.normpath(os.path.join(app_root_init, 'dependencies', 'nltk'))
nltk.data.path.append(nltk_dir)

#----------------------------------------------------------------------------#
#                                Variables                                   #
#----------------------------------------------------------------------------#

# Date variables
#----------------------------------------------------------------------------#
current_date=datetime.datetime.now()
current_date=current_date.strftime("%Y_%m_%d_%H:%M")

# Reference variables
#----------------------------------------------------------------------------#

# Directory Structure
# -------------
def dir_initialization():

	global user_setting_file
	global user_setting_file_user
	global dev_setting_file
	global app_setting_file

	user_setting_file_default = os.path.normpath(os.path.join(app_root_init,'setup','user_setting.json'))

	with open(user_setting_file_default) as data_file:    
		user_setting_data   = json.load(data_file)
	output_dir_default          = os.path.expanduser(str(user_setting_data['output_dir']))

	user_setting_file_user    = os.path.normpath(os.path.join(output_dir_default,'user_setting.json'))

	## setting files

	if (os.path.exists(user_setting_file_user)):
		user_setting_file = user_setting_file_user
	else: 
		user_setting_file = user_setting_file_default

	if (os.path.exists(os.path.join(output_dir_default, "dev_setting_user.json"))):
		dev_setting_file  = os.path.normpath(os.path.join(output_dir_default,"dev_setting_user.json"))
	else: 
		dev_setting_file  = os.path.normpath(os.path.join(app_root_init,'setup','dev_setting.json'))

	if (os.path.exists(os.path.join(output_dir_default, "app_setting_user.json"))):
		app_setting_file  = os.path.normpath(os.path.join(output_dir_default,'app_setting_user.json'))
	else: 
		app_setting_file  = os.path.normpath(os.path.join(app_root_init,'setup','app_setting.json'))

dir_initialization()

## flask app
app_static        = os.path.normpath(os.path.join(app_root_init, 'code','app', 'static'))
app_template      = os.path.normpath(os.path.join(app_root_init, 'code', 'app','template'))

# OAuth2
# -------------

api_auth_file      = os.path.normpath(os.path.join(app_root_init,'code', 'app','static','auth','client_secret_web.json'))
api_auth_scope     = ['https://www.googleapis.com/auth/gmail.readonly','profile','https://www.googleapis.com/auth/contacts.readonly']

# NLP 
# -------------


# Flask
# -------------
secret_key   = 'development key'
redirect_url = '/oauth2callback'

th           = Thread()

# Initialization
#----------------------------------------------------------------------------#

def var_initialization(user_setting):

	api_success  		= 'False'
	feature_success     = 'False'
	user_name    		= ""
	user_photo          = ""
	internal_email_id 	= 0
	link_id_store     	= '-1'
	user                = ""
	user_group_1_store  = np.array([])
	user_group_2_store  = np.array([])
	user_group_na_store = []
	user_group_1  		= []
	user_group_2  		= []
	user_group_na 		= []
	user_group_name        = "**Blank_Default"
	user_group_name_a      = "Group A"
	user_group_name_b      = "Group B"
	user_group_name_basis  = "**Blank_Default"
	user_group_name_list_address = ['/user_group_load_gender','/user_group_load_blank','/user_group_store_rand']
	user_group_name_list_name    = ['**Gender_Default','**Blank_Default','**Random_Default']
	
	return(api_success, feature_success,user_name,user_photo, internal_email_id,link_id_store, user, user_group_1_store, 
		user_group_2_store,user_group_na_store, user_group_1, user_group_2,user_group_na,
		user_group_name,user_group_name_a,user_group_name_b,user_group_name_basis,
		user_group_name_list_address,user_group_name_list_name)

# User Setting Initialization
#----------------------------------------------------------------------------#

def user_setting_initialization():
	
	dir_initialization()

	## initialize
	sample_setting = {}	
	user_setting   = {}	

	## sample settings
	sample_setting['user']	            ='kenneth.lay@enron.com'
	sample_setting['earliest_date']	    = "01/01/2001"
	sample_setting['latest_date']   	= "01/01/2002"
	sample_setting['date_diff']    	    = 100
	
	## user settings (load)
	with open(user_setting_file) as data_file:    
		user_setting_data   = json.load(data_file)
	user_setting['personal_email']          = user_setting_data['personal_email']
	user_setting['use_stored']              = user_setting_data['use_stored']
	user_setting['earliest_date']           = user_setting_data['earliest_date']
	user_setting['latest_date']             = user_setting_data['latest_date']
	user_setting['excl_non_personal_email'] = user_setting_data['excl_non_personal_email']
	user_setting['excl_archived_email']     = user_setting_data['excl_archived_email']
	user_setting['max_contact']             = user_setting_data['max_contact']
	user_setting['dev_mode']                = user_setting_data['dev_mode']
	user_setting['date_diff']               = int((parser.parse( user_setting['latest_date']) - parser.parse( user_setting['earliest_date'])).days)
	user_setting['output_dir']              = os.path.expanduser(str(user_setting_data['output_dir']))
	user_setting['output_dir_base']         = os.path.expanduser(str(user_setting_data['output_dir']))
	user_setting['output_dir_raw']          = str(user_setting_data['output_dir'])
	user_setting['process_email_lim']       = user_setting_data['process_email_lim']
	user_setting['extract_email_lim']       = user_setting_data['extract_email_lim']

	if user_setting['personal_email']=='False':
	
		user_setting['earliest_date']       = sample_setting['earliest_date']
		user_setting['latest_date']         = sample_setting['latest_date']
		user_setting['date_diff']           = sample_setting['date_diff']
		user_setting['sample_user']         = sample_setting['user']   

	# return
	return(user_setting, sample_setting)

#----------------------------------------------------------------------------#

