/*@cc_on _d=document;eval('var document=_d')@*/

if (!navigator.userAgent.match(/(iPhone|iPad|iPod|Android)/)) {
    $(function () {
        $('html').niceScroll({
            cursorcolor: '#000000',
            cursoropacitymin: 0.3,
            cursorwidth: '13px',
            cursorborder: "1px solid #000000",
            cursorborderradius: '14px',
            oneaxismousemode: 'auto',
            zindex: '9999',
        });
    });
}