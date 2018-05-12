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
      main_text = "You sent the most emails to "+ $most_contact_sent.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +". You received the most emails from "+ $most_contact_received.replace(/( |^)\w/g, function(l){ return l.toUpperCase() }) +"."
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
var update_vis = function(mode, text_content,most_send,text_duration=[1000],text_delay=[0], function_new="", delay_1=2000, delay_2=5000) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  generate_chord(chart_data = data_temp.chart_data, chart_data_general = data_temp.chart_data_general, 
    most_send=most_send, delay_1=delay_1, delay_2=delay_2)

  // # Update Text
  generate_text_main(text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new)

}


// ## stage function
var update_stage = function(mode,most_send) {

  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = [text_temp.main_text]

  // # Execute
  update_vis(mode=mode, 
    text_content=text_content,most_send=most_send)

}

// # STAGES

// ## stage_entry
var stage_entry = function() {

  // # Initialize text
  d3v2.select("#text")
    .html("Loading ...");

  // # Initialize buttons
  info_text = "* Gender undetermined: "+Math.round($perc_na) + "% of contacts."
 
  generate_button(width=90, displ_x_origin=180,displ_x_step=0, displ_y_origin=90,displ_y_step=30,
    button_label    = ["All Contacts", "Female Contacts", "Male Contacts", info_text],
    button_function = [stage_0, stage_1, stage_2, ""],
    button_type = ["button","button","button","text" ], 
    button_move = [15,15,15,0])

  // # Call
  stage_0()
}

// ## stage_0
var stage_0 = function(mode="All") {

  text_temp = update_text(mode=mode)
  
  // # Define text
  text_content  = ["You corresponded predominantly with "+ $total_contact +" contacts.<br></i>" + Math.round($perc_female) + "% of these contacts are female.</i>",
    text_temp.main_text]
  text_delay    = [0, 3500]
  text_duration = [1000,1000]
  function_new  = ""

  delay_1       = 3500
  delay_2       = 6000
  
  // # Call
  update_vis(mode=mode,text_content=text_content,most_send=$most_contact_sent, text_duration=text_duration,text_delay=text_delay, function_new=function_new, delay_1=delay_1, delay_2=delay_2)

}

// ## stage_1
var stage_1 = function(mode="Female") {

  // # Call
  update_stage(mode=mode,most_send=$most_contact_sent_female) 

}

// ## stage_2
var stage_2 = function(mode="Male") {
 
  // # Call
  update_stage(mode=mode,most_send=$most_contact_sent_male) 

}


// # Launch
// # -------------
stage_entry()

// END

