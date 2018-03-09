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
	$text_dict["All Emails"].equal  			 	 = "The Emails You Sent And Received From Female and Male Contacts Were Equally Polite.";
	$text_dict["All Emails"].female_polite    		 = "The Emails You Sent And Received From Female Contacts Were More Polite <br>Than Those You Received From Male Contacts.";
	$text_dict["All Emails"].male_polite    	 	 = "The Emails You Sent And Received From Male Contacts Were More Polite <br>Than Those You Received From Female Contacts.";
	
	$text_dict["Sent Emails"] 						 = {};
	$text_dict["Sent Emails"].equal          	  	 = "The Emails You Sent To Female and Male Contacts Were Equally Polite.";
	$text_dict["Sent Emails"].female_polite  		 = "The Emails You Sent To Female Contacts Were More Polite <br>Than Those You Sent To Male Contacts.";
	$text_dict["Sent Emails"].male_polite    		 = "The Emails You Sent To Male Contacts Were More Polite <br>Than Those You Sent To Female Contacts.";
	
	$text_dict["Received Emails"] 				     = {};
	$text_dict["Received Emails"].equal          	 = "The Emails You Received From Female and Male Contacts Were Equally Polite.";
	$text_dict["Received Emails"].female_polite      = "The Emails You Received From Female Contacts Were More Polite <br>Than Those You Received From Male Contacts.";
	$text_dict["Received Emails"].male_polite        = "The Emails You Received From Male Contacts Were More Polite <br>Than Those You Received From Female Contacts.";
	
	$text_dict["Politeness Imbalance"] 				  = {};
	$text_dict["Politeness Imbalance"]['female']	  = {};
	$text_dict["Politeness Imbalance"].female.equal   = "The Emails You Sent To Female Contacts Were As Polite As The Emails You Responded To.";
	$text_dict["Politeness Imbalance"].female.pos     = "The Emails You Sent To Female Contacts Were Meaningfully More Polite Than The Emails You Responded To.";
	$text_dict["Politeness Imbalance"].female.neg     = "The Emails You Sent To Female Contacts Were Meaningfully Less Polite Than The Emails You Responded To.";
	
	$text_dict["Politeness Imbalance"]['male']	      = {};
	$text_dict["Politeness Imbalance"].male.equal     = "The Emails You Sent To Male Contacts Were As Polite As The Emails You Responded To.";
	$text_dict["Politeness Imbalance"].male.pos       = "The Emails You Sent To Male Contacts Were Meaningfully More Polite Than The Emails You Responded To.";
	$text_dict["Politeness Imbalance"].male.neg       = "The Emails You Sent To Male Contacts Were Meaningfully Less Polite Than The Emails You Responded To.";

}
