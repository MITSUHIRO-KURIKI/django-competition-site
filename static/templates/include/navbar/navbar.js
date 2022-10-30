var heroBottom,
    startPos = 0,
    winScrollTop;
 
$(document).on('scroll',function(){

    winScrollTop = $(window).scrollTop();
    heroBottom = $('#hero-area').height();
    heroBottom = heroBottom - 50

    if (winScrollTop >= startPos) {     // 下
        if(winScrollTop >= heroBottom){
            $('#navbar').addClass('hide');
        }
    } else {                            // 上
        $('#navbar').removeClass('hide');
    }
    startPos = winScrollTop;
});
 
$(document).trigger('scroll');