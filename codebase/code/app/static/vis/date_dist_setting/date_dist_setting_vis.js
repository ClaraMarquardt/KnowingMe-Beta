console.log("date_dist vis")


// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// KEY
var width      = 900
var width_svg  = 900
var height     = 300
var height_svg = 300
var margin     = {top:0,bottom:0,left:0,right:0}

var svg = d3v2.select("#chart").append("svg")
             .attr("align","center")
             .attr("width",  width_svg)
             .attr("height", height_svg)
             .append("g")

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function() {

    var chart_data = [];

    for (var i = 0; i < $email_date.length; i++) {
      chart_data.push({
        date: i,
        date_long: new Date($email_date[i]),
        value: $email_count[i],
      });}
    
    return({chart_data:chart_data})

}

// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function() {

  // # Data
  data_temp = update_data()

  // # Update Vis 
  generate_bar_brush(chart_data = data_temp.chart_data)

}


// ## STAGES

// ## stage_entry
var stage_entry = function() {

  // ## call
  update_vis()  

}

// # Launch
// # -------------
stage_entry()

// END
