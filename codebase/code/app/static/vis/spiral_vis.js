console.log("Spiral Vis")

// # Initialize visualization variables
// # ------------------------------
// # ------------------------------

var width = 700
var height = 530
var start = 0,
  end = 2.25,
  numSpirals = 3
  margin = {top:0,bottom:0,left:0,right:0};

var color  = d3.scaleOrdinal(d3.schemeCategory10);

// # Prepare Visualization # 1 - Spiral
// # ------------------------------
// # ------------------------------

var generate_spiral = function() {

  // # Prepare Data
  // # -------------
  var chart_data = [];
  for (var i = 0; i < 365; i++) {

    var currentDate = new Date();
    currentDate.setDate(currentDate.getDate() - i-1);
    
      chart_data.push({
      date: currentDate,
      value: $email_count[i]
    });
  }

  $start_date = new Date($start_date)
  $end_date   = new Date($end_date)

  // # Prepare Visualization variables
  // # -------------
  var r      = d3.min([width, height]) / 2 - 40;
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
  
  // ## BASIC
  var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.left + margin.right)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
  
  var points = d3.range(start, end + 0.001, (end - start) / 1000);
  
  var spiral = d3.radialLine()
    .curve(d3.curveCardinal)
    .angle(theta)
    .radius(radius);
  
  var path = svg.append("path")
    .datum(points)
    .attr("id", "spiral")
    .attr("d", spiral)
    .style("fill", "none")
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
  
  svg.selectAll("rect")
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
    .style("fill", function(d){return color(d.group);})
    .attr("transform", function(d){
      return "rotate(" + d.a + "," + d.x  + "," + d.y + ")"; 
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
  
      tooltip.select('.date').html("Date: <b>" + d.date.toDateString() + "</b>");
      tooltip.select('.value').html("Number of Emails: <b>" + Math.round(d.value*100)/100 + "<b>");
      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
      .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
    
    d3.select(this)
      .style("fill",function(d){return color(d.group);})
      .style("stroke","none");
  
    tooltip.style('display', 'none');
    tooltip.style('opacity',0);
  
  });

}

// # Prepare Visualization # 2 - Bar
// # ------------------------------
// # ------------------------------

var generate_bar = function(mode) {
    
  // # Reset
  // # -------------
  var s = d3.selectAll('svg');
  s.remove();
  
  // # Prepare Data
  // # -------------
  var chart_data = [];
  if (mode=="all") {
    for (var i = 0; i < $email_date_subset.length; i++) {
      var currentDate = new Date($email_date_subset[i]);
      chart_data.push({
        date: currentDate,
        value_default: $email_count_subset[i],
        value: $email_count_subset[i]
      });
    }
  } else if (mode=="sent") {
    for (var i = 0; i < $email_date_subset.length; i++) {
      var currentDate = new Date($email_date_subset[i]);
      chart_data.push({
        date: currentDate,
        value_default: $email_count_subset[i],
        value: $email_count_sent_subset[i]
      });
    }
  } else if (mode=="received") {
    for (var i = 0; i < $email_date_subset.length; i++) {
      var currentDate = new Date($email_date_subset[i]);
      chart_data.push({
        date: currentDate,
        value_default: $email_count_subset[i],
        value: $email_count_received_subset[i]
      });
    }
  }
  
  // # Prepare Visualization variables
  // # -------------
  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().rangeRound([height, 0]);

  // # Create Visualization
  // # -------------
 
  // ## BASIC
  var svg = d3.select("#chart").append("svg")
    .attr("align","left")
    .attr("width", width)
    .attr("height", height)
    .append("g")

  // ## TEXT
  svg.append("text")
      .text("All Emails")
      .attr("transform", "translate(" + 50 + "," + 100 + ")")
      .on("click", function() { generate_bar(mode="all"); });
 
  svg.append("text")
      .text("Sent Emails")
      .attr("transform", "translate(" + 50 + "," + 120 + ")")
      .on("click", function() { generate_bar(mode="sent"); });

  svg.append("text")
      .text("Received Emails")
      .attr("transform", "translate(" + 50 + "," + 140 + ")")
      .on("click", function() { generate_bar(mode="received"); });

  // ## CHART
  var g = svg.append("g")

  x.domain(chart_data.map(function(d) { return d.date; }));
  y.domain([0, d3.max(chart_data, function(d) { return d.value_default; })]);


  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.selectAll(".bar")
    .data(chart_data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.date); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.value); })


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
  
      tooltip.select('.date').html("Date: <b>" + d.date.toDateString() + "</b>");
      tooltip.select('.value').html("Number of Emails: <b>" + Math.round(d.value*100)/100 + "<b>");
      tooltip.style('display', 'block');
      tooltip.style('opacity',2);
  
  })
  .on('mousemove', function(d) {
      
      tooltip.style('top', (d3.event.layerY + 10) + 'px')
      .style('left', (d3.event.layerX - 25) + 'px');
  
  })
  .on('mouseout', function(d) {
      
    tooltip.style('display', 'none');
    tooltip.style('opacity',0);
  
  });


};

// # Create Animation
// # ------------------------------
// # ------------------------------


// # Transition Functions
// # -------------

// ## stage_entry
var stage_entry = function() {
  
  // ## initialize text
  d3.select("#text")
    .text("Over The Past 365 Days You Sent and Received XX Emails - That's XX Emails/Day");
  d3.select("#text_link")
    .text("Next")
    .on("click", function() { stage_1(); });
  
  // ## initialize visualization
  generate_spiral()

}

// ## stage_1
var stage_1 = function() {
  
  // ## update text
  d3.select("#text")
    .text("We've Analysed Your Last XX Emails Over The Period XX to XX");
  d3.select("#text_link")
    .text("Next")
    .on("click", function() { stage_2(); });
  
  // ## update visualization
  d3.selectAll("rect")
    .transition()
    .style("fill", function(d) {return color(d.date<=$end_date & d.date>=$start_date); });

}

// ## stage_2
var stage_2 = function() {
  
  // ## update text
  d3.select("#text")
    .text("Over The Past XX Days You Sent XX Emails And Received XX Emails");
  
  var s = d3.selectAll('#text_link');
  s.remove();

  $('#navigation').text("Lets Take A Look At Some Patterns");

  // ## update visualization
  generate_bar(mode="all")

}

// # Launch
// # -------------
stage_entry()

// END