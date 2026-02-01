(function() {
  'use strict';

  function generateTOC() {
    var content = document.querySelector('.content');
    var tocList = document.querySelector('.toc-list');
    var toc = document.querySelector('.toc');

    if (!content || !tocList || !toc) return;

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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', generateTOC);
  } else {
    generateTOC();
  }
})();
