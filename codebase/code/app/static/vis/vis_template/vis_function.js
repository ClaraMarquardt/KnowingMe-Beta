// # MISC
// # ------------------------------
// # ------------------------------
var format           = d3.format(",d");
var formatPercent    = d3.format("%");
var numberWithCommas = d3.format("0,f");
var formatCount      = d3.format(",.0f");

// # MISC FUNCTIONS
// # ------------------------------
// # ------------------------------

// ## update_insight
// # ------------------------------
var update_insight = function(reset_class, insight_name, redirect_url) {
    
     $(document).ready(function() { 
        $.get(redirect_url,function(data) {

                // # reset 
                reset_vis(reset_class=reset_class)

                 // # update data
                update_raw_data(raw_data=data.insight_data)

                // # update vis
                stage_entry()
            }
        )
    })

}

// ## reset_vis
// # ------------------------------
var reset_vis = function(reset_class) {

    for (var i = 0; i < Object.keys(reset_class).length; i++) {
      d3.selectAll(reset_class[i]).remove().exit()

    }
}

// ## generate_text_fade
// # ------------------------------
var generate_text_fade = function(obj_id="#text", text_new, delay, duration) {

	d3.select(obj_id)
      .text("")
      .transition()
      .delay(delay)
      .duration(duration)
      .on("start", function repeat() {
        var t = d3.active(this)
                  .style("opacity", 0)
        d3.select(obj_id)
          .style("opacity", 0)
          .html(text_new)
          .transition(t)
          .style("opacity", 1)
    });
}

// ## generate_next_link
// # ------------------------------
var generate_next_link = function(obj_id="#text_link", text_new="<i>See More</i>", function_new, delay, duration) {

  d3.select(obj_id).selectAll("svg"). remove()
	
  if (function_new!="") {

   		d3.select(obj_id)
        .append("svg")
        .attr("width",15)
        .attr("height",15)   
        .append("image")
        .attr('xlink:href','static/image/icon/next.png')
        .attr("width",15)
        .attr("height",15)
        // .attr("x", 150)
   		  .on("click", function() { function_new() })

  	} 
}

// ## generate_text_main
// # ------------------------------
var generate_text_main = function(text_content, text_duration, text_delay, function_new) {

    for (var i = 0; i < Object.keys(text_content).length; i++) {

		  if (text_content[i]!="LINK") {
			   generate_text_fade(obj_id="#text", text_new=text_content[i], 
				    delay=text_delay[i], duration=text_duration[i])

		  } else {

			   generate_next_link(obj_id="#text_link", 
				  text_new="<i>See More</i>", function_new=function_new, 
				  delay=text_delay[i], duration=text_duration[i])

		  }
    }
}

// ## gender_color
// # ------------------------------
var group_color = function(group, female_color, male_color, na_color) {
  if (group=="F") {
      return (female_color)
    } else if (group=="M") {
      return (male_color)
    } else {
      return (na_color)
    }
}
 
// ## hour_color
// # ------------------------------
var hour_color = function(group, night_color="#aaa", morning_color="#000", afternoon_color="#000",evening_color="#aaa") {
   if (group<6) {
      return (night_color)
    } else if (group>=6 & group < 12) {
       return (morning_color)
    } else if (group>=12 & group < 18) {
       return (afternoon_color)
    } else if (group>=18 & group <= 23) {
       return (evening_color)
    } 
}


// ## button_d3
// # ------------------------------
button_d3 = function() {

  var dispatch = d3.dispatch('press', 'release');

  var padding = 3,
      radius = 3,
      stdDeviation = 5,
      offsetX = 1,
      offsetY = 1;

  function my(selection) {
    selection.each(function(d, i) {
      var g = d3.select(this)
          .attr('id', 'd3-button' + i)
          .attr('transform', 'translate(' + d.x + ',' + d.y + ')');

      var text = g.append('text').text(d.label);
      var defs = g.append('defs');
      var bbox = text.node().getBBox();
      var rect = g.insert('rect', 'text')
          .attr("x", bbox.x - padding)
          .attr("y", bbox.y - padding)
          // .attr("width", bbox.width + 2 * padding)
          .attr("width", function(d, i) { return d.width})
          .attr("height", bbox.height + 2 * padding)
          .attr('rx', radius)
          .attr('ry', radius)
          .on('mouseover', activate)
          .on('mouseout', deactivate)
          .on('click', toggle)

       addShadow.call(g.node(), d, i);
       addGradient.call(g.node(), d, i);
    });
  }

  function addGradient(d, i) {
    var defs = d3.select(this).select('defs');
    var gradient = defs.append('linearGradient')
        .attr('id', 'gradient' + i)
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '0%')
        .attr('y2', '100%');

    gradient.append('stop')
        .attr('id', 'gradient-start')
        .attr('offset', '0%')

    gradient.append('stop')
        .attr('id', 'gradient-stop')
        .attr('offset', '100%')

    d3.select(this).select('rect').attr('fill', 'url(#gradient' + i + ")" );
  }

  function addShadow(d, i) {
    var defs = d3.select(this).select('defs');
    var rect = d3.select(this).select('rect').attr('filter', 'url(#dropShadow' + i + ")" );
    var shadow = defs.append('filter')
        .attr('id', 'dropShadow' + i)
        .attr('x', rect.attr('x'))
        .attr('y', rect.attr('y'))
        .attr('width', rect.attr('width') + offsetX)
        .attr('height', rect.attr('height') + offsetY)

    shadow.append('feGaussianBlur')
        .attr('in', 'SourceAlpha')
        .attr('stdDeviation', 2)

    shadow.append('feOffset')
        .attr('dx', offsetX)
        .attr('dy', offsetY);

    var merge = shadow.append('feMerge');

    merge.append('feMergeNode');
    merge.append('feMergeNode').attr('in', 'SourceGraphic');
  }

  function activate() {
  
    target_id = this.parentNode.id
    var gradient = d3.select(this.parentNode).select('linearGradient')
    d3.select(this.parentNode).select("rect").classed('active', true)
  
    d3.selectAll(".button").filter(function(d,i) {
      id = this.id
      return (id != target_id);
    }).select("rect").classed("pressed", false)

        d3.selectAll(".button").filter(function(d,i) {
      id = this.id
      return (id != target_id);

    }).select("linearGradient").select('#gradient-start').classed('active', false)

        d3.selectAll(".button").filter(function(d,i) {
      id = this.id
      return (id != target_id);
    }).select("linearGradient").select('#gradient-stop').classed('active', false)

    if (!gradient.node()) return;
    gradient.select('#gradient-start').classed('active', true)
    gradient.select('#gradient-stop').classed('active', true)
  }

  function deactivate() {
    var gradient = d3.select(this.parentNode).select('linearGradient')
    d3.select(this.parentNode).select("rect").classed('active', false)

    if (!gradient.node()) return;
    gradient.select('#gradient-start').classed('active', false);
    gradient.select('#gradient-stop').classed('active', false);
  }

  function toggle(d, i) {
    if (d3.select(this).classed('pressed')) {
        release.call(this, d, i);
        deactivate.call(this, d, i);
    } else {
        press.call(this, d, i);
        activate.call(this, d, i);
    }
  }

  function press(d, i) {
    dispatch.call('press', this, d, i)
    d3.select(this).classed('pressed', true);
    var shadow = d3.select(this.parentNode).select('filter')
    // if (!shadow.node()) return;
    // shadow.select('feOffset').attr('dx', 0).attr('dy', 0);
    // shadow.select('feGaussianBlur').attr('stdDeviation', 0);
  }

  function release(d, i) {
    dispatch.call('release', this, d, i)
    my.clear.call(this, d, i);
  }

  my.clear = function(d, i) {
    d3.select(this).classed('pressed', false);
    var shadow = d3.select(this.parentNode).select('filter')
    if (!shadow.node()) return;
    shadow.select('feOffset').attr('dx', offsetX).attr('dy', offsetY);
    shadow.select('feGaussianBlur').attr('stdDeviation', stdDeviation);
  }

  my.on = function() {
    var value = dispatch.on.apply(dispatch, arguments);
    return value === dispatch ? my : value;
  };

  return my;
}


// ## generate_button
// # ------------------------------
var generate_button = function (width, displ_x_origin,displ_x_step, displ_y_origin,displ_y_step, button_label, button_text, button_type) {

    var button_data = []
    var displ_x     = displ_x_origin
    var displ_y     = displ_y_origin

    for(var i=0; i<Object.keys(button_label).length; i++) {

      if (button_type[i]!="text") {

        button_data.push({
          label:          button_label[i],
          function_click: button_function[i],
          x:              displ_x,
          y:              displ_y, 
          width:          width
        })

      } else {

        g.append("text")
           .style("font-size", "7px")
           .style("font-style", "italic")
           .text(button_label[i])
           .attr("transform", "translate(" + (displ_x-12) + "," + (displ_y+5) + ")")

      }
     
      displ_x = displ_x + displ_x_step
      displ_y = displ_y + displ_y_step

    }


    var button_class = button_d3()
        .on('press', function(d, i) {console.log("Pressed", d, i, this.parentNode);})
        .on('release', function(d, i) {console.log("Released", d, i, this.parentNode)});
    
    var buttons = g.selectAll('.button')
                   .data(button_data)
                   .enter()
                   .append('g')
                   .attr('class', 'button')
                   .call(button_class)
                   .on("click", function(d) {d.function_click()})
}