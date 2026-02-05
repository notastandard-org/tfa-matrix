/**
 * TFA Matrix View Toggle
 * Handles switching between Technical and Public views
 * Persists user preference in localStorage
 * Default: Public view (victims are primary audience)
 */

(function() {
  'use strict';

  var STORAGE_KEY = 'tfa_view_preference';
  var VIEWS = {
    TECHNICAL: 'technical',
    PUBLIC: 'public'
  };

  /**
   * Get saved view preference, default to PUBLIC
   */
  function getPreference() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === VIEWS.TECHNICAL || saved === VIEWS.PUBLIC) {
        return saved;
      }
      return VIEWS.PUBLIC; // Default to public for victims
    } catch (e) {
      return VIEWS.PUBLIC;
    }
  }

  /**
   * Save view preference
   */
  function savePreference(view) {
    try {
      localStorage.setItem(STORAGE_KEY, view);
    } catch (e) {
      // localStorage unavailable, preference won't persist
    }
  }

  /**
   * Apply view to the page
   */
  function applyView(view) {
    var body = document.body;
    var publicContent = document.querySelector('.view-public');
    var technicalContent = document.querySelector('.view-technical');
    var toggleBtns = document.querySelectorAll('.view-toggle-btn');

    // Update body class
    body.classList.remove('public-view', 'technical-view');
    body.classList.add(view + '-view');

    // Update content visibility
    if (publicContent && technicalContent) {
      if (view === VIEWS.PUBLIC) {
        publicContent.style.display = 'block';
        technicalContent.style.display = 'none';
      } else {
        publicContent.style.display = 'none';
        technicalContent.style.display = 'block';
      }
    }

    // Update toggle buttons
    toggleBtns.forEach(function(btn) {
      var isActive = btn.getAttribute('data-view') === view;
      if (isActive) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });

    // Update matrix technique cells if on matrix page
    updateMatrixCells(view);
  }

  /**
   * Update matrix page technique cells to show appropriate titles
   */
  function updateMatrixCells(view) {
    var cells = document.querySelectorAll('.technique-cell[data-public-title]');
    cells.forEach(function(cell) {
      var link = cell.querySelector('a');
      if (!link) return;

      var publicTitle = cell.getAttribute('data-public-title');
      var techTitle = cell.getAttribute('data-tech-title');

      if (view === VIEWS.PUBLIC && publicTitle) {
        link.textContent = publicTitle;
      } else if (techTitle) {
        link.textContent = techTitle;
      }
    });
  }

  /**
   * Initialize view toggle functionality
   */
  function init() {
    // Apply saved preference on page load
    var savedView = getPreference();
    applyView(savedView);

    // Attach click handlers to toggle buttons
    var toggleBtns = document.querySelectorAll('.view-toggle-btn');
    toggleBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var view = this.getAttribute('data-view');
        savePreference(view);
        applyView(view);
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
