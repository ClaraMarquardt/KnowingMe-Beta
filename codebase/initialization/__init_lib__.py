# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         __init__  
# Purpose:      Load Python dependencies
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# System Dependencies
# ------------------------------------------------------------------------ #

# Basic
import os, sys

# Warnings
import warnings

# ------------------------------------------------------------------------ #
# Main Dependencies
# ------------------------------------------------------------------------ #

# Generic
import os
import sys
import dill
import glob
import base64
import csv
import random
import time
import cPickle as pickle
from scipy.sparse import csr_matrix
import calendar
import math
import pandas as pd
import numpy as np
import uuid

import json
import re
import string

import datetime
from   dateutil import parser
import pytz

# Vis
import plotly
import plotly.graph_objs as go

# Flask
import webbrowser
import flask 
from   flask_httpauth import HTTPBasicAuth
from   flask_oauth import OAuth
from   urllib2 import Request, urlopen, URLError
from   threading import Thread
from   gevent.wsgi import WSGIServer
from   flask_sqlalchemy import SQLAlchemy
from   sqlalchemy.dialects.postgresql import JSON
from   werkzeug.debug import DebuggedApplication

# Gmail API & OAuth2
import httplib2
from   googleapiclient import discovery, errors
from   googleapiclient.http import BatchHttpRequest

from   oauth2client import client, tools
from   oauth2client.file import Storage

# Email
import email
from   email.parser import Parser

# NLP
import nltk
import spacy
import pycorenlp
from   pycorenlp.corenlp import StanfordCoreNLP
from   langdetect import detect
from   vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ML & Co
import scipy
import sklearn

# Dependencies - External > Settings
#---------------------------------------------#
pd.options.mode.chained_assignment = None 
pd.options.display.max_colwidth    = 1000 

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="Boolean Series key will be reindexed to match DataFrame index.")
warnings.filterwarnings("ignore", message="Mean of empty slice.")
warnings.filterwarnings("ignore", message="invalid value encountered in double_scalars")

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

