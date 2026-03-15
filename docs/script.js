/* ── France Travail API Documentation Template ──
   Vanilla JS — no dependencies.
   Provides: tab switching, hover sync, click-to-scroll, hash routing.
*/

/* ── Tab switching ── */
function setTab(id, updateHash) {
  document.querySelectorAll('.view').forEach(function(v) { v.classList.remove('active'); });
  document.getElementById('v-' + id).classList.add('active');
  document.querySelectorAll('.tab-group .tb').forEach(function(b, i) {
    b.classList.toggle('active', (id==='nested'&&i===0)||(id==='coverage'&&i===1)||(id==='example'&&i===2));
  });
  if (updateHash !== false) { history.replaceState(null, '', '#' + id); }
}

/* ── Hover highlight ──
   When hovering a [data-section] element in the example tab,
   all elements sharing the same data-section value get highlighted.
   This synchronises the JSON panel with the human narrative panel. */
document.addEventListener('mouseover', function(e) {
  var el = e.target.closest('[data-section]');
  if (!el) return;
  var section = el.getAttribute('data-section');
  document.querySelectorAll('[data-section="' + section + '"]').forEach(function(s) { s.classList.add('highlight'); });
});
document.addEventListener('mouseout', function(e) {
  var el = e.target.closest('[data-section]');
  if (!el) return;
  var section = el.getAttribute('data-section');
  document.querySelectorAll('[data-section="' + section + '"]').forEach(function(s) { s.classList.remove('highlight'); });
});

/* ── Click-to-scroll within example ──
   Clicking a [data-section] in one panel scrolls to and flashes the
   matching section in the opposite panel. */
function flashElement(el) {
  el.classList.remove('flash');
  void el.offsetWidth; // force reflow to restart animation
  el.classList.add('flash');
  setTimeout(function() { el.classList.remove('flash'); }, 1500);
}

document.addEventListener('click', function(e) {
  var el = e.target.closest('.example-split [data-section]');
  if (!el) return;
  var section = el.getAttribute('data-section');
  var panel = el.closest('.panel');
  if (!panel) return;
  var otherClass = panel.classList.contains('panel-json') ? '.panel-human' : '.panel-json';
  var target = document.querySelector(otherClass + ' [data-section="' + section + '"]');
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    flashElement(target);
  }
});

/* ── Hash routing ──
   Supports #nested, #coverage, #example for direct tab linking.
   Works on page load and browser back/forward. */
function resolveHash() {
  var hash = location.hash.replace('#', '');
  if (!hash) return;
  if (hash === 'nested' || hash === 'coverage' || hash === 'example') {
    setTab(hash, false);
  }
}

document.addEventListener('DOMContentLoaded', resolveHash);
window.addEventListener('hashchange', resolveHash);
