## Module    > gender 
## Functions > gender_labeler

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
# from * import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Other Paths
gender_dir = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'gender','gender_database.csv')) 

# Dependencies - External
#---------------------------------------------#
import csv
import re

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# gender_labeler
#---------------------------------------------#

# helper functions (nested functions)
#---------------------------------------------#

def match_maker1(name1):
	global name_count, gender1, in_list_1, match_found1
	
	match_found1 = False     
	with open(gender_dir, 'rt') as f:
		reader1 = csv.reader(f, delimiter=',') 
		
		for row in reader1:

			if name1.capitalize() == row[0]:
					gender1 = row[1]                   
					match_found1 = True
					in_list_1.append(name1)
					name_count += 1
					break
					
	return match_found1


def match_maker2(name2):   
	global name_count, gender2, in_list_2, match_found2
	
	match_found2 = False 
	with open(gender_dir, 'rt') as f:
		reader2 = csv.reader(f, delimiter=',') 
	   
		for row in reader2:  
					  
			 if name2.capitalize() == row[0]:
					gender2 = row[1]                   
					match_found2 = True
					in_list_2.append(name2)
					name_count += 1
					break
				
	return match_found2

# actual function
#---------------------------------------------#

def gender_labeler(contact_list,contact_email, database_filepath=gender_dir):
	
	"""
	

	"""
	# initialize
	name1_list    = [name.split(" ",1)[0] for name in contact_list]
	name2_prelist = [" ".join(name.split()[1:])for name in contact_list]
	name2_list    = [i.split(" ")[0] for i in name2_prelist]
	email1_list   = contact_email

	global in_list_1  
	global name_count
	global gender2
	global match_found2
	global in_list_2 
	global name_count
	global gender1
	global match_found1

	gender1 = ""
	gender2 = ""
	
	name_count   = 0
	hit_count    = 0
	missed_count = 0
	
	name_in_list          = []
	name_not_in_list      = []
	in_list_indeterminate = []
	gender_in_list        = []
	  
	in_list_1 =[]
	in_list_2 =[]

	match_found1 = False 
	match_found2 = False

	#outer loop, matching names
	for name1, name2, email1 in zip(name1_list, name2_list, email1_list):
		
		match_maker1(name1)  
		match_maker2(name2)
		
		# inner loop, deciding name/gender
		if (match_found1 == True) or (match_found2 == True):
								
					if (match_found1 == True) and (match_found2 == True):
						
						if gender1 == gender2:
							true_name = name1
							true_gender = gender1
							name_in_list.append(true_name)
							gender_in_list.append(true_gender)
							hit_count += 1 
							
						if (gender1 != gender2):
							if (name1 not in email1):                      
								 true_name = name1
								 true_gender = gender1
								 name_in_list.append(true_name)
								 gender_in_list.append(true_gender)
								 hit_count += 1 
								 
							elif (name2 not in email1):
								 true_name = name2
								 true_gender = gender2
								 name_in_list.append(true_name)
								 gender_in_list.append(true_gender)
								 hit_count += 1
								 
							else:
								 in_list_indeterminate.append(name1)
								 in_list_indeterminate.append(name2)
								 gender_in_list.append('I')
								 missed_count += 1
																										   
					elif (match_found1 == True) and (match_found2 == False):
							true_name = name1
							true_gender = gender1
							name_in_list.append(true_name)
							gender_in_list.append(true_gender)
							hit_count += 1 
							
					elif (match_found2 == True) and (match_found1 == False):
							true_name = name2
							true_gender = gender2
							name_in_list.append(true_name)
							gender_in_list.append(true_gender)
							hit_count += 1 
							
		if (match_found1 == False) and (match_found2 == False):
			name_not_in_list.append(name1)
			name_not_in_list.append(name2)
			gender_in_list.append('I')
			missed_count += 1
					  
	return(gender_in_list)
#---------------------------------------------#


