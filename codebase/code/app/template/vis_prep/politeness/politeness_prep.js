var update_raw_data = function(raw_data) {
	
	// RAW DATA
	$mean_politeness                     			 = raw_data['stat_mean_politeness']
	$mean_politeness_sent                			 = raw_data['stat_mean_politeness_sent']
	$mean_politeness_received            			 = raw_data['stat_mean_politeness_received']
	
	$mean_politeness_male                			 = raw_data['stat_mean_politeness_male']
	$mean_politeness_sent_male           			 = raw_data['stat_mean_politeness_sent_male']
	$mean_politeness_received_male       			 = raw_data['stat_mean_politeness_received_male']
	
	$mean_politeness_female              			 = raw_data['stat_mean_politeness_female']
	$mean_politeness_sent_female         			 = raw_data['stat_mean_politeness_sent_female']
	$mean_politeness_received_female     			 = raw_data['stat_mean_politeness_received_female']
	
	$mean_politeness_imbalance           			 = raw_data['stat_mean_politeness_imbalance']
	$mean_politeness_imbalance_male      			 = raw_data['stat_mean_politeness_imbalance_male']
	$mean_politeness_imbalance_female    			 = raw_data['stat_mean_politeness_imbalance_female']
	
	
	// AGGREGATED DATA
	$politeness_label                 				 = ["Very Polite", "All","Female","Male"]
	$politeness_label_alt      		 				 = ["Very Polite", "","",""]
	
	$imbalance_label           		 				 = ["No Imbalance", "All","Female","Male"]
	$imbalance_label_alt       	     				 = ["No Imbalance", "","",""]
	
	$politeness           	  		 				 = [1, $mean_politeness,$mean_politeness_female,$mean_politeness_male];
	$politeness_sent           		 				 = [1, $mean_politeness_sent,$mean_politeness_sent_female,$mean_politeness_sent_male];
	$politeness_received       		 				 = [1, $mean_politeness_received,$mean_politeness_received_female,$mean_politeness_received_male];
	$politeness_imbalance     		 				 = [1, $mean_politeness_imbalance,$mean_politeness_imbalance_female,$mean_politeness_imbalance_male];
	
	// DYNAMIC TEXT VARIABLES
	$comparison_cutoff                 				 = 0.01
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["All Emails"] 						 = {};
	$text_dict["All Emails"].equal  			 	 = "The emails you sent and received from female and male contacts were equally polite.";
	$text_dict["All Emails"].female_polite    		 = "The emails you sent and received from female contacts were more polite <br>than those you received From male contacts.";
	$text_dict["All Emails"].male_polite    	 	 = "The emails you sent and received from male contacts were more polite <br>than those you received From female contacts.";
	
	$text_dict["Sent Emails"] 						 = {};
	$text_dict["Sent Emails"].equal          	  	 = "The emails you sent to female and male contacts were equally polite.";
	$text_dict["Sent Emails"].female_polite  		 = "The emails you sent to female contacts were more polite <br>than those you sent to male contacts.";
	$text_dict["Sent Emails"].male_polite    		 = "The emails you sent to male contacts were more polite <br>than those you sent to female contacts.";
	
	$text_dict["Received Emails"] 				     = {};
	$text_dict["Received Emails"].equal          	 = "The emails you received from female and male contacts were equally polite.";
	$text_dict["Received Emails"].female_polite      = "The emails you received from female contacts were more polite <br>than those you received from male contacts.";
	$text_dict["Received Emails"].male_polite        = "The emails you received from male contacts were more polite <br>than those you received from female contacts.";
	
	$text_dict["Politeness Imbalance"] 				  = {};
	$text_dict["Politeness Imbalance"]['female']	  = {};
	$text_dict["Politeness Imbalance"].female.equal   = "The emails you sent to female contacts were as polite as the emails you responded to.";
	$text_dict["Politeness Imbalance"].female.pos     = "The emails you sent to female contacts were more polite than the emails you responded to.";
	$text_dict["Politeness Imbalance"].female.neg     = "The emails you sent to female contacts were less polite than the emails you responded to.";
	
	$text_dict["Politeness Imbalance"]['male']	      = {};
	$text_dict["Politeness Imbalance"].male.equal     = "The emails you sent to male contacts were as polite as the emails you responded to.";
	$text_dict["Politeness Imbalance"].male.pos       = "The emails you sent to male contacts were more polite than the emails you responded to.";
	$text_dict["Politeness Imbalance"].male.neg       = "The emails you sent to male contacts were less polite than the emails you responded to.";

}
