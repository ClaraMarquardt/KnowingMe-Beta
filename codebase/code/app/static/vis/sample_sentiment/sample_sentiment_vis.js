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
var height       = 350
var height_svg   = 300
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

  // ## call
  stage_0()

}

// ## stage_0
var stage_0 = function(mode="Main") {
  
  // # Define
 text_content = ["This Is The Overall Distribution of Your Sentiment (0=Negative, 1=Positive) Across All Your Emails.<br>Click On Any Bar To See A Sample Email At That Positivity Level."]

  text_duration = [1000]
  text_delay    = [0]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, text_content=text_content,text_duration=text_duration, 
   text_delay=text_delay, function_new=function_new)  

}

// ## stage_0
var stage_1 = function(mode="Supplement") {
  
  // # Define
 text_content = [
    "The Graph On The Right Shows You The % Of Text In The Email That is Negative, Neutral, Positive.<br> Click On 'Update Insight' To See Different Samples."]

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
