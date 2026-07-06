'use strict';

function initS5Productivity() {
  var container = document.getElementById('viz-diff-wrap');
  if (!container) return;

  var lines = DATA.productivity.diffLines;

  /* ── Build diff DOM ─────────────────────────────────────────────── */
  var block = document.createElement('div');
  block.className = 'diff-block';

  // Header bar
  var header = document.createElement('div');
  header.className = 'diff-block__header';
  header.textContent = 'productivite_percue.diff';
  block.appendChild(header);

  // Build each line element
  var lineEls = lines.map(function(d) {
    var row = document.createElement('div');
    row.className = 'diff-line diff-line--' + d.type;

    var codeSpan = document.createElement('span');
    codeSpan.className = 'diff-code';
    codeSpan.textContent = d.code;
    row.appendChild(codeSpan);

    if (d.comment) {
      var commentSpan = document.createElement('span');
      commentSpan.className = 'diff-comment';
      commentSpan.textContent = d.comment;
      row.appendChild(commentSpan);
    }

    block.appendChild(row);
    return row;
  });

  container.appendChild(block);

  // Contrepoint note
  var note = document.createElement('p');
  note.className = 'viz-note';
  note.textContent = DATA.productivity.cuiNote;
  container.appendChild(note);

  // Legend (two sources)
  addVizLegend(container, [DATA.productivity.source, DATA.productivity.sourceComplement]);

  /* ── Animation ────────────────────────────────────────────────────── */
  ScrollTrigger.create({
    trigger: '#s5-productivity',
    start: 'top 65%',
    once: true,
    onEnter: function() {
      gsap.to(lineEls, {
        opacity: 1,
        x: 0,
        duration: dur(0.35),
        stagger: dur(0.08),
        ease: 'power2.out'
      });
    }
  });
}
