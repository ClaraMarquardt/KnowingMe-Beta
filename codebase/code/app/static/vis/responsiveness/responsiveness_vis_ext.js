console.log("responsiveness vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color_rate             = ["#08519c", "#08519c", "#08519c"]
var color_time             = ["#810f7c", "#810f7c", "#810f7c"]

// KEY
var width      = 700
var height     = 200
var height_svg = 190
var margin     = {top:50,bottom:100,left:50,right:50};

var svg = d3.select("#chart").append("svg")
            .attr("align","left")
            .attr("width", width)
            .attr("height",height + margin.top)
            .append("g")
            .attr("transform", "translate(" + 0 + "," + (margin.top+10) + ")");


// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function(mode) {

    var chart_data_rate_sent       = [];
    var chart_data_rate_received   = [];

    var chart_data_time_sent       = [];
    var chart_data_time_received   = [];

    for (var i = 0; i < Object.keys($response_rate_sent).length; i++) {
        chart_data_rate_sent.push({
          value:                 $response_rate_sent[i],
          value_default:         101,
          value_default_min:     d3.min($response_rate),
          label:                 $responsiveness_label[i],
          label_alt:             $responsiveness_label_alt[i],
          color:                 color_rate[i]
    });}

    for (var i = 0; i < Object.keys($response_rate_received).length; i++) {
        chart_data_rate_received.push({
          value:                 $response_rate_received[i],
          value_default:         101,
          value_default_min:     d3.min($response_rate),
          label:                 $responsiveness_label[i],
          label_alt:             $responsiveness_label_alt[i],
          color:                 color_rate[i]
    });}

    for (var i = 0; i < Object.keys($response_time_sent).length; i++) {
        chart_data_time_sent.push({
          value:                 $response_time_sent[i],
          value_default:         d3.max($response_time),
          value_default_min:     d3.min($response_time),
          label:                 $responsiveness_label[i],
          label_alt:             $responsiveness_label_alt[i],
          color:                 color_time[i]
    });}

    for (var i = 0; i < Object.keys($response_time_received).length; i++) {
        chart_data_time_received.push({
          value:                 $response_time_received[i],
          value_default:         d3.max($response_time),
          value_default_min:     d3.min($response_time),
          label:                 $responsiveness_label[i],
          label_alt:             $responsiveness_label_alt[i],
          color:                 color_time[i]
    });}
             
    if (mode=="Response Rate - Others (%)") {
        chart_data=chart_data_rate_sent
    } else if (mode=="Response Rate - You (%)") {
         chart_data=chart_data_rate_received
    } else if (mode=="Response Time - Others (Min)") {
        chart_data=chart_data_time_sent
    } else if (mode=="Response Time - You (Min)") {
        chart_data=chart_data_time_received
    }
    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {

  // # All Emails
  if (mode=="Response Rate - Others (%)") {

    if ($mean_response_rate_sent_female>($mean_response_rate_sent_male+$comparison_cutoff_response_rate)) {
      main_text = $text_dict[mode].female_respond
    } else if ($mean_response_rate_sent_male>($mean_response_rate_sent_female+$comparison_cutoff_response_rate)) {
      main_text = $text_dict[mode].male_respond
    } else {
      main_text = $text_dict[mode].equal
    }
  } 

  // # Sent Emails
  if (mode=="Response Rate - You (%)") {

   if ($mean_response_rate_received_female>($mean_response_rate_received_male+$comparison_cutoff_response_rate)) {
      main_text = $text_dict[mode].female_respond
    } else if ($mean_response_rate_received_male>($mean_response_rate_received_female+$comparison_cutoff_response_rate)) {
      main_text = $text_dict[mode].male_respond
    } else {
      main_text = $text_dict[mode].equal
    }
  } 

  // # Received Emails
  if (mode=="Response Time - Others (Min)") {

    if ($mean_response_time_sent_female>($mean_response_time_sent_male+$comparison_cutoff_response_time)) {
      main_text = $text_dict[mode].female_respond
    } else if ($mean_response_time_sent_male>($mean_response_time_sent_female+$comparison_cutoff_response_time)) {
      main_text = $text_dict[mode].male_respond
    } else {
      main_text = $text_dict[mode].equal
    }

  }

  // # response_time imbalance
  if (mode=="Response Time - You (Min)") {

    if ($mean_response_time_received_female>($mean_response_time_received_male+$comparison_cutoff_response_time)) {
      main_text = $text_dict[mode].female_respond
    } else if ($mean_response_time_received_male>($mean_response_time_received_female+$comparison_cutoff_response_time)) {
      main_text = $text_dict[mode].male_respond
    } else {
      main_text = $text_dict[mode].equal
    }

  }

  return({main_text:main_text})

} 


// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode, bar_number, text_content, text_duration, text_delay, function_new) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  generate_multi_bar(mode, chart_data = data_temp.chart_data, bar_number=bar_number, 
    delay_bar = 2000, duration_bar = 2000, delay_label = 2600, duration_label = 1000,
    label_main=mode, text_function="", label_size="10px")

  // # Update Text
  generate_text_main(text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}


// ## STAGES

// ## stage_entry
var stage_entry = function() {
  
  // # Initialize text
  d3.select("#text")
    .html("Loading ...");

  // # Call
  stage_0()
}

// ## stage_0
var stage_0 = function(mode="Response Rate - Others (%)") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Rate At Which Your Contacts Respond To Emails You Send.", 
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = stage_1

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)
}

// ## stage_1
var stage_1 = function(mode="Response Rate - You (%)") {

  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content =["Let's Look At The Rate At Which You Respond To Emails.",  
    text_temp.main_text, "LINK"]
  text_delay    =[0, 3500, 3500]
  text_duration =[1000,1000,1000]
  function_new  = stage_2

  // # Execute
  update_vis(mode=mode, bar_number=1, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}

// ## stage_2
var stage_2 = function(mode="Response Time - Others (Min)") {
 
  // # Generate text
  text_temp = update_text(mode=mode)
 
  // # Define
  text_content =["Let's Look At How Quickly Your Contacts Respond To Emails You Send.",  
    text_temp.main_text, "LINK"]
  text_delay    =[0, 3500, 3500]
  text_duration =[1000,1000,1000]
  function_new  = stage_3

  // # Execute
  update_vis(mode=mode, bar_number=2, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}

// ## stage_3
var stage_3 = function(mode="Response Time - You (Min)") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At How Quickly You Respond To Emails.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=3, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}

// # Launch
// # -------------
stage_entry()

// END
