var update_raw_data = function(raw_data) {

	// RAW DATA
	$earliest_date                      	= {{ earliest_date|tojson|safe }};
	$latest_date                        	= {{ latest_date|tojson|safe }};
	
	$email_date                        		= raw_data['graph_date']
	$email_count                       		= raw_data['graph_email_count']
	
	$min_day                     	        = {{ min_day|tojson|safe }};
	$min_email  						    = {{ min_email|tojson|safe }};
	$max_email  						    = {{ max_email|tojson|safe }};
	$timelag_min						    = {{ timelag_min|tojson|safe }};
	
	// MOD DATA
	$start_date_id_original                 = $email_date.indexOf($earliest_date)
	$end_date_id_original                   = $email_date.indexOf($latest_date)	

}