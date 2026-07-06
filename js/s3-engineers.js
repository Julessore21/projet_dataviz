'use strict';

function initS3Engineers() {
  var container = document.getElementById('viz-engineers-wrap');
  var svgEl     = document.getElementById('viz-engineers');
  if (!container || !svgEl) return;

  /* ── Layout ──────────────────────────────────────────────────────── */
  var margin = { top: 30, right: 60, bottom: 50, left: 195 };
  var W  = 480, H = 260;
  var iW = W - margin.left - margin.right;
  var iH = H - margin.top  - margin.bottom;

  svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svgEl.setAttribute('width',  '100%');
  svgEl.setAttribute('height', '100%');
  svgEl.style.maxHeight = H + 'px';

  var svg = d3.select(svgEl)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var data = DATA.engineers.bySeniority;

  /* ── Scales ──────────────────────────────────────────────────────── */
  var xScale = d3.scaleLinear()
    .domain([0, 65])
    .range([0, iW]);

  var yScale = d3.scaleBand()
    .domain(data.map(function(d) { return d.label; }))
    .range([0, iH])
    .padding(0.42);

  /* ── Axes ────────────────────────────────────────────────────────── */
  // X axis (bottom)
  svg.append('g')
    .attr('transform', 'translate(0,' + iH + ')')
    .call(d3.axisBottom(xScale)
      .tickValues([0, 20, 40, 60])
      .tickFormat(function(d) { return d + ' %'; })
      .tickSize(-iH)
    )
    .call(function(g) {
      g.select('.domain').remove();
      g.selectAll('.tick line').attr('stroke-dasharray', '3 3').attr('opacity', 0.3);
      g.selectAll('.tick text').attr('class', 'axis-label').attr('dy', '1.2em');
    });

  // Y axis (left labels)
  svg.append('g')
    .call(d3.axisLeft(yScale).tickSize(0))
    .call(function(g) {
      g.select('.domain').remove();
      g.selectAll('.tick text')
        .attr('class', 'bar-label')
        .attr('x', -8)
        .attr('text-anchor', 'end')
        .style('font-size', '0.68rem');
    });

  /* ── Background tracks ───────────────────────────────────────────── */
  svg.selectAll('.bar-bg')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar-bg')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.label); })
    .attr('width', xScale(65))
    .attr('height', yScale.bandwidth())
    .attr('rx', 3);

  /* ── Bars (start at width 0) ─────────────────────────────────────── */
  var bars = svg.selectAll('.bar-fill')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar-fill')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.label); })
    .attr('width', 0)
    .attr('height', yScale.bandwidth())
    .attr('rx', 3);

  /* ── Value labels ────────────────────────────────────────────────── */
  var valueLabels = svg.selectAll('.bar-value')
    .data(data)
    .enter()
    .append('text')
    .attr('class', 'bar-value')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.label) + yScale.bandwidth() / 2; })
    .attr('dy', '0.35em')
    .attr('opacity', 0)
    .text(function(d) { return d.daily + ' %'; });

  /* ── Chart title ─────────────────────────────────────────────────── */
  d3.select(svgEl).append('text')
    .attr('x', margin.left)
    .attr('y', 18)
    .attr('class', 'axis-label')
    .attr('fill', '#8B949E')
    .style('font-size', '0.65rem')
    .text('Usage IA quotidien par ancienneté');

  /* ── Animation ──────────────────────────────────────────────────── */
  function animate() {
    bars.transition()
      .duration(dur(700))
      .delay(function(d, i) { return dur(i * 150); })
      .ease(d3.easeCubicOut)
      .attr('width', function(d) { return xScale(d.daily); });

    valueLabels
      .transition()
      .duration(dur(400))
      .delay(function(d, i) { return dur(i * 150 + 500); })
      .attr('x', function(d) { return xScale(d.daily) + 8; })
      .attr('opacity', 1);
  }

  /* dur() retourne 0 quand REDUCED_MOTION est actif → animation instantanée */
  ScrollTrigger.create(stConfig('#s3-engineers', { onEnter: animate }));

  addVizLegend(container, [DATA.engineers.source]);
}
