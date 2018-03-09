console.log("responsiveness vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

// COLOR, ETC
var color_imbalance    = ["#969696", "#810f7c", "#810f7c", "#810f7c"]

// KEY
var width      = 700
var height     = 300
var height_svg = 290
var margin     = {top:50,bottom:100,left:50,right:50};

var svg = d3.select("#chart").append("svg")
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

    var chart_data_character_count_sent         = [];
    var chart_data_character_imbalance          = [];

    var chart_data_word_count_sent              = [];
    var chart_data_word_imbalance               = [];

    var chart_data_sentence_count_sent          = [];
    var chart_data_sentence_imbalance           = [];

    for (var i = 0; i < Object.keys($character_count_sent).length; i++) {
        chart_data_character_count_sent.push({
          count:            $character_count_sent[i]   ,
          label:            $count_label[i],
          label_alt:        $count_label_alt[i]
 
    });}

    for (var i = 0; i < Object.keys($character_imbalance).length; i++) {
        chart_data_character_imbalance.push({
          value:                 $character_imbalance[i],
          value_default_min:     d3.min($character_imbalance),
          value_default:         $character_imbalance[i],
          label:                 $imbalance_label[i],
          label_alt:             $imbalance_label_alt[i],
          color:                 color_imbalance[i]
    });} 

    for (var i = 0; i < Object.keys($word_count_sent).length; i++) {
        chart_data_word_count_sent.push({
          count:            $word_count_sent[i]   ,
          label:            $count_label[i],
          label_alt:        $count_label_alt[i]
 
    });}

    for (var i = 0; i < Object.keys($word_imbalance).length; i++) {
        chart_data_word_imbalance.push({
          value:                 $word_imbalance[i],
          value_default_min:     d3.min($word_imbalance),
          value_default:         $word_imbalance[i],
          label:                 $imbalance_label[i],
          label_alt:             $imbalance_label_alt[i],
          color:                 color_imbalance[i]
    });} 

    for (var i = 0; i < Object.keys($sentence_count_sent).length; i++) {
        chart_data_sentence_count_sent.push({
          count:            $sentence_count_sent[i]   ,
          label:            $count_label[i],
          label_alt:        $count_label_alt[i]
 
    });}

    for (var i = 0; i < Object.keys($sentence_imbalance).length; i++) {
        chart_data_sentence_imbalance.push({
          value:                 $sentence_imbalance[i],
          value_default_min:     d3.min($sentence_imbalance),
          value_default:         $sentence_imbalance[i],
          label:                 $imbalance_label[i],
          label_alt:             $imbalance_label_alt[i],
          color:                 color_imbalance[i]
    });} 
             
    if (mode=="Character Count") {
        chart_data=chart_data_character_count_sent
    } else if (mode=="Character Imbalance") {
         chart_data=chart_data_character_imbalance
    } else if (mode=="Word Count") {
        chart_data=chart_data_word_count_sent
    } else if (mode=="Word Imbalance") {
         chart_data=chart_data_word_imbalance
    } else if (mode=="Sentence Count") {
        chart_data=chart_data_sentence_count_sent
    } else if (mode=="Sentence Imbalance") {
         chart_data=chart_data_sentence_imbalance
    } 

    return({chart_data:chart_data})

}

// # Generate the graph text
// # ------------------------------
// # ------------------------------
var update_text  = function(mode) {

   // # Received Emails
  if (mode=="Character Count") {

    if ($mean_character_count_sent_female>($mean_character_count_sent_male+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].female_talkative
    } else if ($mean_character_count_sent_male>($mean_character_count_sent_female+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].male_talkative
    } else {
      main_text = $text_dict["Count"].equal
    }

  }

  // # Politeness Imbalance
  if (mode=="Character Imbalance") {

    main_text_1 = ""
    main_text_2 = ""

    if ($mean_character_imbalance_female>1+$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.pos
    } else if ($mean_character_imbalance_female<1-$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.neg
    } else {
      main_text_1 = $text_dict['Imbalance'].female.equal
    }

    if ($mean_character_imbalance_male>1+$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.pos
    } else if ($mean_character_imbalance_male<1-$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.neg
    } else {
      main_text_2 = $text_dict['Imbalance'].male.equal
    }
    
    main_text = main_text_1 + "<br>" + main_text_2

  }

  if (mode=="Word Count") {

    if ($mean_word_count_sent_female>($mean_word_count_sent_male+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].female_talkative
    } else if ($mean_word_count_sent_male>($mean_word_count_sent_female+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].male_talkative
    } else {
      main_text = $text_dict["Count"].equal
    }

  }

  // # Politeness Imbalance
  if (mode=="Word Imbalance") {

    main_text_1 = ""
    main_text_2 = ""

    if ($mean_word_imbalance_female>1+$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.pos
    } else if ($mean_word_imbalance_female<1-$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.neg
    } else {
      main_text_1 = $text_dict['Imbalance'].female.equal
    }

    if ($mean_word_imbalance_male>1+$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.pos
    } else if ($mean_word_imbalance_male<1-$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.neg
    } else {
      main_text_2 = $text_dict['Imbalance'].male.equal
    }
    
    main_text = main_text_1 + "<br>" + main_text_2

  }

  if (mode=="Sentence Count") {

    if ($mean_sentence_count_sent_female>($mean_sentence_count_sent_male+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].female_talkative
    } else if ($mean_sentence_count_sent_male>($mean_sentence_count_sent_female+$comparison_cutoff_count)) {
      main_text = $text_dict["Count"].male_talkative
    } else {
      main_text = $text_dict["Count"].equal
    }

  }

  // # Politeness Imbalance
  if (mode=="Sentence Imbalance") {

    main_text_1 = ""
    main_text_2 = ""

    if ($mean_sentence_imbalance_female>1+$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.pos
    } else if ($mean_sentence_imbalance_female<1-$comparison_cutoff_imbalance) {
      main_text_1 = $text_dict['Imbalance'].female.neg
    } else {
      main_text_1 = $text_dict['Imbalance'].female.equal
    }

    if ($mean_sentence_imbalance_male>1+$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.pos
    } else if ($mean_sentence_imbalance_male<1-$comparison_cutoff_imbalance) {
      main_text_2 = $text_dict['Imbalance'].male.neg
    } else {
      main_text_2 = $text_dict['Imbalance'].male.equal
    }
    
    main_text = main_text_1 + "<br>" + main_text_2

  }
  return({main_text:main_text})

} 


// # Create Animation
// # ------------------------------
// # ------------------------------

// ## animation function
var update_vis = function(mode, bar_number, text_content, text_duration, text_delay, function_new, vis_type) {

  // # Data
  data_temp = update_data(mode=mode)

  // # Update Vis 
  generate_multi_bar(mode, chart_data = data_temp.chart_data, bar_number=bar_number, 
    delay_bar = 2000, duration_bar = 2000, delay_label = 2600, duration_label = 1000,
    label_main=mode, text_function="", label_size="13px", vis_type,gap_height=100)

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

  // # Initialize buttons 
  generate_button(width=70, displ_x_origin=170,displ_x_step=150, displ_y_origin=-35,displ_y_step=0,
    button_label    = ["Characters", "Words", "Sentences"],
    button_function = [stage_0, stage_2, stage_4],
    button_type = ["button","button","button"])

}

// ## stage_0
var stage_0 = function(mode="Character Count") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Lenght Of The Emails You Sent In Terms Of Characters.", 
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = stage_1

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "box")
}

// ## stage_1
var stage_1 = function(mode="Character Imbalance") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Length Imbalance Of Your Emails In Terms Of Characters.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=3, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "bar")

}

// ## stage_2
var stage_2 = function(mode="Word Count") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Length Of The Emails You Sent In Terms Of Words.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = stage_3

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "box")
}

// ## stage_3
var stage_3 = function(mode="Word Imbalance") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Length Imbalance Of Your Emails In Terms Of Words.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=3, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "bar")

}

// ## stage_4
var stage_4 = function(mode="Sentence Count") {
  
  // # Call
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Length Of The Emails You Sent In Terms Of Sentences.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = stage_5

  // # Execute
  update_vis(mode=mode, bar_number=0, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "box")
}

// ## stage_5
var stage_5 = function(mode="Sentence Imbalance") {
  
  // # Generate text
  text_temp = update_text(mode=mode)

  // # Define
  text_content  = ["Let's Look At The Length Imbalance Of Your Emails In Terms Of Sentences.",  
    text_temp.main_text, "LINK"]
  text_delay    = [0, 3500, 3500]
  text_duration = [1000,1000,1000]
  function_new  = ""

  // # Execute
  update_vis(mode=mode, bar_number=3, 
    text_content=text_content, text_duration=text_duration, 
    text_delay=text_delay, function_new=function_new,
    vis_type = "bar")

}


// # Launch
// # -------------
stage_entry()

// END


