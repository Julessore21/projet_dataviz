'use strict';

function initS2World() {
  const container = document.getElementById('viz-world-wrap');
  const svgEl     = document.getElementById('viz-world');
  if (!container || !svgEl) return;

  /* ── Dimensions ─────────────────────────────────────────────────── */
  const W = 520, H = 340;
  svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svgEl.setAttribute('width',  '100%');
  svgEl.setAttribute('height', '100%');
  svgEl.style.maxHeight = '340px';

  const svg = d3.select(svgEl);

  /* ── Projection ─────────────────────────────────────────────────── */
  const projection = d3.geoNaturalEarth1()
    .scale(90)
    .translate([W / 2, H / 2]);

  const path = d3.geoPath().projection(projection);

  /* ── Base: graticule + sphere ───────────────────────────────────── */
  const graticule = d3.geoGraticule().step([30, 30]);

  svg.append('path')
    .datum({ type: 'Sphere' })
    .attr('class', 'sphere-outline')
    .attr('d', path);

  svg.append('path')
    .datum(graticule())
    .attr('class', 'graticule')
    .attr('d', path);

  /* ── Country data ────────────────────────────────────────────────── */
  var countries = DATA.world.countries; // sorted descending by rate

  /* ── Radar sweep setup ─────────────────────────────────────────── */
  var cx = W / 2, cy = H / 2;
  var radius = Math.min(W, H) * 0.52;

  // Radial gradient for sweep glow
  var defs = svg.append('defs');
  var grad = defs.append('radialGradient')
    .attr('id', 'radar-grad')
    .attr('cx', '0%').attr('cy', '0%')
    .attr('r', '100%');
  grad.append('stop').attr('offset', '0%')
    .attr('stop-color', '#4FD1C5').attr('stop-opacity', '0.35');
  grad.append('stop').attr('offset', '100%')
    .attr('stop-color', '#4FD1C5').attr('stop-opacity', '0');

  // Sweep pie-slice (45° arc)
  var arcGen = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)
    .startAngle(-Math.PI / 8)
    .endAngle(Math.PI / 8);

  var sweepG = svg.append('g')
    .attr('class', 'radar-sweep')
    .attr('transform', 'translate(' + cx + ',' + cy + ')');

  sweepG.append('path')
    .attr('d', arcGen())
    .attr('fill', 'url(#radar-grad)')
    .attr('opacity', 0.9);

  // Trailing line
  sweepG.append('line')
    .attr('x1', 0).attr('y1', 0)
    .attr('x2', 0).attr('y2', -radius)
    .attr('stroke', '#4FD1C5')
    .attr('stroke-width', 1.5)
    .attr('opacity', 0.7);

  /* Continuous radar rotation — decoupled from scroll */
  if (!REDUCED_MOTION) {
    gsap.to(sweepG.node(), {
      rotation: 360,
      duration: 5,
      repeat: -1,
      ease: 'none',
      transformOrigin: '50% 50%',
      svgOrigin: cx + ' ' + cy
    });
  }

  /* ── Country markers ─────────────────────────────────────────────── */
  var countryGroups = svg.selectAll('.country-group')
    .data(countries)
    .enter()
    .append('g')
    .attr('class', 'country-group')
    .attr('transform', function(d) {
      var coords = projection([d.lon, d.lat]);
      return 'translate(' + coords[0] + ',' + coords[1] + ')';
    });

  countryGroups.append('circle')
    .attr('class', 'country-dot')
    .attr('r', 5)
    .attr('cx', 0)
    .attr('cy', 0);

  // Country name (above dot)
  countryGroups.append('text')
    .attr('class', 'country-label')
    .attr('y', -14)
    .text(function(d) { return d.name; });

  // Rate value (below dot)
  countryGroups.append('text')
    .attr('class', 'country-rate')
    .attr('y', 20)
    .text(function(d) { return d.rate + ' %'; });

  /* ── ScrollTrigger: illuminate countries one by one ─────────────── */
  var tl = gsap.timeline({
    scrollTrigger: {
      trigger: '#s2-world',
      start: 'top 60%',
      end:   'bottom 40%',
      scrub: false,
      once:  true
    }
  });

  countries.forEach(function(d, i) {
    tl.call(function() {
      // Illuminate the i-th group
      var grp = svg.selectAll('.country-group').filter(function(dd) { return dd.iso === d.iso; });
      grp.select('.country-dot').classed('lit', true);
      grp.select('.country-label').classed('lit', true);
      grp.select('.country-rate').classed('lit', true);
    }, null, i * 0.5); // 0.5s delay between each country
  });

  /* Legend */
  addVizLegend(container, [DATA.world.source, DATA.world.sourceComplement]);
}
