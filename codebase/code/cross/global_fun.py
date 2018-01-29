## Module    > 'global_fun'
## Purpose   > Intialize cross-module global (helper) functions
## Functions > freq_tabulate, df_sort, groupshift, pd_htmlformat, dict_round, perc, 
## 			   date_range, date_reindex,fill_array,dict_key_df

#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Dependencies - External
#---------------------------------------------#
import numpy as np
import pandas as pd
import re

# Dependencies - Internal
#---------------------------------------------#

#----------------------------------------------------------------------------#
#                       Function Definitions                                 #
#----------------------------------------------------------------------------#

# freq_tabulate
#---------------------------------------------#
def freq_tabulate(np_array, col_name):

	"""
	Convert an array into a frequency DataFrame

	Arguments:
	* np_array    - array
	* col_name    - column names assigned to the generated frequency DataFrame

	Returns:
	* np_array_df - frequency DataFrame
		
	"""

	np_array_unique,  np_array_unique_count = np.unique(np_array, return_counts=True)
	
	np_array_df           = pd.DataFrame({'item':np_array_unique,'freq':np_array_unique_count })
	np_array_df           = np_array_df.sort_values(by=['freq'], ascending=[False])
	np_array_df.columns   = col_name             
	
	return(np_array_df)

# df_sort
#---------------------------------------------#
def df_sort(df, col_name, ascend):

	"""
	Sort a DataFrame (includes an index reset)

	Arguments:
	* df          - DataFrame which is to be sorted
	* col_name    - column names on which to sort
	* ascend      - whether to sort - ascending (True) / descending (False)

	Returns:
	* np_array_df - frequency DataFrame
		
	"""

	df.sort_values(by=col_name, ascending=ascend)
	df.reset_index(inplace=True,drop=True)

	return(df)


# groupshift
#---------------------------------------------#
def groupshift(df, col_name, unit_col_name, group_col_name, shift_step):

	"""
	Shift a column of a pandas dataframe - within groups and by group-subunits

	Arguments:
	* df                 - DataFrame 
	* col_name           - column name which is to be shifted
	* unit_col_name      - name of column giving the group sub unit identifier
	* group_col_name     - name of column giving the group identifier

	Returns:
	* shift_col           - the shifted column
		
	"""

	# initialise
	df_tmp            = df[[col_name, group_col_name,unit_col_name]]
	df_tmp['id_tmp']  = range(0, len(df_tmp))

	# collapse
	df_tmp_collapse  = df_tmp.drop_duplicates([unit_col_name])

	# shift
	df_tmp_collapse['shift_tmp'] = df_tmp_collapse.groupby([group_col_name])[col_name].shift(shift_step)
	
	# merge with the original df
	df_tmp = pd.merge(df_tmp_collapse[[unit_col_name, 'shift_tmp']], df_tmp,on=unit_col_name, how='inner')

	# format
	df_tmp.sort_values(by='id_tmp', ascending=True)
	shift_col = np.array(df_tmp['shift_tmp'])
	
	# return
	return(shift_col)


# pd_htmlformat
#---------------------------------------------#

def pd_htmlformat(df, dict=False):

	"""
	Prepare a DataFrame for a flask visualisation

	Arguments:
	* df          - DataFrame which is to be formatted
	* dict        - Whether the input is a dictionary

	Returns:
	* df_format   - Formatted DataFrame
		
	"""

	try:

		if dict==False:
	
			df_format         = df.melt()
			df_format.columns = ['var', '']
			df_format['var']  = np.array([re.sub("(^[0-9a-z]*-)(.*)", "\\2", x) for x in df_format['var']])
			df_format.set_index(['var'], inplace=True)
			df_format.index.name=None
			df_format = df_format.to_html()
			
		else:
	
			order            = np.array(np.argsort(df.keys()))
	
			column_sort      = np.array(df.keys())[order]
			item_sort        = np.array(df.items())[order]
			
			data_dict        = [(x,0) for x in column_sort] 
			
			df_format        = pd.DataFrame(data=data_dict, columns=['var', ''])
			df_format['']    = [x[1] for x in item_sort] 
			df_format['var'] = np.array([re.sub("(^[0-9a-z]*-)(.*)", "\\2", x) for x in df_format['var']])

			df_format.set_index(['var'], inplace=True)
			df_format.index.name=None
			df_format = df_format.to_html()

	except Exception as e: 

		# error message
		print("Error Encountered - pd_htmlformat [global_fun]")
		print(e)

		df_format = df

	return(df_format)

# dict_round
#---------------------------------------------#

def dict_round(dict, round_digit=2):

	"""
	Round a dictionary to a specified number of decimals (splitting on /)

	Arguments:
	* dict           - Dictionary which is to be rounded
	* round_digit    - Number of decimal places

	Returns:
	* dict           - Formatted dictionarytaFrame
		
	"""
	
	try:
		for dict_value in dict:
			for k, v in dict.items():
				v_str = str(v)
				if type(v)=="float" or "/" in v_str:
					if "/" in v_str:
						if len(re.sub("[^/]","",v_str))==2:
							v_1,v_2,v_3 = v_str.split("/")
							if pd.notnull(v_1):
								v_1     = str(round(float(v_1), round_digit))
							if pd.notnull(v_2):
								v_2     = str(round(float(v_2), round_digit))
							if pd.notnull(v_3):
								v_3     = str(round(float(v_3), round_digit))

							v       = str(v_1) + " / " + str(v_2) + " / " + str(v_3)
							dict[k] = v
						else: 
							v_1,v_2 = v_str.split("/")
							if pd.notnull(v_1):
								v_1     = str(round(float(v_1), round_digit))
							if pd.notnull(v_2):
								v_2     = str(round(float(v_2), round_digit))
							v       = str(v_1) + " / " + str(v_2) 
							dict[k] = v
	
					else:
						dict[k] = str(round(float(v), round_digit))
				else:
					dict[k] = str(round(float(v), round_digit))

	except Exception as e: 

		# error message
		print("Error Encountered - dict_round [global_fun]")
		print(e)

		dict = dict

	
	return(dict)


# perc
#---------------------------------------------#

def perc(series_a, series_b, round_digit=2):

	"""
	Calculate a percentage given two series

	Arguments:
	* series_a       - Series a
	* series_b		 - Series a
	* round_digit    - Number of decimal places

	Returns:
	* series_perc    - Percentage series
		
	"""

	try: 
	
		if series_b!=0:
			series_perc = series_a / float(series_b)
			series_perc = series_perc * 100
			series_perc = round(series_perc,round_digit)
		else:
			series_perc=np.nan
	except Exception as e: 

		# error message
		print("Error Encountered - perc [global_fun]")
		print(e)

		series_perc = np.nan

	return(series_perc)
	

# date_range
#---------------------------------------------#

def date_range(df):

	"""
	Generate a dictionary with date ranges

	Arguments:
	* df                 - Insight dataframe on the basis of which to generate date ranges

	Returns:
	* date_range_dict    - Date range dictionary
		
	"""

	# initialise
	date_range_dict = {}


	# generate date ranges - df-specific
	df['msg_date_date']          = pd.to_datetime(df['msg_date_date'],errors='ignore',utc=True)
	date_range_dict['date']      = pd.date_range(np.min(df['msg_date_date']), np.max(df['msg_date_date']))

	week_id                       = [int(x[1]) for x in df['msg_date_week'].str.split(" ")]
	date_range_dict['week']       = ["Week " + str(x) for x in range(np.min(week_id),int(np.max(week_id))+1)]

	# generate date ranges - df-nonspecific
	date_range_dict['weekday']   = ['0-Monday','1-Tuesday','2-Wednesday','3-Thursday','4-Friday','5-Saturday','6-Sunday']
	date_range_dict['dayperiod'] = ["1-morning (6am-noon)", "2-afternoon (noon-9pm)", "3-night (9pm-6am)"]

	return(date_range_dict)


# date_reindex
#---------------------------------------------#

def date_reindex(df, date_type, date_range_dict,fill_val=0):

	"""
	Reindex different date/time related series (expand over entire date/time range)

	Arguments:
	* df                 - Insight dataframe on the basis of which to generate date ranges
	* date_type          - Type of the date/time series 
	* date_range_dict    - Date range dictionary

	Returns:
	* df                 - Reindexed/expanded dataframe
		
	"""

	# obtain the correct index
	if date_type=="week":
	
		date_range=date_range_dict['week']

	elif date_type=="weekday":

		date_range=date_range_dict['weekday']

	elif date_type=="dayperiod":

		date_range=date_range_dict['dayperiod']

	elif date_type=="date":

		date_range=date_range_dict['date']

	# expand
	if date_type=="week":

		df_tmp       = pd.DataFrame({'msg_date':df.reindex(date_range, fill_value=fill_val).index})
		df           = pd.merge(df_tmp, df, on='msg_date',how='left')
		df           = df.fillna(fill_val)

	elif date_type=="weekday":

		df_tmp       = pd.DataFrame({'msg_date':df.reindex(date_range, fill_value=fill_val).index})
		df           = pd.merge(df_tmp, df, on='msg_date',how='left')
		df           = df.fillna(fill_val)

	elif date_type=="dayperiod":

		df_tmp       = pd.DataFrame({'msg_date':df.reindex(date_range, fill_value=fill_val).index})
		df           = pd.merge(df_tmp, df, on='msg_date',how='left')
		df           = df.fillna(fill_val)

	elif date_type=="date":

		df.index       = pd.DatetimeIndex(df['msg_date'])
		df             = df.reindex(date_range, fill_value=fill_val)
		df['msg_date'] = df.index
		df.reset_index(drop=True, inplace=True)

	return(df)

# pd_htmlformat_seq
#---------------------------------------------#

def pd_htmlformat_seq(df_array):

	"""
	Prepare an array of DataFrames for a flask visualisation

	Arguments:
	* df_array    - DataFrame which is to be formatted

	Returns:
	* df_format_array   - Formatted DataFrame
		
	"""

	# initialize
	df_format_array =[]

	# loop
	for df_name in df_array.keys():

		df = df_array[df_name]
		df_format = pd_htmlformat(df, dict=True)
		df_format_array.append(df_format)
	
	return(df_format_array)

# fill_array
#---------------------------------------------#

def fill_array(array_len, array_value=0):
	
	"""
	Initialize an array of a given length with a given value

	Arguments:
	* array_len      - Length of the array
	* array_value    - Value of the array

	Returns:
	* tmp_array      - Generated array
		
	"""

	tmp_array = np.empty(array_len,dtype=object)
	tmp_array.fill(array_value)

	return(tmp_array)

# dict_key_df
#---------------------------------------------#

def dict_key_df(dict_list, id_name_1, id_name_2=None, incl_data=False):

	"""
		
	"""

	df_list = []

	for i in dict_list.keys():
		
		if id_name_2 is not None:

			df_temp = pd.DataFrame({id_name_1:getattr(dict_list[i],id_name_1),id_name_2:getattr(dict_list[i],id_name_2)})

		else:

			df_temp = pd.DataFrame({id_name_1:[getattr(dict_list[i],id_name_1)]})
				
		if incl_data==True:
		
			excl_id_attr       = ['msg_id','msg_threadid','link_id']
			excl_msg_text_attr = ['unigram', 'bigram','sentence','word','character','sentence_count','word_count', 'character_count','parse','pos','pos_dict','pos_count','pos_set','pos_indic', 'pos_set_agg','request','polite','sentiment_count','sentiment_indic','sentiment_set','sentiment_set_agg']
			excl_link_attr     = ['link_response_id_pair', 'link_reply_id_pair', 'link_response_count','link_reply_count','link_reply','link_responses']
			excl_conver_attr   = ['conversation']
			excl_msg_attr      = ['conversation_first', 'conversation_last']

			excl_attr          = sum([excl_id_attr,excl_msg_text_attr,excl_link_attr,excl_conver_attr], [])

			attr_list          = [x for x in dir(dict_list[i]) if "__" not in x and x not in excl_attr]
			
			for x in attr_list:

				obj_temp   = getattr(dict_list[i],x)

				## special case #1 - contact
				if x=="contact":

					for z in obj_temp.keys():

						if z!='msg_contact':

							name_tmp                   = ' || '.join(obj_temp[z]['name'])
							address_temp  			   = ' || '.join(obj_temp[z]['address'])
					
							name_tmp_name 			   = z +'_name'
							address_temp_name 		   = z +'_address'
						
							df_temp[name_tmp_name]     = name_tmp
							df_temp[address_temp_name] = address_temp
						
						else:

							df_temp[z]                 = ' || '.join(obj_temp[z])

				## special case #2 - contact
				elif x=="date":

					for z in obj_temp.keys():	
						
						df_temp[z]     = obj_temp[z]
	
				## base case multiple
				elif isinstance(obj_temp, (list, tuple, np.ndarray)):

					df_temp[x] = ' || '.join(obj_temp)

				## base case
				else:
					df_temp[x] = obj_temp

		df_list.append(df_temp)

	df  = pd.concat(df_list)
	df  = df.reset_index(drop=True, inplace=False)

	return(df)

#----------------------------------------------------------------------------#
