'use strict';

function initS1Hero() {
  var titleEl  = document.getElementById('hero-typewriter');
  var cursorEl = document.getElementById('hero-cursor');
  if (!titleEl || !cursorEl) return;

  var TEXT = 'Le shadow AI chez les ingénieurs\nimprudence individuelle\nou échec collectif de gouvernance ?';

  startCursorBlink(cursorEl);

  function runTypewriter() {
    if (REDUCED_MOTION) {
      /* Affichage instantané — pas d'animation caractère par caractère */
      TEXT.split('\n').forEach(function(line, i) {
        if (i > 0) titleEl.appendChild(document.createElement('br'));
        titleEl.appendChild(document.createTextNode(line));
      });
      return;
    }
    var index = 0;
    var SPEED = 38;
    function step() {
      if (index >= TEXT.length) return;
      var ch = TEXT[index];
      if (ch === '\n') titleEl.appendChild(document.createElement('br'));
      else titleEl.appendChild(document.createTextNode(ch));
      index++;
      setTimeout(step, SPEED + (Math.random() * 18 - 9));
    }
    setTimeout(step, 300);
  }

  ScrollTrigger.create({
    trigger: '#s1-hero',
    start:   'top 80%',
    once:    true,
    onEnter: runTypewriter
  });
}
