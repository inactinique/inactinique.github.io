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
      toc.style.display = 'none';
      return;
    }

    var fragment = document.createDocumentFragment();

    headings.forEach(function(heading, index) {
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

    // Sticky TOC behavior
    var tocOriginalTop = toc.offsetTop;
    var header = document.querySelector('.site-header');
    var headerHeight = header ? header.offsetHeight : 0;

    function handleScroll() {
      var scrollPos = window.scrollY;

      // Make TOC fixed when scrolled past its original position
      if (scrollPos > tocOriginalTop - headerHeight) {
        toc.classList.add('is-fixed');
      } else {
        toc.classList.remove('is-fixed');
      }

      // Highlight current section
      var current = null;
      headings.forEach(function(heading) {
        if (heading.offsetTop <= scrollPos + 120) {
          current = heading;
        }
      });

      var tocLinks = tocList.querySelectorAll('.toc-link');
      tocLinks.forEach(function(link) {
        link.classList.remove('active');
        if (current && link.getAttribute('href') === '#' + current.id) {
          link.classList.add('active');
        }
      });
    }

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', function() {
      tocOriginalTop = toc.classList.contains('is-fixed') ? tocOriginalTop : toc.offsetTop;
      headerHeight = header ? header.offsetHeight : 0;
    });
    handleScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', generateTOC);
  } else {
    generateTOC();
  }
})();
