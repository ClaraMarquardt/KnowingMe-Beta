console.log("firstlast vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color_first     = ["#800f7bd1", "#8080803b"]
var color_last      = ["#070777ab", "#8080803b"]

// KEY
var width      = 700
var height     = 300
var height_svg = 290
var margin     = {top:50,bottom:100,left:50,right:50};
radius         = Math.min(width, height) / 4

var svg = d3v2.select("#chart").append("svg")
            .attr("align","left")
            .attr("width", width)
            .attr("height",height + margin.top)
            .append("g")
            .attr("transform", "translate(" + 0 + "," + (margin.top+10) + ")");

var g = svg

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function(mode) {

    var chart_data_first         = [];
    var chart_data_last        = [];

    for (var i = 0; i < Object.keys($first).length; i++) {
        chart_data_first.push({
          perc:             [$first[i],100-$first[i]],
          perc_alt:         [0,100],
          label:            $firstlast_label[i],
          color:            color_first
 
    });}

    for (var i = 0; i < Object.keys($last).length; i++) {
        chart_data_last.push({
          perc:             [$last[i],100-$last[i]],
          perc_alt:         [0,100],
          label:            $firstlast_label[i],
          color:            color_last
 
    });}

    if (mode=="First") {
        chart_data=chart_data_first
    } else if (mode=="Last") {
         chart_data=chart_data_last
    } 
    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {


  if (mode=="First") {

    if ($mean_first_sent_female>($mean_first_sent_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_first
    } else if ($mean_first_sent_male>($mean_first_sent_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_first
    } else {
      main_text = $text_dict[mode].equal
    }
  }


  if (mode=="Last") {

    if ($mean_last_sent_female>($mean_last_sent_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_last
    } else if ($mean_last_sent_male>($mean_last_sent_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_last
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
var update_vis = function(mode, bar_number, text_content, text_duration, text_delay, function_new, label_main) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  generate_multi_bar(mode, chart_data = data_temp.chart_data, bar_number=bar_number, 
    delay_bar = 2000, duration_bar = 2000, delay_label = 2600, duration_label = 1000,
    label_main=label_main, text_function="", label_size="13px", vis_type="circle",gap_height=100)

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
var stage_0 = function(mode="First") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's look at the probability that you were the person starting a conversation.", 
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = stage_1

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    label_main="Start Conversation")
}

// ## stage_1
var stage_1 = function(mode="Last") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's look at the probability that you were the person ending a conversation.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=1, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    label_main="End Conversation")

}


// # Launch
// # -------------
stage_entry()

// END


