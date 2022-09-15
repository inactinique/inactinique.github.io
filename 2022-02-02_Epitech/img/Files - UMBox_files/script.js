var openContextOnRightClick = function (event) {
  event.stopPropagation();
  event.preventDefault();

  var appName = 'files_rightclick';
  var currentFile = $(event.target).closest('tr');
  var leftToRemove = currentFile.find('.selection').width();

  if (currentFile.find('.fileActionsMenu').length != 0) {
    currentFile.find('.fileActionsMenu').remove();
    currentFile.removeClass('mouseOver');
    currentFile.removeClass('highlighted');
    currentFile.find('.action-menu').removeClass('open');

    return false;
  }

  setTimeout(function () {
    if ($(event.target).parent().hasClass('fileactions') || $(event.target).parent().parent().hasClass('fileactions')) {
      $(event.target).click();
      return false;
    }
    else
      currentFile.find('.action-menu').click();

    var menu = currentFile.find('.fileActionsMenu');
    var menuStyle = $('style.rightClickStyle');
    var top = (event.pageY - currentFile.offset().top + (currentFile.height() / 4));
    var left = event.pageX - currentFile.offset().left - leftToRemove - (menu.width() / 2) - 4;
    var generateNewOption = function (action, icon, text, onClick) {
      menu.find('ul').prepend(
        $('<li><a href="#" class="menuitem action action-' + action.toLowerCase() + ' permanent" data-action="' + action + '"><span class="icon icon-' + icon + '"></span><span>' + text + '</span></a></li>').on('click', function (event) {
          event.stopPropagation();
          event.preventDefault();

          menu.remove();
          currentFile.removeClass('mouseOver');
          currentFile.removeClass('highlighted');
          currentFile.find('.action-menu').removeClass('open');

          onClick();
        })
      );
    };

    menu.addClass('rightClickMenu');

    if (left < (-leftToRemove)) {
      right = menu.width();
      left = (-leftToRemove);

      if ((event.pageX - currentFile.offset().left) <= 11)
        menuStyle.text('.fileActionsMenu.rightClickMenu{border-top-left-radius:0} .fileActionsMenu.rightClickMenu:after{left:0}');
      else
        menuStyle.text('.fileActionsMenu.rightClickMenu:after{transform:translateX(-50%);left:' + (event.pageX - currentFile.offset().left) + 'px}');
    } else if (left + menu.width() + leftToRemove + 10 > currentFile.width()) {
      right = 0;
      left = currentFile.width() - leftToRemove - menu.width() - 10;

      if ((event.pageX - currentFile.offset().left - leftToRemove - left) >= (menu.width() - 11))
        menuStyle.text('.fileActionsMenu.rightClickMenu{border-top-right-radius:0} .fileActionsMenu.rightClickMenu:after{right:0}');
      else
        menuStyle.text('.fileActionsMenu.rightClickMenu:after{transform:translateX(-50%);left:' + (event.pageX - currentFile.offset().left - leftToRemove - left) + 'px}');
    } else
      menuStyle.text('.fileActionsMenu.rightClickMenu:after{transform:translateX(-50%);left:' + (menu.width() / 2) + 'px}');

    menu.css({
      right: 'auto',
      top: top,
      left: left
    });

    var mimeType = currentFile.attr('data-mime');
    var text = '';
    var icon = 'toggle';
    var onClick = function () {
      currentFile.find('.filename .nametext').click();
    };

    var share = currentFile.find('.filename .fileactions .action-share');

    if (share.length !== 0) {
      generateNewOption('Share', 'share', t(appName, 'Share this ' + (currentFile.attr('data-type') === 'dir' ? 'folder' : 'file')), function () {
        share.click();
      });
    }

    if (currentFile.attr('data-type') === 'dir') {
      text = t(appName, 'Open this folder');
      icon = 'filetype-folder-drag-accept';

      generateNewOption('Open', 'category-app-bundles', t(appName, 'Open in a new tab'), function () {
        window.open('?dir=' + currentFile.attr('data-path') + (currentFile.attr('data-path') === '/' ? '' : '/') + currentFile.attr('data-file'), "_blank");
      });
    }
    else if (mimeType === 'text/plain') {
      text = t(appName, 'Edit this file');
      icon = 'edit';
    }
    else if (mimeType === 'application/pdf') {
      text = t(appName, 'Read this PDF');
    }
    else if (mimeType.indexOf('image') >= 0) {
      text = t(appName, 'See this picture');

      generateNewOption('Open', 'category-multimedia', t(appName, 'Open in the gallery app'), function () {
        window.open('/apps/gallery' + currentFile.attr('data-path').replace('/', '/#') + (currentFile.attr('data-path') === '/' ? '' : '/') + currentFile.attr('data-file'), "_blank");
      });
    }
    else if (mimeType.indexOf('audio') >= 0) {
      var isReading = function () {
        return (currentFile.find('.ioc').length === 1) && (currentFile.find('.ioc').css('display') !== 'none');
      };

      if (isReading()) {
        text = t(appName, 'Stop playing');
        icon = 'pause';
      }
      else {
        text = t(appName, 'Start playing');
        icon = 'play';

        onClick = function () {
          while (!isReading()) {
            currentFile.find('.filename .nametext').click();
          }
        };
      }
    }
    else if (mimeType.indexOf('video') >= 0) {
      text = t(appName, 'Start watching');
      icon = 'play';
    }
    else if (currentFile.attr('data-type') === 'file') {
      text = t(appName, 'Open this file');
    }

    if (text !== '') {
      generateNewOption('Open', icon, text, onClick);
    }
  }, 200)

  return false;
};

$('<style class="rightClickStyle"></style>').appendTo('head');
$('#fileList').contextmenu(openContextOnRightClick);
