(function() {
  'use strict';

  const THEME_KEY = 'theme-preference';

  // Get stored theme or null if none
  function getStoredTheme() {
    return localStorage.getItem(THEME_KEY);
  }

  // Get system preference
  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  // Apply theme to document
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);

    // Update toggle button states
    const toggles = document.querySelectorAll('.theme-toggle');
    toggles.forEach(function(toggle) {
      toggle.classList.toggle('dark', theme === 'dark');
      toggle.setAttribute('aria-pressed', theme === 'dark');
    });
  }

  // Toggle between light and dark
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || getSystemTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  }

  // Initialize on page load
  function init() {
    const stored = getStoredTheme();
    if (stored) {
      applyTheme(stored);
    }
    // If no stored preference, CSS handles system preference via media query

    // Set up toggle buttons
    const toggles = document.querySelectorAll('.theme-toggle');
    toggles.forEach(function(toggle) {
      toggle.addEventListener('click', toggleTheme);
    });

    // Set up floating toggle visibility
    const header = document.querySelector('.site-header');
    const floatingToggle = document.querySelector('.theme-toggle-floating');

    if (header && floatingToggle) {
      var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          floatingToggle.classList.toggle('visible', !entry.isIntersecting);
        });
      }, { threshold: 0 });

      observer.observe(header);
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      if (!getStoredTheme()) {
        // Only auto-switch if user hasn't set a preference
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
