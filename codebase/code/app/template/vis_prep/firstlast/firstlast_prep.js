var update_raw_data = function(raw_data) {
	
	// RAW DATA
	$mean_first_sent              	      = raw_data['stat_mean_first']
	$mean_first_sent_female           	  = raw_data['stat_mean_first_female']
	$mean_first_sent_male         	      = raw_data['stat_mean_first_male']

	$mean_last_sent              	      = raw_data['stat_mean_last']
	$mean_last_sent_female           	  = raw_data['stat_mean_last_female']
	$mean_last_sent_male         	      = raw_data['stat_mean_last_male']

	// AGGREGATED DATA
	$firstlast_label                	  = ["All","Female","Male"]
	
	$first                                = [$mean_first_sent,$mean_first_sent_female,$mean_first_sent_male];
	$last           	  		          = [$mean_last_sent,$mean_last_sent_female,$mean_last_sent_male];
	
	// DYNAMIC TEXT VARIABLES
	$comparison_cutoff                    = 1
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["First"] 				       = {};
	$text_dict["First"].equal  		           = "You were equally likely to be the person starting the conversation in conversations with female and male contacts.";
	$text_dict["First"].female_first           = "You were more likely to be the person starting the conversation in conversations with female contacts <br>than in conversations with male contacts.";
	$text_dict["First"].male_first    	       = "You were more likely to be the person starting the conversation in conversations with male contacts <br>than in conversations with female contacts.";
	
	$text_dict["Last"] 				       	   = {};
	$text_dict["Last"].equal  		           = "You were equally likely to be the person ending the conversation in conversations with female and male contacts.";
	$text_dict["Last"].female_last             = "You were more likely to be the person ending the conversation in conversations with female contacts <br>than in conversations with male contacts.";
	$text_dict["Last"].male_last    	       = "You were more likely to be the person ending the conversation in conversations with male contacts <br>than in conversations with female contacts.";
		
}

