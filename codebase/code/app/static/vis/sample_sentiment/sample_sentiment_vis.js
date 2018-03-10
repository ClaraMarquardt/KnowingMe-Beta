console.log("sample_sentiment vis")


// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color       = d3.scaleOrdinal(d3.schemeCategory10);
var fill_color  = ["#02091e", "#002fbc"]

// KEY
var width        = 250
var width_svg    = 250
var width_2      = 200
var width_svg_2  = 200
var height       = 320
var height_svg   = 270
var margin     = {top:50,bottom:100,left:50,right:50};

var svg  = d3.select("#a").append("svg")
             .attr("width", width)
             .attr("height",height)
             .append("g")
var g    = svg

var svg2 = d3.select("#b").append("svg")
             .attr("width", width_svg_2)
             .attr("height",height)
             .append("g")
var g2   = svg2



// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode,text_content,text_duration,text_delay,function_new) {

  if (mode=="Main") {
    
    // # Update Vis 
    generate_histogram(mode=mode)
  }

  // # Update Text
  generate_text_main(text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}


// ## STAGES

// ## stage_entry
var stage_entry = function() {

  // # Initialize text
  d3.select("#text")
    .html("Loading...");

  d3.selectAll(".button").remove().exit()
 
  // # Initialize buttons 
  generate_button(width=95, displ_x_origin=87,displ_x_step=0, displ_y_origin=310,displ_y_step=30,
    button_label    = ["Other Examples"],
    button_function = [update_text_sample],
    button_type     = ["button"], 
    button_move     = [8],
    fontsize        ="10px")

  // ## call
  stage_0()

}

// ## stage_0
var stage_0 = function(mode="Main") {
  
  // # Define
 text_content = ["This is the overall distribution of your positiveness (0=Negative, 1=Positive) across all the emails we analyzed.<br>Click on any bar to see a sample email at that positivity level."]

  text_duration = [1000]
  text_delay    = [0]
  function_new  = ""

  $("#c").append("<img id='arrow' src='static/image/icon/arrow_freeform.png' style='width:245px;height:245px'/>");


  // # Execute
  update_vis(mode=mode, text_content=text_content,text_duration=text_duration, 
   text_delay=text_delay, function_new=function_new)  

}

// ## stage_0
var stage_1 = function(mode="Supplement") {
  
  $("#arrow").remove()

  // # Define
 text_content = [
    "The graph on the right shows you the % of text in the email that is negative, neutral, positive.<br> Click on 'Other Examples' to see other examples."]

  text_duration = [1000]
  text_delay    = [0]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, text_content=text_content,text_duration=text_duration, 
   text_delay=text_delay, function_new=function_new)  

}

// # Launch
// # -------------
stage_entry()

// END
