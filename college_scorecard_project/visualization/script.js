
function drawGraph(xText, yText) {
		$('svg').remove();
		var margin = {top: 20, right: 80, bottom: 50, left: 80},
			width = 1060 - margin.left - margin.right,
			height = 550 - margin.top - margin.bottom;

		/* 
		 * value accessor - returns the value to encode for a given data object.
		 * scale - maps value to a visual display encoding, such as a pixel position.
		 * map function - maps from data value to display value
		 * axis - sets up axis
		 */

		var xCat = xText,
			yCat = yText;

		// setup x 
		var xValue = function(d) { return d[xCat];}, // data -> value
			xScale = d3.scale.linear().range([0, width]).nice(), // value -> display
			xMap = function(d) { return xScale(xValue(d));} // data -> display


		// setup y
		var yValue = function(d) { return d[yCat];}, // data -> value
			yScale = d3.scale.linear().range([height, 0]).nice(), // value -> display
			yMap = function(d) { return yScale(yValue(d));} // data -> display


		// load data
		d3.csv("df_joined.csv", function(error, data) {

		  // change string (from CSV) into number format
		  	data.forEach(function(d) {
				d[yText] = +d[yText];
				d[xText] = +d[xText];
			});


			var xMax = d3.max(data, function(d) { return + d[xText]; }) * 1.05,
		      	xMin = d3.min(data, function(d) { return + d[xText]; }) / 1.05,
		      	yMax = d3.max(data, function(d) { return + d[yText]; }) * 1.05,
		      	yMin = d3.min(data, function(d) { return + d[yText]; }) / 1.05 ;


			  // don't want dots overlapping axis, so add in buffer to data domain
			  // xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
			  // yScale.domain([d3.min(data, yValue)-0.3, d3.max(data, yValue)+0.3]);
			
			xScale.domain([xMin-0.1, xMax+0.1]);
	  		yScale.domain([yMin-0.1, yMax+0.1]);

	  		xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(-height);
			yAxis = d3.svg.axis().scale(yScale).orient("left").tickSize(-width);

			var tip = d3.tip()
		      .attr("class", "d3-tip")
		      .offset([-10, 0])
		      .html(function(d) {
		        return d.INSTNM + "<br/>(" + xValue(d) + ", " + yValue(d) + ")";
		      });

		    var zoomBeh = d3.behavior.zoom()
		      .x(xScale) // this might be the problem
		      .y(yScale)
		      .scaleExtent([0, 500])
		      .on("zoom", zoom);

	  			// sets up the canvas
			var svg = d3.select("body").append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
			  .append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				.call(zoomBeh);

			svg.call(tip);

			svg.append("rect")
		      .attr("width", width)
		      .attr("height", height);

				// this draws the x-axis labels
			svg.append("g")
		      .classed("x axis", true)
		      .attr("transform", "translate(0," + height + ")")
		      .call(xAxis)
		    .append("text")
		      .classed("label", true)
		      .attr("x", width + 30)
		      .attr("y", margin.bottom - 20)
		      .style("text-anchor", "end")
		      .text(xCat);

				// draws y-axis labels
			svg.append("g")
		      .classed("y axis", true)
		      .call(yAxis)
		    .append("text")
		      .classed("label", true)
		      .attr("transform", "rotate(-90)")
		      .attr("x", -10)
		      .attr("y", -60)
		      .attr("dy", ".71em")
		      .style("text-anchor", "end")
		      .text(yCat);
	   			

			var objects = svg.append("svg")
		      .classed("objects", true)
		      .attr("width", width)
		      .attr("height", height);

				// draws x-axis lines
			objects.append("svg:line")
		      .classed("axisLine hAxisLine", true)
		      .attr("x1", 0)
		      .attr("y1", 0)
		      .attr("x2", width)
		      .attr("y2", 0)
		      .attr("transform", "translate(0," + height + ")");

			    // draws your y axis line  
			objects.append("svg:line")
		      .classed("axisLine vAxisLine", true)
		      .attr("x1", 0)
		      .attr("y1", 0)
		      .attr("x2", 0)
		      .attr("y2", height);

		      // draws your circles and animate tiptools
			objects.selectAll(".dot")
		      .data(data)
		    .enter().append("circle")
		      .classed("dot", true)
		      .attr("r", 3.5)
		      .attr("transform", transform)
		      .style("fill", function(d) { return "#00ccbc"; })
		      .style("opacity",0.5) 
		      .on("mouseover", tip.show)
		      .on("mouseout", tip.hide);
			

			function zoom() {
				console.log(xAxis);
			    svg.select(".x.axis").call(xAxis);
			    svg.select(".y.axis").call(yAxis);

			    svg.selectAll(".dot")
		        	.attr("transform", transform);
	  		}
	  		
	  		function transform(d) {
	    		return "translate(" + xScale(d[xCat]) + "," + yScale(d[yCat]) + ")";

	  		}

		});
	}

	drawGraph('MN_EARN_WNE_P10', 'MN_EARN_WNE_P10');

	function setGraph() {
		drawGraph($('#x-value').val(), $('#y-value').val());
	}
