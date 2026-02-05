/**
 * Browser Safety Banner
 * Shows a dismissable safety notice on first visit
 */
(function() {
  var BANNER_KEY = 'tfa_safety_banner_dismissed';
  var banner = document.getElementById('browser-safety-banner');
  var closeBtn = document.getElementById('close-safety-banner');

  if (!banner) return;

  try {
    if (localStorage.getItem(BANNER_KEY) === 'true') {
      banner.style.display = 'none';
      return;
    }
  } catch (e) {}

  banner.style.display = 'flex';

  if (closeBtn) {
    closeBtn.addEventListener('click', function() {
      banner.style.display = 'none';
      try { localStorage.setItem(BANNER_KEY, 'true'); } catch (e) {}
    });
  }
})();
