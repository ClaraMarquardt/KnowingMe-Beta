var update_raw_data = function(raw_data) {
		
	$mean_character_count_sent               = raw_data['stat_mean_character_count_sent']
	$mean_character_count_sent_male          = raw_data['stat_mean_character_count_sent_male']
	$mean_character_count_sent_female        = raw_data['stat_mean_character_count_sent_female']
 
	$mean_word_count_sent            	     = raw_data['stat_mean_word_count_sent']
	$mean_word_count_sent_male               = raw_data['stat_mean_word_count_sent_male']
	$mean_word_count_sent_female             = raw_data['stat_mean_word_count_sent_female']
 
	$mean_sentence_count_sent                = raw_data['stat_mean_sentence_count_sent']
	$mean_sentence_count_sent_male           = raw_data['stat_mean_sentence_count_sent_male']
	$mean_sentence_count_sent_female         = raw_data['stat_mean_sentence_count_sent_female']
 
	$mean_character_imbalance         		 = raw_data['stat_mean_character_imbalance']
	$mean_character_imbalance_male    		 = raw_data['stat_mean_character_imbalance_male']
	$mean_character_imbalance_female  		 = raw_data['stat_mean_character_imbalance_female']
 
	$mean_word_imbalance         			 = raw_data['stat_mean_word_imbalance']
	$mean_word_imbalance_male    			 = raw_data['stat_mean_word_imbalance_male']
	$mean_word_imbalance_female  			 = raw_data['stat_mean_word_imbalance_female']
 
	$mean_sentence_imbalance         		 = raw_data['stat_mean_sentence_imbalance']
	$mean_sentence_imbalance_male    		 = raw_data['stat_mean_sentence_imbalance_male']
	$mean_sentence_imbalance_female  		 = raw_data['stat_mean_character_imbalance_female']
 
	// AGGREGATED DATA 
	$imbalance_label           		 		 = ["No Imbalance", "All","Female","Male"]
	$imbalance_label_alt           		 	 = ["No Imbalance", "","",""]
	 
	$count_label           		 		 	 = ["All","Female","Male"]
	$count_label_alt           		 		 = ["", "",""]
 
	$character_count_sent     		 		 = [$mean_character_count_sent,$mean_character_count_sent_female,$mean_character_count_sent_male];
	$word_count_sent     		 			 = [$mean_word_count_sent,$mean_word_count_sent_female,$mean_word_count_sent_male];
	$sentence_count_sent     		 		 = [$mean_sentence_count_sent,$mean_sentence_count_sent_female,$mean_sentence_count_sent_male];
 
	$character_imbalance     		 		 = [1, $mean_character_imbalance,$mean_character_imbalance_female,$mean_character_imbalance_male];
	$word_imbalance     		 			 = [1, $mean_word_imbalance,$mean_word_imbalance_female,$mean_word_imbalance_male];
	$sentence_imbalance     		 		 = [1, $mean_sentence_imbalance,$mean_sentence_imbalance_female,$mean_sentence_imbalance_male];
 
	// DYNAMIC TEXT VARIABLES 
	$comparison_cutoff_count                 = 1
	$comparison_cutoff_imbalance             = 0.01
	
	// DYNAMIC TEXT
	$text_dict   = {};
	
	$text_dict["Count"] 					 = {};
	$text_dict["Count"].equal  			     = "The Emails You Sent To Female and Male Contacts Were Equally Long.";
	$text_dict["Count"].female_talkative     = "The Emails You Sent To Female Contacts Were Longer <br>Than Those You Sent To Male Contacts.";
	$text_dict["Count"].male_talkative    	 = "The Emails You Sent To Male Contacts Were Longer <br>Than Those You Sent To Female Contacts.";
	
	$text_dict["Imbalance"] 				 = {};
	$text_dict["Imbalance"]['female']	     = {};
	$text_dict["Imbalance"].female.equal     = "The Emails You Sent To Female Contacts Were As Long As The Emails You Responded To.";
	$text_dict["Imbalance"].female.pos       = "The Emails You Sent To Female Contacts Were Meaningfully Longer Than The Emails You Responded To.";
	$text_dict["Imbalance"].female.neg       = "The Emails You Sent To Female Contacts Were Meaningfully Shorter Than The Emails You Responded To.";
	
	$text_dict["Imbalance"]['male']	         = {};
	$text_dict["Imbalance"].male.equal       = "The Emails You Sent To Male Contacts Were As Long As The Emails You Responded To.";
	$text_dict["Imbalance"].male.pos         = "The Emails You Sent To Male Contacts Were Meaningfully Longer Than The Emails You Responded To.";
	$text_dict["Imbalance"].male.neg         = "The Emails You Sent To Male Contacts Were Meaningfully Shorter Than The Emails You Responded To.";

}