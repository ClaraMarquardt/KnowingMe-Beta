console.log("contact_group vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var female_color = "#4d004b"
var male_color   = "#012393"
var na_color     = "#969696"

var color        = [female_color, male_color, na_color]

// KEY

var y_origin      = 70
var y_step        = 60

var x_origin_text = 220
var x_origin      = 260
var x_step        = 60

var height_box    = 50
var width_box     = 50
var text_offset   = 30

var width         = 700
var height        = Object.keys($contact_name).length * (y_step+5) + y_origin
var margin        = {top:0,bottom:0,left:0,right:0};

var svg = d3.select("#chart2").append("svg")
            .attr("align","left")
            .attr("width", width)
            .attr("height",height + margin.top)
            .append("g")
            .attr("transform", "translate(" + 0+ "," + (margin.top+10) + ")");

// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data    = function() {

    var chart_data = [];
    var y          = y_origin  
     
    for (var i = 0; i < Object.keys($contact_name).length; i++) {
        
        chart_data[i] = []
        var x          = x_origin       

        for (var j = 1; j < 4; j++) {
            
            chart_data[i][j-1]=[]
            
            chart_data[i][j-1]={
                y:                 y,
                x:                 x,
                width:             width_box,
                height:            height_box,
                higlight:          j==$contact_gender[i],
                gender_label:      ['Female','Male','Unknown'][j-1], 
                index:             i

            };
        x = x + x_step

        }

        y = y + y_step
        
    }

    var chart_data_text = [];
    var y               = y_origin       
    for (var i = 0; i < Object.keys($contact_name).length; i++) {
        
        chart_data_text[i] = []
        
        for (var j = 0; j < 1; j++) {
            
            chart_data_text[i][j]=[]
            
            chart_data_text[i][j]={
                y:                 y+text_offset,
                x:                 x_origin_text,
                label:             $contact_name[i]
        };}

        y = y + y_step
    }


    return({chart_data:chart_data, chart_data_text:chart_data_text})

}


// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function() {

  // # Data
  data_temp = update_data()

  // # Update Vis 
  generate_grid_vis(chart_data = data_temp.chart_data, chart_data_text = data_temp.chart_data_text)

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

