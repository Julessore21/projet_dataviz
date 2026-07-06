'use strict';

function initS7Conclusion() {
  var cursorEl = document.getElementById('conclusion-cursor');
  if (!cursorEl) return;

  ScrollTrigger.create({
    trigger: '#s7-conclusion',
    start:   'top 75%',
    once:    true,
    onEnter: function() {
      startCursorBlink(cursorEl);
    }
  });
}
