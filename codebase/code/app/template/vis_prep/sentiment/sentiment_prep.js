var update_raw_data = function(raw_data) {

	// RAW DATA
	$mean_positivity                     			= raw_data['stat_mean_positivity']
	$mean_positivity_sent                			= raw_data['stat_mean_positivity_sent']
	$mean_positivity_received            			= raw_data['stat_mean_positivity_received']
	
	$mean_positivity_male                			= raw_data['stat_mean_positivity_male']
	$mean_positivity_sent_male           			= raw_data['stat_mean_positivity_sent_male']
	$mean_positivity_received_male       			= raw_data['stat_mean_positivity_received_male']
	
	$mean_positivity_female              			= raw_data['stat_mean_positivity_female']
	$mean_positivity_sent_female         			= raw_data['stat_mean_positivity_sent_female']
	$mean_positivity_received_female     			= raw_data['stat_mean_positivity_received_female']
	
	$mean_positivity_imbalance           			= raw_data['stat_mean_positivity_imbalance']
	$mean_positivity_imbalance_male      			= raw_data['stat_mean_positivity_imbalance_male']
	$mean_positivity_imbalance_female    			= raw_data['stat_mean_positivity_imbalance_female']
	
	
	// AGGREGATED DATA
	$positivity_label                 				= ["Neutral", "All","Female","Male"]
	$positivity_label_alt      		 				= ["Neutral", "","",""]
	
	$imbalance_label           		 				= ["No Imbalance", "All","Female","Male"]
	$imbalance_label_alt       	     				= ["No Imbalance", "","",""]
				
	$positivity           	  		 				= [0.5, $mean_positivity,$mean_positivity_female,$mean_positivity_male];
	$positivity_sent           		 				= [0.5, $mean_positivity_sent,$mean_positivity_sent_female,$mean_positivity_sent_male];
	$positivity_received       		 				= [0.5, $mean_positivity_received,$mean_positivity_received_female,$mean_positivity_received_male];
	$positivity_imbalance     		 				= [1, $mean_positivity_imbalance,$mean_positivity_imbalance_female,$mean_positivity_imbalance_male];
	
	// DYNAMIC TEXT VARIABLES
	$comparison_cutoff                  			= 0.01
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["All Emails"] 						 = {};
	$text_dict["All Emails"].equal  			     = "The emails you sent and received from female and male contacts were equally positive.";
	$text_dict["All Emails"].female_polite    		 = "The emails you sent and received from female contacts were more positive <br>than those you received from male contacts.";
	$text_dict["All Emails"].male_polite    	     = "The emails you sent and received from male contacts were more positive <br>than those you received from female contacts.";
	
	$text_dict["Sent Emails"] 						 = {};
	$text_dict["Sent Emails"].equal          	  	 = "The emails you sent to female and male contacts were equally positive.";
	$text_dict["Sent Emails"].female_polite  		 = "The emails you sent to female contacts were more positive <br>than those you sent to male contacts.";
	$text_dict["Sent Emails"].male_polite    		 = "The emails you sent to male contacts were more positive <br>than those you sent to female contacts.";
	
	$text_dict["Received Emails"] 				     = {};
	$text_dict["Received Emails"].equal          	 = "The emails you received from female and male contacts were equally positive.";
	$text_dict["Received Emails"].female_polite      = "The emails you received from female contacts were more positive <br>than those you received from male contacts.";
	$text_dict["Received Emails"].male_polite        = "The emails you received from male contacts were more positive <br>than those you received from female contacts.";
	
	$text_dict["Positivity Imbalance"] 				 = {};
	$text_dict["Positivity Imbalance"]['female']	 = {};
	$text_dict["Positivity Imbalance"].female.equal  = "The emails you sent to female contacts were as positive as the emails you responded to.";
	$text_dict["Positivity Imbalance"].female.pos    = "The emails you sent to female contacts were more positive than the emails you responded to.";
	$text_dict["Positivity Imbalance"].female.neg    = "The emails you sent to female contacts were less positive than the emails you responded to.";
	
	$text_dict["Positivity Imbalance"]['male']	     = {};
	$text_dict["Positivity Imbalance"].male.equal    = "The emails you sent to male contacts were as positive as the emails you responded to.";
	$text_dict["Positivity Imbalance"].male.pos      = "The emails you sent to male contacts were more positive than the emails you responded to.";
	$text_dict["Positivity Imbalance"].male.neg      = "The emails you sent to male contacts were less positive than the emails you responded to.";
	
}