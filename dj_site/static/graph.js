var clearGraph = function(curSvg){
  var svg = d3.select(curSvg);
  svg.selectAll("*").remove();
};

var createGraph = function(graph, curSvg){
  var svg = d3.select(curSvg),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

  var link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(graph.links)
      .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
      .attr("stroke", "#ccc");

  var node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("r", 50)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("title")
      .text(function(d) { return d.id; });

  // Add node names as text elements
  var nodeName = svg.append("g")
    .attr("class", "node-names")
    .selectAll("text")
    .data(graph.nodes)
    .enter().append("text")
    .text(function(d) { return d.id; })
    .attr("dx", 12)
    .attr("dy", 4);   

  // Add edge names as text elements
  var linkName = svg.append("g")
    .attr("class", "link-names")
    .selectAll("text")
    .data(graph.links)
    .enter().append("text")
    .text(function(d) { return d.id; })
    .attr("dx", 5)
    .attr("dy", -5);   

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

        // Position node names at the same coordinates as nodes
    nodeName
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; });

    // Position edge names at the midpoint of the corresponding edges
    linkName
      .attr("x", function(d) { return (d.source.x + d.target.x) / 2; })
      .attr("y", function(d) { return (d.source.y + d.target.y) / 2; });    
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
};

var scaleNodeSize = function(){

};
