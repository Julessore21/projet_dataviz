'use strict';

function initS6Trust() {
  var container = document.getElementById('viz-trust-wrap');
  var svgEl     = document.getElementById('viz-trust');
  if (!container || !svgEl) return;

  /* ── Layout ──────────────────────────────────────────────────────── */
  var margin = { top: 55, right: 90, bottom: 60, left: 80 };
  var W  = 480, H = 320;
  var iW = W - margin.left - margin.right;
  var iH = H - margin.top  - margin.bottom;

  svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svgEl.setAttribute('width',  '100%');
  svgEl.setAttribute('height', '100%');
  svgEl.style.maxHeight = H + 'px';

  var svg = d3.select(svgEl)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var trustData = DATA.trust.bySeniority;
  var labels    = trustData.map(function(d) { return d.label; });

  /* ── Scales ──────────────────────────────────────────────────────── */
  var xScale = d3.scalePoint()
    .domain(labels)
    .range([0, iW])
    .padding(0.25);

  var yScale = d3.scaleLinear()
    .domain([0, 24])
    .range([iH, 0]);

  /* ── Axes ────────────────────────────────────────────────────────── */
  svg.append('g')
    .attr('transform', 'translate(0,' + iH + ')')
    .call(d3.axisBottom(xScale).tickSize(0))
    .call(function(g) {
      g.select('.domain').attr('stroke', '#30363D');
      g.selectAll('.tick text')
        .attr('class', 'trust-axis-label')
        .attr('dy', '1.4em');
    });

  svg.append('g')
    .call(d3.axisLeft(yScale)
      .tickValues([0, 5, 10, 15, 20])
      .tickFormat(function(d) { return d + ' %'; })
      .tickSize(-iW)
    )
    .call(function(g) {
      g.select('.domain').remove();
      g.selectAll('.tick line').attr('stroke-dasharray', '3 3').attr('opacity', 0.25);
      g.selectAll('.tick text').attr('class', 'trust-axis-label');
    });

  /* ── Legend ─────────────────────────────────────────────────────── */
  var legendData = [
    { label: '% "très confiant"',  color: '#4FD1C5' },
    { label: '% "très méfiant"',   color: '#F0B429' }
  ];
  var lg = svg.append('g').attr('transform', 'translate(' + (iW - 5) + ',' + (-38) + ')');
  legendData.forEach(function(ld, i) {
    var row = lg.append('g').attr('transform', 'translate(0,' + (i * 17) + ')');
    row.append('line')
      .attr('x1', -50).attr('x2', -8)
      .attr('y1', 0).attr('y2', 0)
      .attr('stroke', ld.color).attr('stroke-width', 2.5);
    row.append('text')
      .attr('x', 0).attr('y', 0)
      .attr('dominant-baseline', 'middle')
      .attr('class', 'trust-legend-item')
      .text(ld.label);
  });

  /* ── Line generators ─────────────────────────────────────────────── */
  var lineFav = d3.line()
    .x(function(d) { return xScale(d.label); })
    .y(function(d) { return yScale(d.favorable); })
    .curve(d3.curveCatmullRom.alpha(0.5));

  var lineSkep = d3.line()
    .x(function(d) { return xScale(d.label); })
    .y(function(d) { return yScale(d.skeptical); })
    .curve(d3.curveCatmullRom.alpha(0.5));

  /* ── Draw lines ─────────────────────────────────────────────────── */
  var pathFav = svg.append('path')
    .datum(trustData)
    .attr('class', 'trust-line trust-line--fav')
    .attr('d', lineFav);

  var pathSkep = svg.append('path')
    .datum(trustData)
    .attr('class', 'trust-line trust-line--skep')
    .attr('d', lineSkep);

  /* Dasharray via GSAP inline style (overrides CSS class) */
  var favLen  = pathFav.node().getTotalLength();
  var skepLen = pathSkep.node().getTotalLength();
  gsap.set(pathFav.node(),  { strokeDasharray: favLen,  strokeDashoffset: favLen  });
  gsap.set(pathSkep.node(), { strokeDasharray: skepLen, strokeDashoffset: skepLen });

  /* ── Data point dots ─────────────────────────────────────────────── */
  trustData.forEach(function(d) {
    var cx = xScale(d.label);
    svg.append('circle')
      .attr('class', d.srcFav
        ? 'trust-dot-source trust-dot-source--fav'
        : 'trust-dot-interp trust-dot-interp--fav')
      .attr('cx', cx).attr('cy', yScale(d.favorable))
      .attr('r', d.srcFav ? 5 : 3);

    svg.append('circle')
      .attr('class', d.srcSkep
        ? 'trust-dot-source trust-dot-source--skep'
        : 'trust-dot-interp trust-dot-interp--skep')
      .attr('cx', cx).attr('cy', yScale(d.skeptical))
      .attr('r', d.srcSkep ? 5 : 3);

    if (d.srcFav) {
      svg.append('text')
        .attr('class', 'trust-label')
        .attr('x', cx - 8).attr('y', yScale(d.favorable) - 10)
        .attr('text-anchor', 'middle').attr('fill', '#4FD1C5')
        .style('font-size', '0.62rem').text(d.favorable + ' %');
    }
    if (d.srcSkep) {
      svg.append('text')
        .attr('class', 'trust-label')
        .attr('x', cx + 8).attr('y', yScale(d.skeptical) - 10)
        .attr('text-anchor', 'middle').attr('fill', '#F0B429')
        .style('font-size', '0.62rem').text(d.skeptical + ' %');
    }
  });

  /* ── Crossing point annotation ───────────────────────────────────── */
  var d0 = trustData[0], d1 = trustData[1];
  var t  = (d0.favorable - d0.skeptical) / ((d0.favorable - d0.skeptical) - (d1.favorable - d1.skeptical));
  var crossX = xScale(d0.label) + t * (xScale(d1.label) - xScale(d0.label));
  var crossY = yScale(d0.favorable + t * (d1.favorable - d0.favorable));

  var crossMarker = svg.append('circle')
    .attr('class', 'trust-cross-marker')
    .attr('cx', crossX).attr('cy', crossY).attr('r', 10);

  var crossLabel = svg.append('text')
    .attr('class', 'trust-cross-label')
    .attr('x', crossX).attr('y', crossY - 16)
    .attr('text-anchor', 'middle').attr('fill', '#E6E6E6')
    .style('font-size', '0.6rem').text('Point de bascule');

  /* ── Interpolation note ──────────────────────────────────────────── */
  svg.append('text')
    .attr('x', 0).attr('y', iH + 48)
    .attr('class', 'trust-axis-label')
    .style('font-size', '0.55rem').attr('fill', '#8B949E')
    .text('⚠ Points intermédiaires : tendance interpolée. Valeurs source : cercles ouverts.');

  /* ── Animation — toujours via GSAP (inline style > classe CSS) ──── */
  function animate() {
    gsap.to(pathFav.node(), {
      strokeDashoffset: 0,
      duration: dur(1.2),
      ease: 'power2.inOut'
    });
    gsap.to(pathSkep.node(), {
      strokeDashoffset: 0,
      duration: dur(1.2),
      delay: dur(0.2),
      ease: 'power2.inOut',
      onComplete: function() {
        gsap.to(crossMarker.node(), { opacity: 1, duration: dur(0.4) });
        gsap.to(crossLabel.node(),  { opacity: 1, duration: dur(0.4) });
      }
    });
  }

  /* ScrollTrigger toujours actif ; dur() = 0 si reduced-motion */
  ScrollTrigger.create(stConfig('#s6-trust', { onEnter: animate }));

  addVizLegend(container, [DATA.trust.source]);

  var note = document.createElement('p');
  note.className = 'viz-note';
  note.textContent = 'Courbes : % "très confiant" et % "très méfiant" de l\'exactitude des outputs IA, par niveau d\'ancienneté. ' + DATA.trust.n;
  container.appendChild(note);
}
