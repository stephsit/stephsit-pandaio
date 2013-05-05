function open_in_new_tab(url )
{
  var win=window.open(url, '_blank');
  win.focus();
}

$(function(){
    var $container = $('#container');
    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.masonryImage'
      });
    });
    $('.masonryImage').hover(
    	function(){
    		var w = $(this).width
    		var h = $(this).height
  			var artist = $(this).attr('data-artist');
  			$(this).append('<div class="bottom-box">' + artist + '</div>');
    	},
    	function(){
		console.log($(this));
		$(this).children()[1].remove();
    });
	$('.masonryImage').click(function(){
		open_in_new_tab($(this).attr('data-url'));
	}); 
  });
