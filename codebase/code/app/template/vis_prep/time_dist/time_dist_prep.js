var update_raw_data = function(raw_data) {

	// RAW DATA
	$date_weekday               	= raw_data['graph_weekday']
	$date_hour                  	= raw_data['graph_hour']
	$email_count                	= raw_data['graph_email_count']
	
	$date_weekday_sent          	= raw_data['graph_weekday_sent']
	$date_hour_sent             	= raw_data['graph_hour_sent']
	$email_count_sent           	= raw_data['graph_email_count_sent']
	
	$date_weekday_received      	= raw_data['graph_weekday_received']
	$date_hour_received         	= raw_data['graph_hour_received']
	$email_count_received       	= raw_data['graph_email_count_received']
	
	$date_weekday_most          	= raw_data['stat_most_email_weekday']
	$date_daypart_most          	= raw_data['stat_most_email_daypart']
	$date_weekday_least         	= raw_data['stat_least_email_weekday']
	$date_daypart_least        		= raw_data['stat_least_email_daypart']
	
	$date_weekday_sent_most     	= raw_data['stat_most_email_weekday_sent']
	$date_daypart_sent_most     	= raw_data['stat_most_email_daypart_sent']
	$date_weekday_sent_least    	= raw_data['stat_least_email_weekday_sent']
	$date_daypart_sent_least    	= raw_data['stat_least_email_daypart_sent']
	
	$date_weekday_received_most     = raw_data['stat_most_email_weekday_received']
	$date_daypart_received_most     = raw_data['stat_most_email_daypart_received']
	$date_weekday_received_least    = raw_data['stat_least_email_weekday_received']
	$date_daypart_received_least    = raw_data['stat_least_email_daypart_received']
	
	$timezone_utc_offset            = {{ timezone_utc_offset|tojson|safe }};
	$timezone_utc_name              = {{ timezone_utc_name|tojson|safe }};

}