(function() {
  'use strict';

  function generateTOC() {
    var content = document.querySelector('.content');
    var tocList = document.querySelector('.toc-list');
    var toc = document.querySelector('.toc');

    if (!content || !tocList || !toc) return;

    // Find all h2 and h3 headings in content
    var headings = content.querySelectorAll('h2, h3');

    if (headings.length < 2) {
      // Hide TOC if fewer than 2 headings
      toc.style.display = 'none';
      return;
    }

    var fragment = document.createDocumentFragment();

    headings.forEach(function(heading, index) {
      // Create an ID if the heading doesn't have one
      if (!heading.id) {
        heading.id = 'heading-' + index;
      }

      var li = document.createElement('li');
      li.className = 'toc-item toc-item-' + heading.tagName.toLowerCase();

      var link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = heading.textContent;
      link.className = 'toc-link';

      li.appendChild(link);
      fragment.appendChild(li);
    });

    tocList.appendChild(fragment);

    // Highlight current section on scroll
    var tocLinks = tocList.querySelectorAll('.toc-link');

    function highlightCurrentSection() {
      var scrollPos = window.scrollY + 100;

      var current = null;
      headings.forEach(function(heading) {
        if (heading.offsetTop <= scrollPos) {
          current = heading;
        }
      });

      tocLinks.forEach(function(link) {
        link.classList.remove('active');
        if (current && link.getAttribute('href') === '#' + current.id) {
          link.classList.add('active');
        }
      });
    }

    window.addEventListener('scroll', highlightCurrentSection, { passive: true });
    highlightCurrentSection();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', generateTOC);
  } else {
    generateTOC();
  }
})();
