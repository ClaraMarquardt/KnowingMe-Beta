var update_raw_data = function(raw_data) {

	// RAW DATA
	$email_date                        		= raw_data['graph_date']
	$email_month                       		= raw_data['graph_month']
	$email_count                       		= raw_data['graph_email_count']
	
	$earliest_date                      	= {{ earliest_date|tojson|safe }};
	$latest_date                        	= {{ latest_date|tojson|safe }};
	$email_diff                        		= {{ date_diff|tojson|safe }};
	
	$email_date_subset                 		= raw_data['graph_date_subset']
	
	$email_count_subset                		= raw_data['graph_email_count_subset']
	$email_count_sent_subset           		= raw_data['graph_email_count_sent_subset']
	$email_count_received_subset       		= raw_data['graph_email_count_received_subset']
	
	$email_sample_subset                    = raw_data['graph_email_sample_subset']
	$email_sample_contact_subset			= raw_data['graph_email_sample_contact_subset'] 
	$email_sample_sent_subset               = raw_data['graph_email_sample_sent_subset']
	$email_sample_contact_sent_subset	    = raw_data['graph_email_sample_contact_sent_subset'] 
	$email_sample_received_subset           = raw_data['graph_email_sample_received_subset']
	$email_sample_contact_received_subset	= raw_data['graph_email_sample_contact_received_subset'] 
	
	$email_count_total  		  	   		= raw_data['stat_total_email']
	$email_count_total_per_day         		= raw_data['stat_email_per_day']
	
	$email_count_subset_total     	   		= raw_data['stat_subset_total_email']
	$email_count_subset_sent_total     		= raw_data['stat_subset_sent_total_email']
	$email_count_subset_received_total  	= raw_data['stat_subset_received_total_email']
	
	$lang_perc_eng  		  	   		    = raw_data['stat_perc_eng']
	
	// AGGREGATED DATA
	$start_date 							= new Date($earliest_date)
	$end_date   							= new Date($latest_date)

}