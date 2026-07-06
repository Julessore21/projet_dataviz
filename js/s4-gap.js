'use strict';

function initS4Gap() {
  var container = document.getElementById('viz-gap-wrap');
  var svgEl     = document.getElementById('viz-gap');
  if (!container || !svgEl) return;

  /* ── Layout ──────────────────────────────────────────────────────── */
  var margin = { top: 55, right: 50, bottom: 55, left: 210 };
  var W  = 480, H = 290;
  var iW = W - margin.left - margin.right;
  var iH = H - margin.top  - margin.bottom;

  svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svgEl.setAttribute('width',  '100%');
  svgEl.setAttribute('height', '100%');
  svgEl.style.maxHeight = H + 'px';

  var svg = d3.select(svgEl)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var tasks      = DATA.gap.tasks;
  var refVal     = DATA.gap.itRulesStrict; // 28.2

  /* ── Scales ──────────────────────────────────────────────────────── */
  var xScale = d3.scaleLinear()
    .domain([0, 70])
    .range([0, iW]);

  var yScale = d3.scaleBand()
    .domain(tasks.map(function(d) { return d.label; }))
    .range([0, iH])
    .padding(0.5);

  var rowMid = function(d) { return yScale(d.label) + yScale.bandwidth() / 2; };

  /* ── Axes ────────────────────────────────────────────────────────── */
  svg.append('g')
    .attr('transform', 'translate(0,' + iH + ')')
    .call(d3.axisBottom(xScale)
      .tickValues([0, 28.2, 40, 60])
      .tickFormat(function(v) { return v + ' %'; })
      .tickSize(-iH)
    )
    .call(function(g) {
      g.select('.domain').remove();
      g.selectAll('.tick line')
        .attr('stroke-dasharray', '3 3')
        .attr('opacity', function(v) { return v === 28.2 ? 0 : 0.3; });
      g.selectAll('.tick text')
        .attr('class', 'axis-label')
        .attr('dy', '1.2em');
    });

  svg.append('g')
    .call(d3.axisLeft(yScale).tickSize(0))
    .call(function(g) {
      g.select('.domain').remove();
      g.selectAll('.tick text')
        .attr('class', 'dumbbell-task-label')
        .attr('x', -10)
        .attr('text-anchor', 'end');
    });

  /* ── Reference vertical line (IT rules at 28.2%) ─────────────────── */
  svg.append('line')
    .attr('class', 'ref-line')
    .attr('x1', xScale(refVal)).attr('x2', xScale(refVal))
    .attr('y1', -28).attr('y2', iH + 12);

  // Label above
  svg.append('text')
    .attr('x', xScale(refVal))
    .attr('y', -34)
    .attr('text-anchor', 'middle')
    .attr('class', 'axis-label')
    .attr('fill', '#4FD1C5')
    .style('font-size', '0.6rem')
    .text('Règles IT strictes');

  svg.append('text')
    .attr('x', xScale(refVal))
    .attr('y', -22)
    .attr('text-anchor', 'middle')
    .attr('class', 'axis-label')
    .attr('fill', '#4FD1C5')
    .style('font-size', '0.6rem')
    .text(refVal + ' %');

  /* ── Dumbbell tracks (background) ──────────────────────────────────── */
  tasks.forEach(function(d) {
    var x1 = xScale(Math.min(d.usage, refVal));
    var x2 = xScale(Math.max(d.usage, refVal));
    svg.append('line')
      .attr('class', 'dumbbell-track')
      .attr('x1', x1).attr('x2', x2)
      .attr('y1', rowMid(d)).attr('y2', rowMid(d));
  });

  /* ── Dumbbell animated lines ─────────────────────────────────────── */
  var lines = svg.selectAll('.dumbbell-line')
    .data(tasks)
    .enter()
    .append('line')
    .attr('class', function(d) {
      var direction = d.usage > refVal ? 'above' : 'below';
      return 'dumbbell-line dumbbell-line--' + direction;
    })
    .attr('x1', function(d) { return xScale(Math.min(d.usage, refVal)); })
    .attr('x2', function(d) { return xScale(Math.max(d.usage, refVal)); })
    .attr('y1', rowMid).attr('y2', rowMid)
    .attr('stroke-dasharray', function() {
      return this.getTotalLength ? this.getTotalLength() : 200;
    })
    .attr('stroke-dashoffset', function() {
      return this.getTotalLength ? this.getTotalLength() : 200;
    });

  /* Fix dasharray after append (getTotalLength needs rendered element) */
  lines.each(function() {
    var len = this.getTotalLength();
    d3.select(this)
      .attr('stroke-dasharray', len)
      .attr('stroke-dashoffset', len);
  });

  /* ── Reference dots (cyan) ───────────────────────────────────────── */
  svg.selectAll('.dot-ref')
    .data(tasks)
    .enter()
    .append('circle')
    .attr('class', 'dot-ref')
    .attr('cx', xScale(refVal))
    .attr('cy', rowMid)
    .attr('r', 6);

  /* ── Usage dots (amber for shadow, cyan for self-reg) ────────────── */
  svg.selectAll('.dot-usage')
    .data(tasks)
    .enter()
    .append('circle')
    .attr('class', function(d) {
      return 'dot-usage dot-usage--' + d.stakes;
    })
    .attr('cx', function(d) { return xScale(d.usage); })
    .attr('cy', rowMid)
    .attr('r', 6);

  /* ── Usage value labels ───────────────────────────────────────────── */
  tasks.forEach(function(d) {
    var above = d.usage > refVal;
    svg.append('text')
      .attr('class', 'dumbbell-value-label')
      .attr('x', xScale(d.usage) + (above ? 10 : -10))
      .attr('y', rowMid(d))
      .attr('text-anchor', above ? 'start' : 'end')
      .text(d.usage + ' %');

    // Stakes badge
    svg.append('text')
      .attr('class', 'stakes-badge')
      .attr('x', xScale(d.usage) + (above ? 10 : -10))
      .attr('y', rowMid(d) + 12)
      .attr('text-anchor', above ? 'start' : 'end')
      .attr('fill', d.stakes === 'low' ? '#F0B429' : '#4FD1C5')
      .style('font-size', '0.55rem')
      .text(d.stakes === 'low' ? '↑ enjeu faible' : '↓ enjeu élevé');
  });

  /* ── Animation ────────────────────────────────────────────────────── */
  function animate() {
    lines.transition()
      .duration(dur(650))
      .delay(function(d, i) { return dur(i * 200); })
      .ease(d3.easeCubicOut)
      .attr('stroke-dashoffset', 0);
  }

  ScrollTrigger.create(stConfig('#s4-gap', { onEnter: animate }));

  addVizLegend(container, [DATA.gap.source]);

  // Extra note below legend
  var note = document.createElement('p');
  note.className = 'viz-note';
  note.textContent = DATA.gap.note;
  container.appendChild(note);
}
