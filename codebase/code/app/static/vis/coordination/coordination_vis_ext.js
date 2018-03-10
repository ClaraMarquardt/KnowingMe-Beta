console.log("coordination vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color      = [ "#969696", "#08519c", "#08519c", "#08519c"]

// KEY
var width      = 600
var height     = 200
var height_svg = 190
var margin     = {top:50,bottom:0,left:50,right:50};

var svg = d3.select('#chart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + 0 + ')');

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function() {

    var chart_data       = [];

    for (var i = 0; i < Object.keys($coordination).length; i++) {
        chart_data.push({
          value:     $coordination[i],
          label:     $coordination_label[i],
          label_alt: $coordination_label_alt[i],
          color:     color[i], 
          mode:      "Linguistic Coordination"
    });}


    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {
    
    if ($mean_coordination_female>($mean_coordination_male+$comparison_cutoff)) {
      main_text = $text_dict[mode].female_coordinate
    } else if ($mean_coordination_male>($mean_coordination_female+$comparison_cutoff)) {
      main_text = $text_dict[mode].male_coordinate
    } else {
      main_text = $text_dict[mode].equal
    }

  return({main_text:main_text})

} 


// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode, bar_number, text_content, text_duration, text_delay, function_new) {

  // # Data
  data_temp = update_data()

  // # Update Vis 
  generate_vertical_bar(chart_data = data_temp.chart_data, bar_number=bar_number, 
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
  text_content  = ["Let's look at your overall coordination.", text_temp.main_text]
  text_delay    = [0, 2000]
  text_duration = [1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)
}


// # Launch
// # -------------
stage_entry()

// END
