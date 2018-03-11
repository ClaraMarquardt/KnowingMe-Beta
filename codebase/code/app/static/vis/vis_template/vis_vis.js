// # MULTIPLE BAR CHART
// # ------------------------------
// # ------------------------------
var generate_multi_bar = function(mode, chart_data, bar_number, delay_bar = 2000, duration_bar = 2000, delay_label = 2600, duration_label = 800,label_main="",text_function, label_size="13px", vis_type="bar",gap_height=0) {
    
    var text_function=function(mode,bar_number) {

      // ## Generate text
      text_temp = update_text(mode).main_text
     
      // # Update text      
      generate_text_main(text_content=[text_temp], text_duration=[1000], 
        text_delay=[0], function_new="")
     
      // # Update visualization
      d3.selectAll(".bar_vis").style("opacity", 0.3)
      d3.selectAll(".bar_vis_"+bar_number).style("opacity", 1)

      d3.selectAll(".circle_vis").style("opacity", 0.3)
      d3.selectAll(".circle_vis_"+bar_number).style("opacity", 1)

    }


    // ## BAR VIS
    if(vis_type=="bar") {
    
      // # Prepare Visualization Variables
      // # -------------

      // ## AXIS
      var x               = d3.scaleBand().rangeRound([0, 50]).padding(0.1),
          y               = d3.scaleLinear().rangeRound([height_svg-gap_height, 0])
      
      x.domain(chart_data.map(function(d) { return d.label; }));
      y.domain([0, d3.max(chart_data, function(d) { return d.value_default; })]);


      // # Initialize
      // # -------------
      gap            = d3.max(chart_data, function(d) { return d.value_default; })/2.5
      min_transition = d3.min(chart_data, function(d) { return d.value_default_min; }) - gap
      min_transition = d3.max([0, min_transition])
      min_transition = d3.max(chart_data, function(d) { return d.value_default; })-min_transition
      displ          = [100, 250, 400, 550][bar_number]
      
      // # Create Visualization
      // # -------------
      
      // ## BASIC
      var g = svg.append("g")
      
      d3.selectAll(".bar_vis").style("opacity", 0.3)

      svg.append("text")
       .text(label_main)
       .attr("class", "bar_vis bar_vis_"+bar_number)
       .style("font-family","Lucida Grande")
       .style("fill", "white" )
       .style("stroke", "white" )
       .style("text-anchor", "middle")
       .style("font-size", label_size )
       .attr("x", displ+(2.5*x.bandwidth()))
       .attr("y", function(d) { return -10+gap_height/2; })
       .transition()
       .delay(delay_label)
       .duration(duration_label)
       .style("fill", "black" )
       .style("stroke", "none" )

      bar = g.selectAll(".bar")
             .data(chart_data)
             .enter().append("g")
       
      bar.append("rect")
         .attr("class", "bar_vis bar bar_vis_"+bar_number)
         .attr("x", function(d) { return x(d.label)+displ; })
         .attr("y", function(d) { return y(0)+gap_height; })
         .on("click", function(d){ text_function(mode, bar_number) })
         .style("opacity",1)
         .style("fill", function(d) { return d.color})
         .attr("width", x.bandwidth())
         .transition()
         .duration(1000)
         .attr("y", function(d) { return y(d.value)+gap_height; })
         .attr("height", function(d) { return height_svg-gap_height - y(d.value)+1; })
         .transition()
         .delay(delay_bar-1000)
         .duration(duration_bar)
         .attr("y", function(d) { return y(d.value)+y(min_transition)+gap_height; })
         .attr("height", function(d) { return height_svg-gap_height - y(d.value)+1; })
      
       bar.append("text").text(function(d) {return(d.label_alt)})
          .attr("class", "bar_vis bar bar_vis_"+bar_number)
          .attr("transform",function(d) { return "translate("+(x(d.label)+displ+3)+","+(y(d.value)+5+gap_height)+") rotate(90)"})
          .style("font-family","Lucida Grande")
          .style("fill", "white" )
          .style("stroke", "none" )
          .style("font-size", "8px" )
          .transition()
          .delay(delay_bar)
          .duration(duration_bar)
          .attr("transform",function(d) { return "translate("+(x(d.label)+displ+3)+","+(y((d.value))+5+y(min_transition)+gap_height)+") rotate(90)"})
          .style("fill", "white" )
          .style("stroke", "none" )
          .text(function(d) {return(d.label)})  

        // ## TOOLTIP
        var tooltip = d3.select("#chart")
                        .append('div')
                        .attr('class', 'tooltip');
        
        tooltip.append('div')
               .attr('class', 'date');
        tooltip.append('div')
               .attr('class', 'value');
        
        svg.selectAll(".bar")
          .on('mouseover', function(d) {
        
            tooltip.select('.date').html("<b>" + d.label + "</b>");
            tooltip.select('.value').html(d.mode +": <b>" + d.value.toFixed(3) + "<b>");
            tooltip.style('display', 'block');
            tooltip.style('opacity',2);
        
        })
        .on('mousemove', function(d) {
            
            tooltip.style('top', (d3.event.layerY + 10) + 'px')
                   .style('left', (d3.event.layerX - 25) + 'px');
        
        })
        .on('mouseout', function(d) {
            
          tooltip.style('display', 'none')
                 .style('opacity',0);
        
        });

    // ## BOX VIS
    } else if (vis_type=="box") {

      // # Reset
      // # -------------
      svg.selectAll(".bar_vis").remove().exit()
      svg.selectAll(".box").remove().exit()

      d3.selectAll(".bar_vis").style("opacity", 0.3)

      for (var j = 0; j < chart_data.length; j++) {

        var g = svg.append("g")
  
        bar = g.selectAll(".bar")
               .data(function(d) { 
                 var data = []; 
                 d3.range(d3.min([500, Math.round(chart_data[j].count)])).forEach(function(){
                 data.push({color: "red",count:chart_data[j].count,label:chart_data[j].label, mode:chart_data[j].mode});}); 
                return data;})
               .enter()
               .append("g")
      
          bar.append("rect")
             .attr("class", "box")
             .attr("x", function(d,i) { return (((0+1)/10)-Math.floor(((0+1)/10)))*60+100+j*150; })
             .attr("y", function(d,i) { return 290-5*(Math.ceil(((chart_data[j].count)+1)/10)); })
             .attr("width", "50px")
             .attr("height", "200px")
             .attr("opacity",0)
             .on("click", function(d){ text_function(mode, bar_number) })
             .attr("fill","white")
  
         bar.append("rect")
            .attr("class", "box bar_vis bar_vis_"+bar_number)
            .attr("x", function(d,i) { return (((i+1)/10)-Math.floor(((i+1)/10)))*60+100+j*150; })
            .attr("y", function(d,i) { return 290-5*(Math.ceil((i+1)/10)); })
            .attr("width", "2px")
            .attr("height", "2px")
            .attr("opacity",1)
            .attr("fill","white")
            .transition()
            .delay(function(d,i) { return j*3000+10*i})
            .attr("fill","black")
  
        bar.append("text")
           .text(function(d,i) { return chart_data[j].label})
           .style("font-family","Lucida Grande")
           .style("fill", "white" )
           .style("stroke", "white" )
           .style("text-anchor", "middle")
           .style("font-size", "10px" )
           .attr("transform",function(d) { return "translate("+(90+j*150)+","+(250)+") rotate(270)"})
           .transition()
           .delay(j*3000+10*chart_data[j].count)
           .duration(duration_label)
           .style("fill", "black" )
           .style("stroke", "none" )
      }

      svg.append("text")
          .attr("class", "bar_vis bar bar_vis_"+bar_number)
         .text(label_main)
         .style("font-family","Lucida Grande")
         .style("fill", "white" )
         .style("stroke", "white" )
         .style("text-anchor", "middle")
         .style("font-size", label_size )
         .attr("x", 280)
         .attr("y", function(d) { return 40; })
         .transition()
         .delay(delay_label*3)
         .duration(duration_label)
         .style("fill", "black" )
         .style("stroke", "none" )


        // ## TOOLTIP
        var tooltip = d3.select("#chart")
                        .append('div')
                        .attr('class', 'tooltip');
        
        tooltip.append('div')
               .attr('class', 'date');
        tooltip.append('div')
               .attr('class', 'value');
        
        svg.selectAll(".box")
          .on('mouseover', function(d) {
        
            tooltip.select('.date').html("<b>" + d.label + "</b>");
            tooltip.select('.value').html(d.mode + ": <b>" + d.count.toFixed(3) + "<b>");
            tooltip.style('display', 'block');
            tooltip.style('opacity',2);
        
        })
        .on('mousemove', function(d) {
            
            tooltip.style('top', (d3.event.layerY + 10) + 'px')
                   .style('left', (d3.event.layerX - 25) + 'px');
        
        })
        .on('mouseout', function(d) {
            
          tooltip.style('display', 'none')
                 .style('opacity',0);
        
        });

  } else if (vis_type=="circle") {

  d3.selectAll(".circle_vis").style("opacity", 0.3)

  // ## Helper function
  function arcTween(a) {
    var i = d3v2.interpolate(this._current, a);
    this._current = i(0);
    return function(t) {
    return arc(i(t));
    };
  }

  function change() {
    for (var m = 0; m < 3; m++) {

      var value = this.value;
      path_temp=path_array[m]
      pie.value(function(d) { return d.perc; }); 
      path_temp = path_temp.data(pie);
      path_temp.transition().delay(m*1000).duration(1500).attrTween("d", arcTween); 
    }
  }

  //# Visualization

  var path_array = []

  for (var i = 0; i < chart_data.length; i++) {

    // ## generate data
    chart_data_temp = []

    for (var j = 0; j < Object.keys(chart_data[i].perc).length; j++) {
      chart_data_temp.push({
      perc:            chart_data[i].perc[j],
      perc_alt:        chart_data[i].perc_alt[j]

    });}

    color = chart_data[i].color

    // ## generate pie
    var pie = d3v2.layout.pie()
                  .sort(null)
                  .value(function(d) { return d.perc_alt; });
  
    var arc = d3v2.svg.arc()
                  .innerRadius(radius - 100)
                  .outerRadius(radius - 20);
  
  
    path_array[i] = svg.append("g")
                       .datum(chart_data_temp)
                       .selectAll("path")
                       .data(pie)
                       .enter()
                       .append("path")
                       .attr("transform", "translate(" + (140+200*i) + "," + (50+bar_number*150) + ")")
                       .attr("d", arc)
                       .each(function(d) { this._current = d; }) 
                       .attr("class", "circle_vis circle_vis_vis circle_vis_"+bar_number)
                       .attr("opacity",1)
                       .attr("fill", function(d,i) { return color[i]; })
                       .on("click",function(d){ text_function(mode, bar_number) })
    
    svg.append("text")
       .text(Math.round(chart_data[i].perc[0])+"%")
       .style("font-family","Lucida Grande")
       .style("fill", "black" )
       .style("stroke", "black" )
       .style("text-anchor", "middle")
       .style("font-size", "10px" )
       .attr("class", "circle_vis circle_vis_"+bar_number)
       .style("opacity",0)
       .attr("transform", "translate(" + (140+200*i) + "," + (70+bar_number*150) + ")")
       .transition()
       .delay(1400*i)
       .style("opacity",1)

    svg.append("text")
       .text(chart_data[i].label)
       .style("font-family","Lucida Grande")
       .style("fill", "black" )
       .style("stroke", "black" )
       .style("text-anchor", "middle")
       .style("font-size", "10px" )
       .style("opacity",0)
       .attr("class", "circle_vis circle_vis_"+bar_number)
       .attr("transform", "translate(" + (140+200*i) + "," + (-20+bar_number*150) + ")")
       .transition()
       .delay(1400*i)
       .style("opacity",1)


  
    setTimeout(function () {change();}, 100);                  

  }

  svg.append("text")
     .text(label_main)
     .style("font-family","Lucida Grande")
     .attr("class", "circle_vis circle_vis_"+bar_number)
     .style("fill", "black" )
     .style("stroke", "black" )
     .style("text-anchor", "middle")
     .style("font-size", "10px" )
     .style("opacity",0)
     .attr("transform", "translate(" + (70) + "," + (50+bar_number*150) + ") rotate(270)")
     .transition()
     .delay(1400*i)
     .style("opacity",1)

}

};


// # GRID
// # ------------------------------
// # ------------------------------

var generate_grid_vis = function(chart_data, chart_data_text) {

// boxes
var row = svg.selectAll(".row")
              .data(chart_data)
              .enter().append("svg:g")

var col = row.selectAll(".cell")
             .data(function (d) { return d; })
             .enter().append("svg:rect")
             .attr("class", function(d) { return "rect_"+d.y})
             .attr("x", function(d) { return d.x})
             .attr("y", function(d) { return d.y })
             .attr("width", function(d) { return d.width; })
             .attr("height", function(d) { return d.height; })
             .style("fill", function(d,i) { 
              if (d.higlight==true) {
                return color[i]
              } else {
                return "white"; 
              }})
             .style("stroke", '#555')
             .on('click', function(d,i) {
                d3.selectAll(".rect_"+d.y).style("fill", "white")
                d3.select(this).style("fill", color[i])
                $contact_gender[d.index] = i+1

                d3.select("#contact_email_updated").property("value", $contact_email);
                d3.select("#contact_gender_updated").property("value", $contact_gender);

             })

// text
var row_text = svg.selectAll(".row_text")
                  .data(chart_data_text)
                  .enter().append("svg:g")

var col_text = row_text.selectAll(".cell_text")
                       .data(function (d) { return d; })
                       .enter().append("svg").append("text")
                       .attr("x", function(d) { return d.x})
                       .attr("y", function(d) { return d.y })
                       .text(function(d) {return d.label.replace(/( |^)\w/g, function(l){ return l.toUpperCase() })})
                       .style("text-anchor", "end")

// labels
var row_label = svg.selectAll(".row_label")
                    .data([chart_data[0]])
                    .enter().append("svg:g")

var col_label = row_label.selectAll(".cell_label")
                         .data(function (d) {return d; })
                         .enter().append("svg").append("text")
                         .attr("transform",function(d) { return "translate("+(d.x+20)+","+(d.y-10)+") rotate(300)"})
                         .text(function(d) {return d.gender_label})

}


// # VERTICAL BAR
// # ------------------------------
// # ------------------------------
var generate_vertical_bar = function(chart_data, bar_number, delay_bar = 2000, duration_bar = 2000, delay_label = 2600, duration_label = 800,label_main="") {
    
  
// set the ranges
var y = d3.scaleBand()
    .range([height, 0])
    .padding(0.1);

var x = d3.scaleLinear()
    .range([0, width]);

  x.domain([-1,1]);
  y.domain(chart_data.map(function (d) {
    return d.label;}));

  svg.selectAll(".bar")
      .data(chart_data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function (d) {return x(Math.min(0, 0));})
      .attr("y", function (d) {return y(d.label);})
      .attr("width", 0)
      .attr("height", y.bandwidth())
      .style("fill", function(d) { return d.color})
      .transition()
      .duration(1500)
      .attr("x", function (d) {return x(Math.min(0, d.value));})
      .attr("width", function (d) {return Math.abs(x(d.value) - x(0));})

    let yAxisGroup = svg.append("g")
                        .attr("transform", "translate(" + x(0) + ",0)")
                        .call(d3.axisRight(y));
    
    yAxisGroup.selectAll('.tick')
              .data(chart_data)
              .select('text')
              .attr('x', function(d,i){return d.value<0?9:-9})
              .style('text-anchor', function(d,i){return d.value<0?'start':'end'})
 
  // ## TOOLTIP
  var tooltip = d3.select("#chart")
                  .append('div')
                  .attr('class', 'tooltip');
  
  tooltip.append('div')
         .attr('class', 'date');
  tooltip.append('div')
         .attr('class', 'value');
  
  svg.selectAll("rect")
    .on('mouseover', function(d) {
  
      tooltip.select('.date').html("<b>" + d.label + "</b>");
      tooltip.select('.value').html(d.mode + ": <b>" + d.value.toFixed(3) + "<b>");
      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
             .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
      
    tooltip.style('display', 'none')
           .style('opacity',0);
  
  });

  };

// # HISTOGRAM
// # ------------------------------
// # ------------------------------
var generate_histogram = function(mode) {

    d3.selectAll(".vis").attr("opacity",1)
    
    
    // # Initialize visualization functions
    // # -------------
    var x = d3.scaleLinear()
        .rangeRound([0, width_svg]);
    
    var bins = d3.histogram()
        .domain([0,1])
        .thresholds(x.ticks(10))
        ($sentiment_score);
    
    var y = d3.scaleLinear()
              .domain([0, d3.max(bins, function(d) { return d.length; })])
              .range([height_svg, 0]);
  
    var bar = g.selectAll(".bar")
                .data(bins)
                .enter().append("g")
                .attr("class", "bar")
                .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; });

    
      // # Create visualization
      // # -------------
     
      bar.append("rect")
         .attr("x", 1)
         .attr("class","vis")
         .attr("width", x(bins[0].x1) - x(bins[0].x0) - 1)
         .attr("height", function(d) { return height_svg - y(d.length); })
         .attr("fill","darkblue")
         .on("click", function(d){
          
          d3.selectAll(".vis").attr("opacity",0.1)
          d3.select(this).attr("opacity",1)
          stage_1()

         // # clear/update text
        d3.select("#c").selectAll(".text_sample").remove().exit()
        d3.select("#c").append("text").attr("class", "text_sample").text($sentiment_score_sample[Math.ceil(d.x0*10)]).style("font-style","italic").style("color", "darkblue")
        
        // # clear/update dist
        d3.selectAll(".dist_sample").remove().exit()
        dist_sample_data_label = ["% Neg", "% Neu", "% Pos"]
        dist_sample_data = $sentiment_score_sample_dist[Math.ceil(d.x0*10)]
        dist_sample_data = dist_sample_data.split("/") 
        dist_sample_data = dist_sample_data.map(function(d) { return +d; })
  
        dist_sample_data_all =[]
           for (var i = 0; i < 3; i++) {
              dist_sample_data_all.push({
                value:     dist_sample_data[i],
                label:     dist_sample_data_label[i]
        });}
  
        var x_bar = d3.scaleBand().rangeRound([0, width_svg_2]).padding(0.1)
        var y_bar = d3.scaleLinear().rangeRound([height_svg, 0])
  
        x_bar.domain(dist_sample_data_all.map(function(d) { return d.label; }));
        y_bar.domain([0, d3.max(dist_sample_data_all, function(d) { return d.value; })]);
  
        g2.selectAll(".hh")
          .data(dist_sample_data_all)
          .enter().append("rect")
          .attr("class", "dist_sample dist_sample_rect")
          .attr("x", function(d,i) { return x_bar(d.label); })
          .attr("y", function(d,i) {  return y_bar(d.value); })
          .attr("width", x_bar.bandwidth())
          .attr("height", function(d) { return height_svg - y_bar(d.value)+1; })
      
 
        g2.append("g")
          .attr("class", "dist_sample")
          .attr("transform", "translate(0," + (height_svg) + ")")
          .call(d3.axisBottom(x_bar));

  var tooltip = d3.select("#a")
                      .append('div')
                      .attr('class', 'tooltip');
      
      tooltip.append('div')
             .attr('class', 'weekday')
      tooltip.append('div')
            .attr('class', 'hour')
      tooltip.append('div')
          .attr('class', 'value')

      d3.selectAll(".dist_sample_rect")
         .on('mouseover', function(d) {

          d3.select(this)
            .style("fill","white")
            .style("stroke","black")
            .style("stroke-width","1px");

          tooltip.select('.weekday').html("<b>"+d.label+":</b>");
          tooltip.select('.hour').html((d.value*100).toFixed(3));
          tooltip.style('display', 'block');
          tooltip.style('opacity',2);
      
      })
      .on('mousemove', function(d) {
          
          tooltip.style('top', (d3.event.layerY + 200) + 'px')
                 .style('left', (d3.event.layerX + 550) + 'px');
      
      })
      .on('mouseout', function(d) {
        
        d3.select(this)
          .style("fill","black" )
          .style("stroke","black")
          .style("stroke-width","1px");
      
        tooltip.style('display', 'none')
               .style('opacity',0);
      
      });

        })  
  
       g.append("g")
        .attr("transform", "translate(0," + height_svg + ")")
        .call(d3.axisBottom(x));
  
  }

// # HEATMAP
// # ------------------------------
// # ------------------------------
var generate_heatmap = function(chart_data) {

  // # Reset
  // # -------------
  svg.selectAll(".hour").remove().exit()

  // # Initialize visualization functions
  // # -------------
    var colorScale = d3.scaleQuantile()
                       .domain([0, buckets-1, d3.max(chart_data, function (d) { 
                        return d.value_default_max; 
                        })])
                       .range(colors);

  // # Create Visualization
  // # -------------
  
  // ## BASIC
  var dayLabels = svg.selectAll(".dayLabel")
                     .data(days)
                     .enter().append("text")
                     .text(function(d) { return d })
                     .attr("x", 0)
                     .attr("y", function (d, i) { return i * gridSize; })
                     .style("text-anchor", "end")
                     .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
                     .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono_week axis axis-workweek" : "dayLabel mono_week axis"); })

  var timeLabels = svg.selectAll(".timeLabel")
                      .data(times)
                      .enter().append("text")
                      .text(function(d) { return d; })
                      .attr("x", function(d, i) { return i * gridSize; })
                      .attr("y", 0)
                      .style("text-anchor", "middle")
                      .attr("transform", "translate(" + gridSize / 2 + ", -6)")
                      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); })
                      .attr("fill", function (d, i) { return hour_color(i)})

 var daypartLabels = svg.selectAll(".jjj")
                      .data(daytime)
                      .enter().append("text")
                      .attr("font-family", "FontAwesome")
                      .text(function(d) { return d; })
                      .attr("x", function(d, i) { return i * gridSize; })
                      .attr("y", 0)
                      .style("text-anchor", "right")
                      .attr("transform", "translate(" + gridSize / 2 + ", 220)")

  var cards = svg.selectAll(".hour")
                 .data(chart_data, function(d) {return d.day+':'+d.hour;});


  cards.enter().append("rect")
       .attr("x", function(d) { return (d.hour) * gridSize; })
       .attr("y", function(d) { return (d.day) * gridSize; })
       .attr("rx", 4)
       .attr("ry", 4)
       .attr("class", "hour bordered")
       .attr("width", gridSize)
       .attr("height", gridSize)
       .style("fill", "#FFFFFF")
       .transition().duration(2000)
       .style("fill", function(d) { return colorScale(d.value); });

  // ## Legend
  var legend = svg.selectAll(".legend")
                  .data([0].concat(colorScale.quantiles()), (d) => d);

  var legend_g = legend.enter().append("g")
                       .attr("class", "legend");

  legend_g.append("rect")
          .attr("x", (d, i) => (legendElementWidth * i)+150)
          .attr("y", height_svg+40)
          .attr("width", legendElementWidth)
          .attr("height", gridSize / 2)
          .style("fill", (d, i) => colors[i]);

  legend_g.append("text")
          .attr("class", "mono")
          .text((d) => "≥ " + Math.round(d))
          .attr("x", (d, i) => (legendElementWidth * i)+150)
          .attr("y", height_svg+70);

  // ## TOOLTIP
  var tooltip = d3.select("#chart")
  .append('div')
  .attr('class', 'tooltip');
  
  tooltip.append('div')
         .attr('class', 'weekday')
  tooltip.append('div')
        .attr('class', 'hour')
  tooltip.append('div')
      .attr('class', 'value')

  svg.selectAll(".hour")
     .on('mouseover', function(d) {
  
      d3.select(this)
        .style("fill","#000000")
        .style("stroke","#000000")
        .style("stroke-width","1px");

      tooltip.select('.weekday').html("Weekday: <b>" + days_long[d.day] + "</b>");
      tooltip.select('.hour').html("Time: <b>" + times_long[d.hour] + "</b>");
      tooltip.select('.value').html("Emails: <b>" + Math.round(d.value*100)/100 + "<b>");
      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
             .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
    
    d3.select(this)
      .style("fill",function(d){return colorScale(d.value); })
      .style("stroke","#FFFFFF")
      .style("stroke-width","3px");
  
    tooltip.style('display', 'none')
           .style('opacity',0);
  
  });

}

// # BAR BRUSH
// # ------------------------------
// # ------------------------------
var generate_bar_brush = function(chart_data) {


  // # Helper functions
  // # -------------
  var sum_value = function(chart_data,start,end) {

    temp =  d3.sum(chart_data, function(d) {if (d.date>=end & d.date<=start) {

            return(d.value)
            
          } else {
            
            return(0)

    }})

    return(temp)
  }

  function brushinit(original_start_id, original_end_id) {
      // ## constraints
      localBrush_email   = sum_value(chart_data,original_start_id,original_end_id)
      localBrush_daylag  = original_end_id + 1
      localBrush_daydiff =  original_start_id - original_end_id

      if ((original_start_id!= $start_date_id_original| original_end_id!=$end_date_id_original) & (localBrush_email > $max_email | localBrush_email< $min_email | localBrush_daylag < $timelag_min| localBrush_daydiff < $min_day |  localBrush_daydiff < 0)) {
        alert("You need to select a timeframe which spands at least "+$min_day+" days and does not begin within the past "+$timelag_min+" days. The timeframe you select needs to contain between "+$min_email+" and " + $max_email + " emails.")
        
        brushinit(original_start_id=$start_date_id_original, original_end_id=$end_date_id_original)
      } else {

          d3v2.selectAll(".bar").style("opacity", 1)
          brush.extent([original_start_id, original_end_id]);
          svg.select(".brush").call(brush);
        
          d3.select("#text").text("The selected timeframe contains " + localBrush_email + " emails.");
          d3.select("#end_date").property("value", $email_date[original_end_id]);
          d3.select("#start_date").property("value", $email_date[original_start_id]);

      }


  }

  function update_user_start () {

      var new_date_start = $('#start_date').val()
      if ($email_date.indexOf(new_date_start)!=-1) {
         var new_date_start_id = $email_date.indexOf(new_date_start)
          b = brush.extent();
        localBrush_end_date = (brush.empty()) ? brush_end_date : Math.ceil(b[1]),

         brushinit(original_end_id=new_date_start_id, original_start_id= localBrush_end_date)
      } else {
         alert("Please enter a valid date ('mm/dd/yyyy') within the past year ("+$email_date[$start_date_id_original]+" - "+$email_date[$end_date_id_original]+").")
         brushinit(original_start_id=$start_date_id_original, original_end_id=$end_date_id_original)

      }
  }

  function update_user_end () {

      var new_date_end = $('#end_date').val()
      if ($email_date.indexOf(new_date_end)!=-1) {
         var new_date_end_id = $email_date.indexOf(new_date_end)
         b = brush.extent();
         localBrush_end_date = (brush.empty()) ? brush_end_date : Math.ceil(b[0]),
         brushinit(original_end_id=localBrush_end_date,original_start_id= new_date_end_id)
      } else {
         alert("Please enter a valid date ('mm/dd/yyyy') within the past year ("+$email_date[$start_date_id_original]+" - "+$email_date[$end_date_id_original]+").")
         brushinit(original_end_id=$start_date_id_original, original_start_id=$end_date_id_original)

      }
  }


  function brushmove() {
     
      b = brush.extent();
  
      localBrush_end_date = (brush.empty()) ? brush_end_date : Math.ceil(b[0]),
      localBrush_start_date   = (brush.empty()) ? brush_start_date : Math.ceil(b[1]);

      d3v2.select("g.brush").call((brush.empty()) ? brush.clear() : brush.extent([localBrush_end_date, localBrush_start_date]));
  
      d3v2.selectAll(".bar").style("opacity", function(d, i) {
        return d.date >= localBrush_end_date && d.date < localBrush_start_date || brush.empty() ? "1" : ".4";
      });

      // ## update the text fields
      d3.select("#text").text("The selected timeframe contains " + localBrush_email + " emails.");
      d3.select("#end_date").property("value", $email_date[localBrush_end_date]);
      d3.select("#start_date").property("value", $email_date[localBrush_start_date]);

  }
  
  function brushend() {
  
    var localBrush_end_date = (brush.empty()) ? brush_end_date : Math.ceil(b[0]),
        localBrush_start_date = (brush.empty()) ? brush_start_date : Math.floor(b[1]);
  
      d3v2.selectAll(".bar").style("opacity", function(d, i) {
        return d.date >= localBrush_end_date && d.date <= localBrush_start_date || brush.empty() ? "1" : ".4";
      });

       // ## constraints
      localBrush_email   = sum_value(chart_data,localBrush_start_date,localBrush_end_date)
      localBrush_daylag  = localBrush_end_date + 1
      localBrush_daydiff =   localBrush_start_date - localBrush_end_date
        
      if ((localBrush_start_date!= $start_date_id_original| localBrush_end_date!=$end_date_id_original) & (localBrush_email > $max_email | localBrush_email< $min_email | localBrush_daylag < $timelag_min| localBrush_daydiff < $min_day |  localBrush_daydiff < 0)) {

        alert("You need to select a timeframe which spands at least "+$min_day+" days and does not begin within the past "+$timelag_min+" days. The timeframe you select needs to contain between "+$min_email+" and " + $max_email + " emails.")
        
        brushinit(original_start_id=$start_date_id_original, original_end_id=$end_date_id_original)
      } else {

      d3.select("#text").text("The selected timeframe contains " + localBrush_email + " emails.");
      d3.select("#end_date").property("value", $email_date[localBrush_end_date]);
      d3.select("#start_date").property("value", $email_date[localBrush_start_date]);
    }
  }
  
  
 
  // # Prepare Visualization variables
  // # -------------
  var x = d3.scaleLinear().rangeRound([0, width_svg])
  var y = d3.scaleLinear().rangeRound([height_svg, 0])
  
  brush_start_date = 0;
  brush_end_date   = 10;

  var barchart = svg

  // # Create Visualization
  // # -------------

  // ## BASIC
  x.domain([d3.max(chart_data, function(d) { return d.date;}),0]);
  y.domain([0, d3.max(chart_data, function(d) { return d.value;})]);

  barchart.append("g")

  barchart.selectAll(".bar")
          .data(chart_data)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.date); })
          .attr("y", function(d) {  return y(d.value); })
          .attr("width", 0.8)
          .attr("height", function(d) { return height_svg - y(d.value)+1; })

  // ## BRUSH
  brush = d3v2.svg.brush()
              .x(x)
              .on("brush", brushmove)
              .on("brushend", brushend);

  var arc = d3v2.svg.arc()
                .outerRadius(height / 80)
                .startAngle(0)
                .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });

  brushg = barchart.append("g")
                   .attr("class", "brush")
                   .call(brush);

  brushg.selectAll(".resize").append("path")
        .attr("transform", "translate(0," +  height / 2 + ")")
        .attr("d", arc);

  brushg.selectAll("rect")
        .attr("height", height);

  d3.select("#Reset").on('click', function(d) {brushinit(original_start_id=$start_date_id_original, original_end_id=$end_date_id_original);})

  $('#start_date').on('change', function () {update_user_start()} )
  $('#end_date').on('change', function () {update_user_end()})

  // # initialize the brush
  brushinit(original_end_id=$start_date_id_original, original_start_id=$end_date_id_original)


};

// # BAR
// # ------------------------------
// # ------------------------------
var generate_bar = function(chart_data) {

  svg.selectAll(".bar").remove().exit()

  // # Prepare Visualization variables
  // # -------------
  var x = d3.scaleBand().rangeRound([0, width_svg]).padding(0.1)
  var y = d3.scaleLinear().rangeRound([height_svg, 0])

  // # Create Visualization
  // # -------------
 
  // ## BASIC
  x.domain(chart_data.map(function(d) { return d.date; }));
  y.domain([0, d3.max(chart_data, function(d) { return d.value_default; })]);

  g.append("g")
   .attr("class", "axis axis--x")
   .attr("transform", "translate(0," + height_svg + ")")
   .call(d3.axisBottom(x));

  g.selectAll(".bar")
   .data(chart_data)
   .enter().append("rect")
   .attr("class", "bar")
   .attr("x", function(d) { return x(d.date); })
   .attr("y", function(d) {  return height_svg; })
   .attr("width", x.bandwidth()/2)
   .attr("height", function(d) { return 0 })
   .transition()
   .duration(1000)
   .attr("y", function(d) {  return y(d.value); })
   .attr("height", function(d) { return height_svg - y(d.value)+1; })

  // ## TOOLTIP
  var tooltip = d3.select("#chart")
                  .append('div')
                  .attr('class', 'tooltip');
  
  tooltip.append('div')
         .attr('class', 'date');
  tooltip.append('div')
         .attr('class', 'value');
  tooltip.append('div')
         .attr('class', 'sample');


  svg.selectAll(".bar")
     .on('mouseover', function(d) {
  
      tooltip.select('.date').html("<b>" + d.date.toDateString() + "</b>");
      tooltip.select('.value').html("Emails: <b>" + d.value+ "<b>");
      tooltip.select('.sample').html("Sample Email <br><i>" + d.sample+ "<br>" + d.sample_detail +"</i></b>");

      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
             .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
      
    tooltip.style('display', 'none')
           .style('opacity',0);
  
  });


};

// # SPIRAL
// # ------------------------------
// # ------------------------------
var generate_spiral = function(chart_data) {

  // # Prepare Visualization variables
  // # -------------
  var r      = d3.min([width, height]) / 2 - 20;
  var radius = d3.scaleLinear()
                 .domain([start, end])
                 .range([40, r]);
 
  
  // # Initialize visualization functions
  // # -------------
  
  var theta = function(r) {
    return numSpirals * Math.PI * r;
  };
  
  // # Create Visualization
  // # -------------  
  var points = d3.range(start, end + 0.001, (end - start) / 1000);
  
  var spiral = d3.radialLine()
    .curve(d3.curveCardinal)
    .angle(theta)
    .radius(radius);
  
  svg.selectAll("rect").remove().exit()
  var g = svg
   g.append("svg")
    .attr("transform", "translate("+width/2+"," + height_svg/2 + ")")
  
  var path = g.append("path")
    .datum(points)
    .attr("id", "spiral")
    .attr("d", spiral)
    .style("fill", "none")
    .attr("transform", "translate("+width/2+"," + height_svg/2 + ")")
    .style("stroke", "steelblue");
  
  var spiralLength = path.node().getTotalLength(),
      N = 365,
      barWidth = (spiralLength / N) - 1;
  
  var timeScale = d3.scaleTime()
    .domain(d3.extent(chart_data, function(d){
      return d.date;
    }))
    .range([0, spiralLength]);
  
  var yScale = d3.scaleLinear()
    .domain([0, d3.max(chart_data, function(d){
      return d.value;
    })])
    .range([0, (r / numSpirals) - 30]);
  
  bar = g.selectAll("rect")
    .data(chart_data)
    .enter()
    .append("rect")
    .attr("x", function(d,i){
      
      var linePer = timeScale(d.date),
          posOnLine = path.node().getPointAtLength(linePer),
          angleOnLine = path.node().getPointAtLength(linePer - barWidth);
    
      d.linePer = linePer; 
      d.x = posOnLine.x; 
      d.y = posOnLine.y; 
      
      d.a = (Math.atan2(angleOnLine.y, angleOnLine.x) * 180 / Math.PI) - 90; 
  
      return d.x;
    })
    .attr("y", function(d){
      return d.y;
    })
    .attr("width", function(d){
      return barWidth;
    })
    .attr("height", function(d){
      return yScale(d.value);
    })
    .attr("fill", function(d) {return fill_color[d.col_group]})
    .attr("transform", function(d){
      return "translate("+width/2+"," + height_svg/2 + ") rotate(" + d.a + "," + d.x  + "," + d.y + ")"; 
    });
    
   // ## DATA LABELS
   var tF = d3.timeFormat("%b %Y"),
      firstInMonth = {};
  
  svg.selectAll("text")
    .data(chart_data)
    .enter()
    .append("text")
    .attr("dy", 10)
    .style("text-anchor", "start")
    .style("font", "10px arial")
    .append("textPath")
    .filter(function(d){
      var sd = tF(d.date);
      if (!firstInMonth[sd]){
        firstInMonth[sd] = 1;
        return true;
      }
      return false;
    })
    .text(function(d){
      date_ = d.date
      currDay   = date_.getDate()-10;
      currMonth = date_.getMonth();
      if (currMonth!=11){
        currMonth = date_.getMonth() + 1;
      } else {
        currMonth = 0
      }
      currYear  = date_.getYear()+1900;
      date__ = new Date(currYear, currMonth, currDay);
      return tF(date__);
    })
    
    .attr("xlink:href", "#spiral")
    .style("fill", "grey")
    .attr("startOffset", function(d){
      return ((d.linePer / spiralLength) * 100) + "%";
    })
  
  // ## TOOLTIP
  var tooltip = d3.select("#chart")
  .append('div')
  .attr('class', 'tooltip');
  
  tooltip.append('div')
  .attr('class', 'date');
  tooltip.append('div')
  .attr('class', 'value');
  
  svg.selectAll("rect")
  .on('mouseover', function(d) {
  
      d3.select(this)
        .style("fill","#FFFFFF")
        .style("stroke","#000000")
        .style("stroke-width","2px");
  
      tooltip.select('.date').html("<b>" + d.date.toDateString() + "</b>");
      tooltip.select('.value').html("Emails: <b>" + Math.round(d.value*100)/100 + "<b>");
      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
      .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
    
    d3.select(this)
      .style("fill",function(d){return fill_color[d.col_group];})
      .style("stroke","none");
  
    tooltip.style('display', 'none');
    tooltip.style('opacity',0);
  
  });

}


// # CHORD
// # ------------------------------
// # ------------------------------
function generate_chord( chart_data, chart_data_general,most_send, delay_1=3500, delay_2=6000) {
    
    // # Initialize
    // # -------------


    // # Define helper functions
    // # -------------

    // ## arcTween
    function arcTween(oldLayout) {
      var oldGroups = {};
      if (oldLayout) {
          oldLayout.groups().forEach( function(groupData) {
              oldGroups[ groupData.index ] = groupData;
          });
      }
    
      return function (d, i) {
        var tween;
        var old = oldGroups[d.index];
        if (old) { 
            tween = d3v2.interpolate(old, d);
        }
        else {
            var emptyArc = {startAngle:d.startAngle,
                            endAngle:d.startAngle};
            tween = d3v2.interpolate(emptyArc, d);
        }
        
        return function (t) {
            return arc( tween(t) );
        };
      };
    }

    // ## chordKey
    function chordKey(data) {
      return (data.source.index < data.target.index) ?
        data.source.index  + "-" + data.target.index:
        data.target.index  + "-" + data.source.index;
    }

    // ## chordTween
    function chordTween(oldLayout) {
    
      var oldChords = {};
      
      if (oldLayout) {
          oldLayout.chords().forEach( function(chordData) {
              oldChords[ chordKey(chordData) ] = chordData;
          });
      }
      
      return function (d, i) {
          
          var tween;
          var old = oldChords[ chordKey(d) ];
          if (old) {
              if (d.source.index != old.source.index ){
                  old = {
                      source: old.target,
                      target: old.source
                  };
              }
              
              tween = d3v2.interpolate(old, d);
          }
          else {
              var emptyChord = {
                  source: { startAngle: d.source.startAngle,
                           endAngle: d.source.startAngle},
                  target: { startAngle: d.target.startAngle,
                           endAngle: d.target.startAngle}
              };
              tween = d3v2.interpolate( emptyChord, d );
          }
  
          return function (t) {
              return path(tween(t));
          };
      };
    }

    // ## getDefaultLayout
    function getDefaultLayout() {
      return d3v2.layout.chord()
               .padding(0.03)
               .sortSubgroups(d3v2.descending)
               .sortChords(d3v2.descending)
               .sortGroups(d3v2.descending);
    } 
    
    // # Prepare Visualization Variables
    // # -------------

    // # Create Visualization
    // # -------------

    // ## BASIC
    layout = getDefaultLayout();
    layout.matrix(chart_data);

    var groupG = g.selectAll("g.group")
                  .data(layout.groups(), function (d) {
                     return d.index; 
                  });
    
    groupG.exit()
          .attr("transform", "rotate(0)")
          .transition()
          .duration(1500)
          .attr("opacity", 0)
          .remove(); 
    
    var newGroups = groupG.enter().append("g")
                          .attr("class", "group");

    newGroups.append("title");
    
    newGroups.append("path")
            .attr("id", function (d) {
              return "group" + d.index;
            })
            .style("fill", function (d) {
                if (d.index!=0) {
                  return group_color(chart_data_general[d.index].group, 
                    female_color=female_color, male_color=male_color,na_color=na_color);
                } else {return "#FFF"}
            })
           .style("stroke", function(d) {
                if (d.index!=0) {
                  return "none";
                } else {return "#000"}
            });
 
    groupG.select("path") 
          .attr("transform", "rotate(0)")
          .transition()
          .duration(1500)
          .attr("opacity", 0.5) 
          .attrTween("d", arcTween( last_layout ))
          .transition().duration(100).attr("opacity", 0.7)
    
    newGroups.append("svg:text")
             .attr("dy", ".35em")
             .attr("color", "#fff")
             .attr("class", "test")
             .text(function (d) {
                if (chart_data[0][d.index]>0 |chart_data[d.index][0]>0){
                  return ($contact_name[d.index]).replace(/( |^)\w/g, function(l){ return l.toUpperCase() });}
                else {
                  return ""
                }
            });
    
    text_temp = d3v2.selectAll(".test")
    text_temp.text("")
    
    d3v2.selectAll(".test")
        .text(function (d) {
            if (chart_data[0][d.index]>0 |chart_data[d.index][0]>0){
              return ($contact_name[d.index]).replace(/( |^)\w/g, function(l){ return l.toUpperCase() });}
            else {
             return ""
           }
        })
        .attr("font-size", "7px")

    groupG.select("text")
        .transition()
        .duration(1500)
        .attr("transform", function(d) {
            d.angle = (d.startAngle + d.endAngle) / 2;                
            return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")" +
              " translate(" + (innerRadius + 10) + ")" + 
              (d.angle > Math.PI ? " rotate(180)" : " rotate(0)"); 
        })
        .attr("text-anchor", function (d) {
            return d.angle > Math.PI ? "end" : "begin";
        });
    
    var chordPaths = g.selectAll("path.chord")
                      .data(layout.chords(), chordKey )
       
    var tooltip = d3v2.select("#chart_small")
                    .append('div')
                    .attr('class', 'tooltip');
  
    tooltip.append('div')
           .attr('class', 'name');
    tooltip.append('div')
           .attr('class', 'email');
    tooltip.append('div')
           .attr('class', 'value_sent');
    tooltip.append('div')
           .attr('class', 'value_received');
        
    var newChords = chordPaths.enter()
                              .append("path")
                              .attr("class", "chord")
                              .on('mouseover', function(d) {
        
                                    target_id       = d3v2.max([d.target.index, d.source.index])

                                    if (target_id!=0) {
                                        
                                        target_name     = chart_data_general[target_id].label
                                        target_email    = chart_data_general[target_id].label_detail
                                        sent_email      = chart_data_general[target_id].value_1
                                        received_email  = chart_data_general[target_id].value_2
                        
                                        tooltip.select('.name').html("<b>" + target_name + "</b>");
                                        tooltip.select('.email').html("<i>(" + target_email + ")</i>");
                                        tooltip.select('.value_sent').html("Emails (Sent): <b>" + sent_email + "<b>");
                                        tooltip.select('.value_received').html("Emails (Received): <b>" + received_email + "<b>");
                        
                                        tooltip.style('display', 'block')
                                               .style('opacity',2);
                        
                                    } 
                              })
                              .on('mousemove', function(d) {
      
                                tooltip.style('top', (d3v2.event.layerY + 10) + 'px')
                                       .style('left', (d3v2.event.layerX - 25) + 'px');
  
                              })
                              .on('mouseout', function(d) {
      
                                tooltip.style('display', 'none')
                                       .style('opacity',0);


                              });
    
    newChords.append("title");
    
    chordPaths.exit().transition()
              .duration(1500)
              .attr("opacity", 0)
              .remove();
    
    chordPaths.transition()
              .duration(2000)
              .attr("opacity", 0.2) 
              .style("fill", function (d) {
                return group_color(chart_data_general[d3v2.max([d.source.index,d.target.index])].group, 
                  female_color=female_color, male_color=male_color,na_color=na_color)
              })
              .attrTween("d", chordTween(last_layout))
              .transition().delay(delay_1).duration(1000).attr("opacity", function(d,i) {
            target_id       = chart_data_general[d3v2.max([d.source.index,d.target.index])].label
            if (target_id==most_send) {
              return 1
            } else {
            return 0.2}})
            .transition().delay(delay_2).duration(2000).attr("opacity", 0.5)

    groupG.on("mouseover", function(d) {
        
        chordPaths.classed("fade", function (p) {
            return ((p.source.index != d.index) && (p.target.index != d.index));
        });
        
        target_id       = d.index
        d3v2.selectAll('.test').filter(function(d,i) {

            text = $contact_name[d.index]
            target = $contact_name[target_id]
            return (text == target);
      
        }). attr("font-size", "8px")

        if (target_id!=0) {
           
            target_name     = chart_data_general[target_id].label
            target_email    = chart_data_general[target_id].label_detail
            sent_email      = chart_data_general[target_id].value_1
            received_email  = chart_data_general[target_id].value_2

            tooltip.select('.name').html("<b>" + target_name + "</b>");
            tooltip.select('.email').html("<i>(" + target_email + ")</i>");
            tooltip.select('.value_sent').html("Emails (Sent): <b>" + sent_email + "<b>");
            tooltip.select('.value_received').html("Emails (Received): <b>" + received_email + "<b>");

            tooltip.style('display', 'block')
                   .style('opacity',2);

        } 
    })
    .on('mousemove', function(d) {
      
      tooltip.style('top', (d3v2.event.layerY + 10) + 'px')
             .style('left', (d3v2.event.layerX - 25) + 'px');
  
    })
    .on('mouseout', function(d) {
      
      d3v2.selectAll('.test').attr("font-size", "7px")
      
      tooltip.style('display', 'none')
             .style('opacity',0);
    });
    
    last_layout = layout; 


}


 