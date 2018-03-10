console.log("date_dist vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color       = d3.scaleOrdinal(d3.schemeCategory10);
var fill_color  = ["#02091e", "#002fbc"]

// KEY
var width      = 700
var width_svg  = 700
var height     = 400
var height_svg = 350
var start      = 0
var end        = 2.25
var numSpirals = 3
var margin     = {top:0,bottom:0,left:0,right:0}

var svg = d3.select("#chart").append("svg")
             .attr("align","left")
             .attr("width", width)
             .attr("height", height_svg)
             .append("g")

var g = svg

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function(mode) {

    var chart_data_overview         = [];
    var chart_data_overview_subset  = [];
    var chart_data_all              = [];
    var chart_data_sent             = [];
    var chart_data_received         = [];


    for (var i = 0; i < Object.keys($email_date).length; i++) {  
      chart_data_overview.push({
        date: new Date($email_date[i]) ,
        value: $email_count[i],
        col_group: 0

    });}

    for (var i = 0; i < Object.keys($email_date).length; i++) { 
      date_temp = new Date($email_date[i])
      chart_data_overview_subset.push({
        date: new Date($email_date[i]), 
        value: $email_count[i],
        col_group: date_temp<=$end_date & date_temp>=$start_date

    });}

    for (var i = 0; i < $email_date_subset.length; i++) {
      chart_data_all.push({
        date: new Date($email_date_subset[i]),
        value_default: $email_count_subset[i],
        value: $email_count_subset[i],
        sample: $email_sample_contact_subset[i],
        sample_detail: $email_sample_subset[i]
      });}
 

    for (var i = 0; i < $email_date_subset.length; i++) {
      chart_data_sent.push({
        date: new Date($email_date_subset[i]),
        value_default: $email_count_subset[i],
        value: $email_count_sent_subset[i],
        sample: $email_sample_contact_sent_subset[i],
        sample_detail: $email_sample_sent_subset[i]
      });}


    for (var i = 0; i < $email_date_subset.length; i++) {
      chart_data_received.push({
        date: new Date($email_date_subset[i]),
        value_default: $email_count_subset[i],
        value: $email_count_received_subset[i],
        sample: $email_sample_contact_received_subset[i],
        sample_detail: $email_sample_received_subset[i]
      });}
     
    if (mode=="Overview") {
        chart_data=chart_data_overview
    } else if (mode=="Overview Subset") {
        chart_data=chart_data_overview_subset
    } else if (mode=="All Emails") {
        chart_data=chart_data_all
    } else if (mode=="Sent Emails") {
         chart_data=chart_data_sent
    } else if (mode=="Received Emails") {
        chart_data=chart_data_received
    } 
    
    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {


  // # Overview
  if (mode=="Overview") {

    main_text = "Over the past 365 days you sent and received " + $email_count_total + " emails - that's "+ Math.round($email_count_total_per_day) +" emails per day."
  
  } 

  if (mode=="Overview Subset") {

    main_text = "We've closely analyzed your last "+ $email_count_subset_total +" emails over the period "+ $earliest_date +" to "+ $latest_date + ". <br> To ensure that the analysis is meaningful we have focused on all emails with text content."
  
  } 

  // # All Emails
  if (mode=="All Emails") {


    main_text = "Over these "+ $email_diff +" days you sent and received "+ $email_count_subset_total  +" emails.<br><i> " + "" + Math.round($lang_perc_eng)  + "% of those emails were in English - for some insights we will only be looking at this subset of emails.</i>"


  } 

  // # Sent Emails
  if (mode=="Sent Emails") {

    main_text = "Over these "+ $email_diff +" days you sent "+ $email_count_subset_sent_total  +" emails."

  } 

  // # Received Emails
  if (mode=="Received Emails") {

    main_text = "Over these "+ $email_diff +" days you received "+ $email_count_subset_received_total  +" emails."

  }

  return({main_text:main_text})

} 


// END

// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode, text_content, function_new, text_delay=text_delay, text_duration=text_duration) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  if (mode=="Overview" | mode=="Overview Subset") {
    generate_spiral(chart_data = data_temp.chart_data)
  } else {
     generate_bar(chart_data = data_temp.chart_data)
  }
  // # Update Text
  generate_text_main(text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}


// ## STAGES

// ## stage_entry
var stage_entry = function() {

  // # Initialize text
  d3v2.select("#text")
    .html("Loading ...");

  // ## call
  stage_0()

}

// ## stage_0
var stage_0 = function(mode="Overview") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text, "LINK"]
  text_duration = [1000,1000]
  text_delay    = [0,0]
  function_new  = stage_1

  // # Execute
  update_vis(mode=mode, text_content=text_content,function_new=function_new,
    text_delay=text_delay, text_duration=text_duration)  

}

// ## stage_1
var stage_1 = function(mode="Overview Subset") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text, "LINK"]
  function_new  = stage_2

  // # Execute
  update_vis(mode=mode, text_content=text_content,function_new=function_new,
    text_delay=text_delay, text_duration=text_duration)
}


// ## stage_2
var stage_2 = function() {


  // # Reset
  var s = svg.selectAll("rect").remove()
  var s = svg.selectAll("#spiral").remove()

  // # Call
  stage_3()

  // # Initialize buttons
  generate_button(width=80, displ_x_origin=230,displ_x_step=100, displ_y_origin=20,displ_y_step=0,
    button_label    = ["All Emails", "Sent Emails", "Received Emails"],
    button_function = [stage_3, stage_4, stage_5],
    button_type = ["button","button","button"], 
    button_move = [16,16,8,0])

}

// ## stage_3
var stage_3 = function(mode="All Emails") {

  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text, "Hover over any bar to see an email that you sent or received on the day in question.<br><i> Throughout the app you can hover over any visualization to get more information.</i>", "LINK"]
  text_duration = [1000,1000,1000]
  text_delay    = [0,4000,4000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, text_content=text_content, function_new=function_new,
    text_delay=text_delay, text_duration=text_duration)

}

// ## stage_4
var stage_4 = function(mode="Sent Emails") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text]
  text_duration = [1000]
  text_delay    = [0]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, text_content=text_content,function_new=function_new,
    text_delay=text_delay, text_duration=text_duration)

}

// ## stage_5
var stage_5 = function(mode="Received Emails") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text]
  text_duration = [1000]
  text_delay    = [0]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, text_content=text_content,function_new=function_new,
    text_delay=text_delay, text_duration=text_duration)

}


// # Launch
// # -------------
stage_entry()

// END
