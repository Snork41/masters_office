// bootstrap Tooltips (на кнопках "редактировать запись", "следущая/предыдущая запись")
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


// Стрелка возврата в верх страницы
$(window).scroll(function() {
    if ($(this).scrollTop() > 500) {
        $('.scroll-to-top').fadeIn();
    } else {
        $('.scroll-to-top').fadeOut();
    }
}).scroll();

$('.scroll-to-top').click(function(event) {
    event.preventDefault();
    $('html, body').animate({scrollTop: 0}, 300);
});

  
// for bootstrap Toast show
// const toastContent = document.querySelector('.toast');
// const toast = new bootstrap.Toast(toastContent);
// toast.show();