console.log("time_dist vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var buckets            = 6
var colors             = ["#c6dbef","#9ecae1","#4292c6","#2171b5","#08519c","#08306b"]
var days               = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
var times              = ["0a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p"]
var days_long          = ["Monday ", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
var times_long         = ["0am-1am", "1am-2am", "2am-3am", "3am-4am", "4am-5am", "5am-6am", "6am-7am", "7am-8am", "8am-9am", "9am-10am", "10am-11am", "11am-12pm", "12pm-1pm", "1pm-2pm", "2pm-3pm", "3pm-4pm", "4pm-5pm", "5pm-6pm", "6pm-7pm", "7pm-8pm", "8pm-9pm", "9pm-10pm", "10pm-11pm", "11pm-12pm"]
var daytime            = ["", "", "Night  \uf236", "", "", "", "", "", "Morning  \uf0f4", "", "", "", "", "", "Afternoon  \uf185", "", "", "", "", "", "Evening  \uf186", "", "", ""]

// KEY
var width      = 700
var width_svg  = 700
var height     = 200
var height_svg = 200
var margin     = {top:50,bottom:90,left:50,right:50};

var gridSize           = Math.floor(width / 24)
var legendElementWidth = gridSize*2

var svg = d3.select("#chart").append("svg")
            .attr("width", width_svg + margin.right + margin.left)
            .attr("height", height_svg + margin.bottom + margin.top)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
var g = svg

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function(mode) {

    var chart_data = [];
  
  if (mode=="All Emails") {
    for (var i = 0; i < Object.keys($date_weekday).length; i++) {
      chart_data.push({
        day:  $date_weekday[i],
        hour: $date_hour[i],
        value: $email_count[i], 
        value_default_max: d3.max($email_count)
      });
    }
  } else if (mode=="Sent Emails") {
    for (var i = 0; i < Object.keys($date_weekday_sent).length; i++) {
      chart_data.push({
        day:  $date_weekday_sent[i],
        hour: $date_hour_sent[i],
        value: $email_count_sent[i], 
        value_default_max: d3.max($email_count)
      });
    }
  } else if (mode=="Received Emails") {
    for (var i = 0; i < Object.keys($date_weekday_received).length; i++) {
      chart_data.push({
        day:  $date_weekday_received[i],
        hour: $date_hour_received[i],
        value: $email_count_received[i], 
        value_default_max: d3.max($email_count)
      });
    }
  }
 
    return({chart_data:chart_data})

}


// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {

  // # All Emails
  if (mode=="All Emails") {

    main_text = "You corresponded the most on " + $date_weekday_most + ". You corresponded the most in the "+ $date_daypart_most + ".<br> "+"You corresponded the least on " + $date_weekday_least + ". You corresponded the least in the " + $date_daypart_least + ".<br><i> All times are rendered in " + $timezone_utc_name + " (UTC-" + $timezone_utc_offset+").</i>" 


  } 

  // # Sent Emails
  if (mode=="Sent Emails") {

    main_text = "You sent the most emails on " + $date_weekday_sent_most + ". You sent the most emails in the "+ $date_daypart_sent_most + ".<br> "+"You sent the fewest emails on " + $date_weekday_sent_least + ". You sent the fewest emails in the " + $date_daypart_sent_least + "."

  } 

  // # Received Emails
  if (mode=="Received Emails") {

    main_text = "You received the most emails on " + $date_weekday_received_most + ". You received the most emails in the "+ $date_daypart_received_most + ".<br> "+"You received the fewest emails on " + $date_weekday_received_least + ". You received the fewest emails in the " + $date_daypart_received_least  + "."

  }

  return({main_text:main_text})

} 


// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode, text_content) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  generate_heatmap(chart_data = data_temp.chart_data, chart_data_general = data_temp.chart_data_general)

  // # Update Text
  generate_text_main(text_content=text_content, text_duration=[1000], 
    text_delay=[0], function_new="")

}

// ## stage function
var update_stage = function(mode) {

  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text]

  // # Execute
  update_vis(mode=mode, 
    text_content=text_content)

}


// ## STAGES

// ## stage_entry
var stage_entry = function() {
  
  // # Initialize text
  d3.select("#text")
    .html("Loading ...");

  // # Call
  stage_0()

  // # Initialize buttons 
  generate_button(width=70, displ_x_origin=170,displ_x_step=150, displ_y_origin=-35,displ_y_step=0,
    button_label    = ["All Emails", "Sent Emails", "Received Emails"],
    button_function = [stage_0, stage_1, stage_2],
    button_type = ["button","button","button"],
    button_move = [10,10,3])

}

// ## stage_0
var stage_0 = function(mode="All Emails") {

  // # Call
    update_stage(mode=mode)

}

// ## stage_1
var stage_1 = function(mode="Sent Emails") {

  // # Call
    update_stage(mode=mode)

}

// ## stage_2
var stage_2 = function(mode="Received Emails") {

  // # Call
    update_stage(mode=mode)

}


// # Launch
// # -------------
stage_entry()

// END
