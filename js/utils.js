'use strict';

/* ── Motion preference ───────────────────────────────────────────────── */
/* Peut être surchargé via ?motion=1 dans l'URL pour la démo/soutenance */
const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  && !window.location.search.includes('motion=1');

/* Duration helper: return 0 when reduced motion is active */
function dur(d) { return REDUCED_MOTION ? 0 : d; }

/* ── Legend injector ─────────────────────────────────────────────────── */
/**
 * Appends a .viz-legend div below `containerEl`.
 * sources: array of { name, url, n } objects
 */
function addVizLegend(containerEl, sources) {
  const wrap = document.createElement('div');
  wrap.className = 'viz-legend';

  sources.forEach(function(src, i) {
    if (i > 0) {
      const sep = document.createElement('span');
      sep.className = 'viz-legend__sep';
      sep.textContent = ' · ';
      wrap.appendChild(sep);
    }
    const link = document.createElement('a');
    link.href = src.url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.className = 'viz-legend__source';
    link.textContent = src.name;
    wrap.appendChild(link);

    const nSpan = document.createElement('span');
    nSpan.className = 'viz-legend__n';
    nSpan.textContent = ' — ' + src.n;
    wrap.appendChild(nSpan);
  });

  containerEl.appendChild(wrap);
}

/* ── Blinking cursor ─────────────────────────────────────────────────── */
/**
 * Starts a CSS-class-based blink on `el`.
 * Returns the GSAP tween so it can be killed.
 */
function startCursorBlink(el) {
  if (REDUCED_MOTION) {
    el.style.opacity = '1';
    return null;
  }
  return gsap.to(el, {
    opacity: 0,
    duration: 0.55,
    ease: 'steps(1)',
    repeat: -1,
    yoyo: true
  });
}

/* ── SVG responsive size ─────────────────────────────────────────────── */
/**
 * Returns { width, height } from a container element's bounding rect,
 * clamped to sensible minimums.
 */
function svgSize(containerEl) {
  const r = containerEl.getBoundingClientRect();
  return {
    width:  Math.max(320, r.width  || 480),
    height: Math.max(260, r.height || 380)
  };
}

/* ── ScrollTrigger factory ───────────────────────────────────────────── */
/**
 * Returns a basic ScrollTrigger config object.
 * `once` prevents re-animation on scroll back.
 */
function stConfig(trigger, opts) {
  return Object.assign({
    trigger:  trigger,
    start:    'top 72%',
    once:     true
  }, opts || {});
}
