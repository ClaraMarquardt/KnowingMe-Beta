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
	
	$text_dict["Received Response (%)"] 				        = {};
	$text_dict["Received Response (%)"].equal  		            = "Female and male contacts responded to your emails at the same rate.";
	$text_dict["Received Response (%)"].female_respond          = "Female contacts responded to your emails at a higher rate than male contacts.";
	$text_dict["Received Response (%)"].male_respond     	    = "Male contacts responded to your emails at a higher rate than female contacts.";
	
	$text_dict["Sent Response (%)"] 				   			= {};
	$text_dict["Sent Response (%)"].equal  		   			    = "You responded to female and male contacts at the same rate.";
	$text_dict["Sent Response (%)"].female_respond   			= "You responded to female contacts at a higher rate than to male contacts.";
	$text_dict["Sent Response (%)"].male_respond     			= "You responded to male contacts at a higher rate than to female contacts.";

	$text_dict["Time to Response Receipt (Min)"] 				= {};
	$text_dict["Time to Response Receipt (Min)"].equal  		= "Female and male contacts responded to your emails equally quickly.";
	$text_dict["Time to Response Receipt (Min)"].female_respond = "Female contacts responded to your emails more quickly than male contacts.";
	$text_dict["Time to Response Receipt (Min)"].male_respond   = "Male contacts responded to your emails more quickly than female contacts.";
	
	$text_dict["Time to Sent Response (Min)"] 				   	= {};
	$text_dict["Time to Sent Response (Min)"].equal  		   	= "You responded to female and male contacts equally quickly.";
	$text_dict["Time to Sent Response (Min)"].female_respond   	= "You responded to female contacts more quickly than to male contacts.";
	$text_dict["Time to Sent Response (Min)"].male_respond     	= "You responded to male contacts more quickly than to female contacts.";
		
}