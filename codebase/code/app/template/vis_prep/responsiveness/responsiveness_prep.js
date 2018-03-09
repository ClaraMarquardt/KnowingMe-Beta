var update_raw_data = function(raw_data) {

	// RAW DATA
	$mean_response_rate_sent              	  = raw_data['stat_mean_response_rate_sent']
	$mean_response_rate_sent_female           = raw_data['stat_mean_response_rate_sent_female']
	$mean_response_rate_sent_male         	  = raw_data['stat_mean_response_rate_sent_male']

	$mean_response_rate_received              = raw_data['stat_mean_response_rate_received']
	$mean_response_rate_received_female       = raw_data['stat_mean_response_rate_received_female']
	$mean_response_rate_received_male         = raw_data['stat_mean_response_rate_received_male']
	
	$mean_response_time_sent              	  = raw_data['stat_mean_response_time_sent']
	$mean_response_time_sent_female       	  = raw_data['stat_mean_response_time_sent_female']
	$mean_response_time_sent_male             = raw_data['stat_mean_response_time_sent_male']

	$mean_response_time_received              = raw_data['stat_mean_response_time_received']
	$mean_response_time_received_female       = raw_data['stat_mean_response_time_received_female']
	$mean_response_time_received_male         = raw_data['stat_mean_response_time_received_male']

	// AGGREGATED DATA
	$responsiveness_label                	  = ["All","Female","Male"]
	$responsiveness_label_alt      		      = ["","",""]
	
	$response_rate           	  		      = [$mean_response_rate_sent,$mean_response_rate_sent_female,$mean_response_rate_sent_male,$mean_response_rate_received,$mean_response_rate_received_female,$mean_response_rate_received_male];
	$response_rate_sent           	  		  = [$mean_response_rate_sent,$mean_response_rate_sent_female,$mean_response_rate_sent_male];
	$response_rate_received           	      = [$mean_response_rate_received,$mean_response_rate_received_female,$mean_response_rate_received_male];

	$response_time           	  		      = [$mean_response_time_sent,$mean_response_time_sent_female,$mean_response_time_sent_male,$mean_response_time_received,$mean_response_time_received_female,$mean_response_time_received_male];
	$response_time_sent           		 	  = [$mean_response_time_sent,$mean_response_time_sent_female,$mean_response_time_sent_male];
	$response_time_received           		  = [$mean_response_rate_received,$mean_response_rate_received_female,$mean_response_rate_received_male];
	
	// DYNAMIC TEXT VARIABLES
	$comparison_cutoff_response_rate          = 1
	$comparison_cutoff_response_time          = 1
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["Response Rate - Others (%)"] 				       = {};
	$text_dict["Response Rate - Others (%)"].equal  		       = "Female And Male Contacts Responded To Your Emails At The Same Rate.";
	$text_dict["Response Rate - Others (%)"].female_respond        = "Female Contacts Responded To Your Emails At A Higher Rate Than Male Contacts.";
	$text_dict["Response Rate - Others (%)"].male_respond     	   = "Male Contacts Responded To Your Emails At A Higher Rate Than Female Contacts.";
	
	$text_dict["Response Rate - You (%)"] 				   			= {};
	$text_dict["Response Rate - You (%)"].equal  		   			= "You Responded To Female And Male Contacts At The Same Rate.";
	$text_dict["Response Rate - You (%)"].female_respond   			= "You Responded To Female Contacts At A Higher Rate Than To Male Contacts.";
	$text_dict["Response Rate - You (%)"].male_respond     			= "You Responded To Male Contacts At A Higher Rate Than To Female Contacts.";

	$text_dict["Response Time - Others (Min)"] 				       	= {};
	$text_dict["Response Time - Others (Min)"].equal  		       	= "Female And Male Contacts Responded To Your Emails Equally Quickly.";
	$text_dict["Response Time - Others (Min)"].female_respond       = "Female Contacts Responded To Your Emails More Quickly Than Male Contacts.";
	$text_dict["Response Time - Others (Min)"].male_respond     	= "Male Contacts Responded To Your Emails More Quickly Than Female Contacts.";
	
	$text_dict["Response Time - You (Min)"] 				   			= {};
	$text_dict["Response Time - You (Min)"].equal  		   			= "You Responded To Female And Male Contacts Equally Quickly.";
	$text_dict["Response Time - You (Min)"].female_respond   			= "You Responded To Female Contacts More Quickly Than To Male Contacts.";
	$text_dict["Response Time - You (Min)"].male_respond     			= "You Responded To Male Contacts More Quickly Than To Female Contacts.";
		
}