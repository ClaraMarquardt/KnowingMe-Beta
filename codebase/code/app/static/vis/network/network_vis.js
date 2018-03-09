console.log("network vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var female_color = "#4d004b"
var male_color   = "#012393"
var na_color     = "#969696"
   
// KEY
var width       = 800
var height      = 400
var outerRadius = Math.min(width, height)*0.35
var innerRadius = outerRadius - 5;

var g = d3v2.select("#chart_small").append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("id", "circle")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    
    g.append("circle")
     .attr("r", outerRadius);

var arc = d3v2.svg.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);

var path = d3v2.svg.chord()
             .radius(innerRadius);

// TEMP
var last_layout; 


// # Generate the graph data
// # ------------------------------
// # ------------------------------
var update_data  = function(mode) {

  var chart_data_general = []
  var chart_data_all     = [];
  var chart_data_male    = [];
  var chart_data_female  = [];

  // ## Matrx Data
  for(var i=0; i<Object.keys($contact_email).length; i++) {
    chart_data_all[i] = [];
    for(var j=0; j<Object.keys($contact_email).length; j++) {
        chart_data_all[i][j] = $network_matrix[(i*Object.keys($contact_email).length)+j];
    }
  }

  for(var i=0; i<Object.keys($contact_email).length; i++) {
    chart_data_male[i] = [];
    for(var j=0; j<Object.keys($contact_email).length; j++) {
        chart_data_male[i][j] =  $network_matrix_male[(i*Object.keys($contact_email).length)+j];
    }
  }

  for(var i=0; i<Object.keys($contact_email).length; i++) {
    chart_data_female[i] = [];
    for(var j=0; j<Object.keys($contact_email).length; j++) {
        chart_data_female[i][j] = $network_matrix_female[(i*Object.keys($contact_email).length)+j];
    }
  }
  
  // ## General Data
  for(var i=0; i<Object.keys($contact_email).length; i++) {
        chart_data_general.push({
          value_1:          $contact_sent[i],
          value_2:          $contact_received[i],
          label:            $contact_name[i],
          label_detail:     $contact_email[i],
          group:            $contact_gender[i]
  })}


  if (mode=="All") {
        chart_data=chart_data_all
  } else if (mode=="Male") {
         chart_data=chart_data_male
  } else if (mode=="Female") {
        chart_data=chart_data_female
  } 

  return({chart_data:chart_data, chart_data_general:chart_data_general})

}


// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {

  if (mode=="All") {
      main_text = "You sent the most emails to "+ $most_contact_sent.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +". You received the most emails from "+ $most_contact_received.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +".<br><i>(Out of the "+ $total_contact +" contacts that you corresponded with and whose gender we identified "+ Math.round($perc_female) +"% are female)</i>"
  } else if (mode=="Male") {
      main_text = "You sent the most emails to "+ $most_contact_sent_male.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +". You received the most emails from "+ $most_contact_received_male.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +"."
  } else if (mode=="Female") {
      main_text = "You sent the most emails to "+ $most_contact_sent_female.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +". You received the most emails from "+ $most_contact_received_female.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +"."
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
  generate_chord(chart_data = data_temp.chart_data, chart_data_general = data_temp.chart_data_general)

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

// # STAGES

// ## stage_entry
var stage_entry = function() {

  // # Initialize text
  d3v2.select("#text")
    .html("Loading ...");

  // # Initialize buttons
  info_text = "* "+Math.round($perc_na) + "% Of Contacts - Gender Unknown"
 
  generate_button(width=60, displ_x_origin=180,displ_x_step=0, displ_y_origin=100,displ_y_step=30,
    button_label    = ["All Contacts", "Female Contacts", "Male Contacts", info_text],
    button_function = [stage_0, stage_1, stage_2, ""],
    button_type = ["button","button","button","text" ])

  // # Call
  stage_0()
}

// ## stage_0
var stage_0 = function(mode="All") {

  // # Call
  update_stage(mode=mode) 

}

// ## stage_1
var stage_1 = function(mode="Female") {

  // # Call
  update_stage(mode=mode) 

}

// ## stage_2
var stage_2 = function(mode="Male") {
 
  // # Call
  update_stage(mode=mode) 

}


// # Launch
// # -------------
stage_entry()

// END

