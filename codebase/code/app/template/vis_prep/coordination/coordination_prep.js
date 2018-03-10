var update_raw_data = function(raw_data) {
	
	// RAW DATA
	$mean_coordination                     			 = raw_data['stat_mean_coordination']	
	$mean_coordination_male                			 = raw_data['stat_mean_coordination_male']	
	$mean_coordination_female              			 = raw_data['stat_mean_coordination_female']
			
	// AGGREGATED DATA
	$coordination_label                 			 = [ "Perfect Coordination", "All","Female","Male"]
	$coordination_label_alt      		 		     = [ "Perfect Coordination", "","",""]
		
	$coordination           	  		 			 = [ 1, $mean_coordination,$mean_coordination_female,$mean_coordination_male];
	
	// DYNAMIC TEXT VARIABLES
	$comparison_cutoff                 				 = 0.01
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["All Emails"] 						 = {};
	$text_dict["All Emails"].equal  			 	 = "You coordinate to the same degree with female and male contacts.";
	$text_dict["All Emails"].female_coordinate       = "You coordinate more with female contacts than with male contacts.";
	$text_dict["All Emails"].male_coordinate    	 = "You coordinate more with male contacts than with female contacts.";
		
}
