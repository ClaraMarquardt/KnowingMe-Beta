console.log("politeness vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color              = ["#969696", "#08519c", "#08519c", "#08519c"]
var color_imbalance    = ["#969696", "#810f7c", "#810f7c", "#810f7c"]

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

    var chart_data_all       = [];
    var chart_data_sent      = [];
    var chart_data_received  = [];
    var chart_data_imbalance  = [];


    for (var i = 0; i < Object.keys($politeness).length; i++) {
        chart_data_all.push({
          value:                 $politeness[i],
          value_default:         1.1,
          value_default_min:     d3.min($politeness),
          label:                 $politeness_label[i],
          label_alt:             $politeness_label_alt[i],
          color:                 color[i], 
          mode:                  "Politeness (All Emails)"
    });}


    for (var i = 0; i < Object.keys($politeness).length; i++) {
        chart_data_sent.push({
          value:                 $politeness_sent[i],
          value_default:         1.1,
          value_default_min:     d3.min($politeness),
          label:                 $politeness_label[i],
          label_alt:             $politeness_label_alt[i],
          color:                 color[i], 
          mode:                  "Politeness (Sent Emails)"
    });} 

    for (var i = 0; i < Object.keys($politeness).length; i++) {
        chart_data_received.push({
          value:                 $politeness_received[i],
          value_default:         1.1,
          value_default_min:     d3.min($politeness),
          label:                 $politeness_label[i],
          label_alt:             $politeness_label_alt[i],
          color:                 color[i], 
          mode:                  "Politeness (Received Emails)"
    });} 

    for (var i = 0; i < Object.keys($politeness).length; i++) {
        chart_data_imbalance.push({
          value:                 $politeness_imbalance[i],
          value_default:         $politeness_imbalance[i],
          value_default_min:     d3.min($politeness_imbalance),
          label:                 $imbalance_label[i],
          label_alt:             $imbalance_label_alt[i],
          color:                 color_imbalance[i], 
          mode:                  "Politeness Imbalance"
    });} 
             
    if (mode=="All Emails") {
        chart_data=chart_data_all
    } else if (mode=="Sent Emails") {
         chart_data=chart_data_sent
    } else if (mode=="Received Emails") {
        chart_data=chart_data_received
    } else if (mode=="Politeness Imbalance") {
        chart_data=chart_data_imbalance
    }

    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {

  // # All Emails
  if (mode=="All Emails") {

    if ($mean_politeness_female>($mean_politeness_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_polite
    } else if ($mean_politeness_male>($mean_politeness_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_polite
    } else {
      main_text = $text_dict[mode].equal
    }
  } 

  // # Sent Emails
  if (mode=="Sent Emails") {

   if ($mean_politeness_sent_female>($mean_politeness_sent_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_polite
    } else if ($mean_politeness_sent_male>($mean_politeness_sent_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_polite
    } else {
      main_text = $text_dict[mode].equal
    }
  } 

  // # Received Emails
  if (mode=="Received Emails") {

    if ($mean_politeness_received_female>($mean_politeness_received_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_polite
    } else if ($mean_politeness_received_male>($mean_politeness_received_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_polite
    } else {
      main_text = $text_dict[mode].equal
    }

  }

  // # Politeness Imbalance
  if (mode=="Politeness Imbalance") {

    main_text_1 = ""
    main_text_2 = ""

    if ($mean_politeness_imbalance_female>1+$comparison_cutoff) {
      main_text_1 = $text_dict[mode].female.pos
    } else if ($mean_politeness_imbalance_female<1-$comparison_cutoff) {
      main_text_1 = $text_dict[mode].female.neg
    } else {
      main_text_1 = $text_dict[mode].female.equal
    }

    if ($mean_politeness_imbalance_male>1+$comparison_cutoff) {
      main_text_2 = $text_dict[mode].male.pos
    } else if ($mean_politeness_imbalance_male<1-$comparison_cutoff) {
      main_text_2 = $text_dict[mode].male.neg
    } else {
      main_text_2 = $text_dict[mode].male.equal
    }
    
    main_text = main_text_1 + "<br>" + main_text_2

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
    label_main=mode)

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
var stage_0 = function(mode="All Emails") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's look at your overall politeness.", "Most emails are relatively polite - let's zoom in.", 
    text_temp.main_text, "LINK"]
  text_delay    = [0, 2000, 3500, 3500]
  text_duration = [1000,1000,1000,1000]
  function_new  = stage_1

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)
}

// ## stage_1
var stage_1 = function(mode="Sent Emails") {

  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content =["Let's look at the politeness of your sent emails.",  
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
var stage_2 = function(mode="Received Emails") {
 
  // # Generate text
  text_temp = update_text(mode=mode)
 
  // # Define
  text_content =["Let's look at the politeness of your received emails.",  
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
var stage_3 = function(mode="Politeness Imbalance") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's look at the politeness imbalance of your emails.",  
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
