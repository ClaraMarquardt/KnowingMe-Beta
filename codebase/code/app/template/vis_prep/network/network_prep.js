var update_raw_data = function(raw_data) {
	
	// RAW DATA
	$contact_gender               	= raw_data['graph_contact_gender']
	$contact_name                 	= raw_data['graph_contact_name']
	$contact_email                	= raw_data['graph_contact_email']
	$contact_sent                 	= raw_data['graph_network_matrix_sent']
	$contact_received             	= raw_data['graph_network_matrix_received']
	
	$network_matrix         	  	= raw_data['graph_network_matrix']
	$network_matrix_female        	= raw_data['graph_network_matrix_female']
	$network_matrix_male          	= raw_data['graph_network_matrix_male']

	$total_contact_perc             = raw_data['stat_total_contact_perc']
	$total_contact                	= raw_data['stat_total_contact']
	$perc_female                  	= raw_data['stat_perc_female']
	$perc_na                      	= raw_data['stat_perc_na']
	
	$most_contact                 	= raw_data['stat_most_contact']
	$most_contact_sent            	= raw_data['stat_most_contact_sent']
	$most_contact_received        	= raw_data['stat_most_contact_received']
	
	$most_contact_male              = raw_data['stat_most_contact_male']
	$most_contact_sent_male         = raw_data['stat_most_contact_sent_male']
	$most_contact_received_male     = raw_data['stat_most_contact_received_male']
	
	$most_contact_female            = raw_data['stat_most_contact_female']
	$most_contact_sent_female       = raw_data['stat_most_contact_sent_female']
	$most_contact_received_female   = raw_data['stat_most_contact_received_female']

}