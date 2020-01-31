// SE ACTIVA EL MENU AL PRESIONAR EL ICONO EN MODO RESPONSIVO
$(document).ready(function(){
    var contador = 0;
    $('#icono').click(function () {
        if (contador == 0) {
            $('#menu').slideDown();
            contador = 1;
        } else {
            $('#menu').slideUp();
            contador = 0;
        }
    });
});
// -----------------------------------------------------------

// DEJA STICKY NUESTRO MENU (MENU FIJO)
$(document).ready(function () {
    var altura = $('.container-menu').offset().top;
    $(window).on('scroll', function() {
        if($(window).scrollTop() > altura) {
            $('.container-menu').addClass('container-fixed');
            $('.menu').addClass('container-fixed');
        } else {
            $('.container-menu').removeClass('container-fixed');
            $('.menu').removeClass('container-fixed')
        }
    });
});
// ------------------------------------------------------------

$(document).ready(function () {
    $(window).scroll(function () {
        if($(this).scrollTop() >100) {
            console.log('100 px');
        } else {
            console.log('0 scroll');
        }
    });
});